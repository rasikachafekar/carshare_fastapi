from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select
from starlette import status

from schemas import User, UserOutput
from db import get_session

security = HTTPBasic()

def get_current_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        session: Annotated[Session, Depends(get_session)]) -> UserOutput:
    query = select(User).where(User.username == credentials.username)
    user = session.exec(query).first()
    if user and user.verify_password(credentials.password):
        return UserOutput.model_validate(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect."
        )