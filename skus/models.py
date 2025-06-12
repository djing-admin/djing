from django.db import models


class Sku(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255)

    product = models.OneToOneField(
        "products.Product",
        related_name="sku",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
