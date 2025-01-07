from django.db import models

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Address(models.Model):
    id = models.AutoField(primary_key=True)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
