from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import auth, models, services
from app.core.config import settings

router = APIRouter()


@router.post("/token", response_model=models.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Получение JWT токена по логину и паролю.
    """
    user = services.get_user(username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/salary", response_model=models.SalaryInfo)
async def read_own_salary(
    current_user: Annotated[models.UserInDB, Depends(auth.get_current_user)],
):
    """
    Получение данных о своей зарплате.
    Доступно только аутентифицированным пользователям.
    """
    return current_user
