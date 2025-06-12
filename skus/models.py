from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

UserModel = get_user_model()


class Sku(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
