from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from app.auth.jwt import create_access_token
from app.models import Author
from app.schemas import AuthorCreate, Token
from tortoise.exceptions import DoesNotExist


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


@router.post("/register", response_model=Token)
async def register(author: AuthorCreate):
    author_obj = await Author.create(
        username=author.username,
        hashed_password=bcrypt.hash(author.password)
    )
    access_token = create_access_token(data={"sub": author_obj.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login(author: AuthorCreate):
    try:
        author_obj = await Author.get(username=author.username)
        if not author_obj.verify_password(author.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(data={"sub": author_obj.username})
    return {"access_token": access_token, "token_type": "bearer"}
