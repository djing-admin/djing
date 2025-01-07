from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Product(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)
    image = models.FileField(max_length=255, default=None, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=4, default=None, blank=True, null=True
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
