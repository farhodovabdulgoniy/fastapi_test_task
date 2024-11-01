from pydantic import BaseModel
from typing import Optional


class AuthorCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ArticleCreate(BaseModel):
    title: str
    content: str


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True
