from django.db import models


class Address(models.Model):
    id = models.AutoField(primary_key=True)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    user = models.OneToOneField(
        "Address",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="address",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
