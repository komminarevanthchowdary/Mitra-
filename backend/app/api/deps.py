from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.identity import Branch, Role, User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sign in to continue.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized
    try:
        user_id = decode_access_token(credentials.credentials)
    except Exception as exc:
        raise unauthorized from exc
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise unauthorized
    if user.role == Role.BRANCH:
        branch = db.get(Branch, user.branch_id) if user.branch_id else None
        if branch is None or not branch.is_active:
            raise HTTPException(status_code=403, detail="This branch account is not active.")
    return user


def require_roles(*allowed: Role) -> Callable[..., User]:
    def dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to do this.")
        return user

    return dependency
