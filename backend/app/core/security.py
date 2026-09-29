import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hasher = PasswordHash.recommended()
# Verifying this when an email is unknown makes the common invalid-login path
# spend roughly the same password-hash work as a known account.
_DUMMY_PASSWORD_HASH = password_hasher.hash("not-a-real-mitra-solar-password")


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        return password_hasher.verify(password, encoded_hash)
    except (ValueError, TypeError):
        return False


def verify_unknown_user_password(password: str) -> None:
    verify_password(password, _DUMMY_PASSWORD_HASH)


def create_access_token(user_id: UUID) -> tuple[str, int]:
    now = datetime.now(UTC)
    lifetime = timedelta(minutes=settings.access_token_minutes)
    token = jwt.encode(
        {
            "sub": str(user_id),
            "typ": "access",
            "iat": now,
            "exp": now + lifetime,
            "jti": str(uuid4()),
        },
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )
    return token, int(lifetime.total_seconds())


def decode_access_token(token: str) -> UUID:
    claims = jwt.decode(
        token,
        settings.jwt_secret.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "typ", "iat", "exp", "jti"]},
    )
    if claims.get("typ") != "access":
        raise jwt.InvalidTokenError("Wrong token type")
    return UUID(claims["sub"])


def issue_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def refresh_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.refresh_token_days)
