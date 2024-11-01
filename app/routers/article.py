from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from app.schemas import (
    ArticleCreate,
    ArticleResponse
)
from app.crud.article import (
    get_articles_for_author,
    get_article,
    create_article,
    update_article,
    delete_article,
)
from app.dependencies import get_current_author


router = APIRouter()


@router.get("/", response_model=list[ArticleResponse])
async def read_articles(author=Depends(get_current_author)):
    return await get_articles_for_author(author.id)


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article_by_author(
        article_id: int,
        author=Depends(get_current_author)):

    article_db = await get_article(article_id)

    if not article_db:
        raise HTTPException(status_code=404, detail="Article not found")

    article_author_exists = await author.articles.filter(id=article_db.id).exists()

    if not article_author_exists:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this article")

    return article_db


@router.post("/", response_model=ArticleResponse)
async def create_new_article(
        article: ArticleCreate,
        author=Depends(get_current_author)):
    return await create_article(author, article.title, article.content)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_existing_article(
        article_id: int,
        article: ArticleCreate,
        author=Depends(get_current_author)):

    article_db = await get_article(article_id)
    article_author = await author.articles.filter(id=article_db.id)

    if not (article_db and article_author):
        raise HTTPException(status_code=404, detail="Article not found")

    return await update_article(article_db.id, article.title, article.content)


@router.delete("/{article_id}")
async def delete_existing_article(article_id: int, author=Depends(get_current_author)):
    article_db = await get_article(article_id)

    article_author_exists = await author.articles.filter(id=article_db.id).exists()

    if not (article_db and article_author_exists):
        raise HTTPException(status_code=404, detail="Article not found")

    await delete_article(article_db.id)
    return {"status": "Article deleted"}
