from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.identity import User
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair, UserRead
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> TokenPair:
    return auth_service.login(db, str(payload.email), payload.password)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: Annotated[Session, Depends(get_db)]) -> TokenPair:
    return auth_service.rotate_refresh_token(db, payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshRequest, db: Annotated[Session, Depends(get_db)]) -> None:
    auth_service.revoke_refresh_token(db, payload.refresh_token)


@router.get("/me", response_model=UserRead)
def me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
