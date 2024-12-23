from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db.models import (
    Model,
    AutoField,
    ForeignKey,
    CASCADE,
    SET_NULL,
    DateTimeField,
    CharField,
    TextField,
    BooleanField,
    EmailField,
    ManyToManyField,
    Sum,
    IntegerField,
)
from django.db.models.functions import Coalesce, Cast
from random_username.generate import generate_username
from tree_queries.models import TreeNode


def get_default_user_display_name():
    return generate_username()[0]


class User(AbstractBaseUser, PermissionsMixin):
    id = AutoField(primary_key=True)
    username = EmailField(unique=True)
    email = EmailField(null=True)
    name = CharField(max_length=255, unique=True, default=get_default_user_display_name)
    created_at = DateTimeField(auto_now_add=True)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    USERNAME_FIELD = "username"
    objects = UserManager()

    def __str__(self):
        return self.name

    @staticmethod
    def owner_field():
        return "id"


class Tag(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


AUTHOR = "author"
SCORE = "score"


class Post(Model):
    PROMPT_MODES = ((AUTHOR, AUTHOR), (SCORE, SCORE))

    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    chat_role = TextField(max_length=65535, default="You are a helpful assistant.")
    tags = ManyToManyField(Tag, blank=True)
    prompt_mode = CharField(max_length=255, default=AUTHOR, choices=PROMPT_MODES)

    def __str__(self):
        return f"{self.id}|{self.title}"

    @staticmethod
    def owner_field():
        return "author_id"

    @property
    def total_score(self):
        score = PostScore.objects.filter(post=self).aggregate(
            score=Coalesce(Sum((Cast("upvote", IntegerField()) * 2 - 1)), 0)
        )["score"]
        return score


class Comment(TreeNode):
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    text = TextField(max_length=65535)
    post = ForeignKey(Post, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_prompt = BooleanField(default=False)

    @staticmethod
    def owner_field():
        return "author_id"

    @property
    def total_score(self):
        query = CommentScore.objects.filter(comment=self)
        upvotes = query.filter(upvote=True).count()
        downvotes = query.filter(upvote=False).count()
        return upvotes - downvotes


class CommentScore(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE)
    upvote = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    comment = ForeignKey(Comment, on_delete=CASCADE)

    @staticmethod
    def owner_field():
        return "user_id"

    class Meta:
        unique_together = ("user", "comment")


class PostScore(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE)
    upvote = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    post = ForeignKey(Post, on_delete=CASCADE)

    class Meta:
        unique_together = ("user", "post")

    @staticmethod
    def owner_field():
        return "user_id"
