from django.db.models import Model, AutoField, ForeignKey, CASCADE, SET_NULL, DateTimeField, CharField, TextField, \
    BooleanField, EmailField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password


class GoogleUserManager(UserManager):
    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        del extra_fields["is_staff"]
        return self._create_user(email, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = AutoField(primary_key=True)
    email = EmailField(unique=True)
    google_id = CharField(max_length=255, unique=True)
    name = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = GoogleUserManager()

    def __str__(self):
        return self.email


class Post(Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)


class Comment(Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    text = TextField(max_length=255)
    post_id = ForeignKey(Post, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_prompt = BooleanField(default=False)


class CommentScore(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    upvote = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    comment = ForeignKey(Comment, on_delete=CASCADE)


class PostScore(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    upvote = BooleanField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    post = ForeignKey(Post, on_delete=CASCADE)