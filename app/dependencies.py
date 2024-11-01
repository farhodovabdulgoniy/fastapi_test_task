from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from app.models import Author
from app.config import SECRET_KEY, ALGORITHM
from app.auth.jwt import decode_access_token
from tortoise.exceptions import DoesNotExist


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_author(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    try:
        author = await Author.get(username=username)
    except DoesNotExist:
        raise credentials_exception

    return author