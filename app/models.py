from tortoise import fields, models
from passlib.hash import bcrypt


class Author(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    hashed_password = fields.CharField(max_length=128)
    articles = fields.ManyToManyField("models.Article", related_name="authors")

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)


class Article(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
