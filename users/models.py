from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=255, default=None, blank=False, null=False)

    last_name = models.CharField(max_length=255, default=None, blank=False, null=False)

    username = models.CharField(
        max_length=255, unique=True, default=None, blank=False, null=False
    )

    email = models.CharField(
        max_length=255, unique=True, default=None, blank=False, null=False
    )

    password = models.CharField(max_length=255)

    password_reset_token = models.CharField(
        max_length=255, default=None, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    class Meta:
        db_table = "users"
