from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for a custom user"""

    def create_user(self, email, name, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have name')

        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password, **extra_fields):
        """Create and save a new super user"""
        user = self.create_user(email, name, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class TodoList(models.Model):
    """Todo list objects"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    DEFAULT_NAME = 'Default'

    def __str__(self):
        """String representation of TodoList"""
        return self.name


class TodoTask(models.Model):
    """Todo Task objects"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    todo_list = models.ForeignKey(
        'core.TodoList',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    def __str__(self):
        """String representation of TodoTask"""
        return self.title
