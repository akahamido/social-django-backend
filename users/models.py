from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,PermissionsMixin
import uuid
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email=None, username=None, phone=None, password=None, **extra_fields):
        if not (email or username or phone):
            raise ValueError("حداقل یکی از فیلدهای email، username یا phone باید پر باشد.")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپریوزر باید is_staff=True باشد.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپریوزر باید is_superuser=True باشد.")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = []      

    objects = UserManager()   
    def __str__(self):
        return self.username or self.email or str(self.id)
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    mentions = models.ManyToManyField('users.User', related_name='mentioned_in_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post {self.id} by {self.author}"

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    mentions = models.ManyToManyField('users.User', related_name='mentioned_in_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id} on {self.post.id}"

class UsernameChangeHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', related_name='username_history', on_delete=models.CASCADE)
    old_username = models.CharField(max_length=150, null=True, blank=True)
    new_username = models.CharField(max_length=150, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
