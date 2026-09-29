from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_refresh_token,
    issue_refresh_token,
    refresh_expiry,
    verify_password,
    verify_unknown_user_password,
)
from app.models.identity import Branch, RefreshToken, Role, User
from app.schemas.auth import TokenPair


def _create_pair(db: Session, user: User) -> TokenPair:
    access_token, expires_in = create_access_token(user.id)
    refresh_token = issue_refresh_token()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_expiry(),
        )
    )
    db.commit()
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
    )


def login(db: Session, email: str, password: str) -> TokenPair:
    normalized_email = email.strip().casefold()
    user = db.scalar(select(User).where(User.email == normalized_email))
    if user is None:
        verify_unknown_user_password(password)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    password_ok = verify_password(password, user.hashed_password)
    if not password_ok or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    if user.role == Role.BRANCH:
        branch = db.get(Branch, user.branch_id) if user.branch_id else None
        if branch is None or not branch.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    return _create_pair(db, user)


def rotate_refresh_token(db: Session, raw_token: str) -> TokenPair:
    now = datetime.now(UTC)
    token_row = db.scalar(
        select(RefreshToken)
        .where(RefreshToken.token_hash == hash_refresh_token(raw_token))
        .with_for_update()
    )
    if (
        token_row is None
        or token_row.revoked_at is not None
        or token_row.expires_at <= now
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session has expired. Sign in again.")
    user = db.get(User, token_row.user_id)
    if user is None or not user.is_active:
        token_row.revoked_at = now
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session has expired. Sign in again.")

    # Revoke and replace in one transaction. The database row lock prevents
    # two simultaneous refresh requests from both rotating the same token.
    token_row.revoked_at = now
    access_token, expires_in = create_access_token(user.id)
    refresh_token = issue_refresh_token()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_expiry(),
        )
    )
    db.commit()
    return TokenPair(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in)


def revoke_refresh_token(db: Session, raw_token: str | None) -> None:
    if not raw_token:
        return
    token_row = db.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hash_refresh_token(raw_token))
    )
    if token_row is not None and token_row.revoked_at is None:
        token_row.revoked_at = datetime.now(UTC)
        db.commit()
