from app.models import Article, Author


async def get_articles_for_author(author_id: int):
    return await Article.filter(authors__id=author_id)
    

async def get_article(article_id: int):
    return await Article.get_or_none(id=article_id)


async def create_article(author: Author, title: str, content: str):
    article = await Article.create(title=title, content=content)
    await article.authors.add(author)
    return article


async def update_article(article_id: int, title: str, content: str):
    article = await Article.get(id=article_id)
    article.title = title
    article.content = content
    await article.save()
    return article


async def delete_article(article_id: int):
    await Article.get(id=article_id).delete()