from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.config import TORTOISE_ORM
from app.auth.auth_routes import router as auth_router
from app.routers.article import router as article_router


app = FastAPI()


register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(article_router, prefix="/articles", tags=["articles"])


@app.get("/")
async def root():
    return {"message": "FastAPI with PostgreSQL and Tortoise ORM connected successfully!"}
