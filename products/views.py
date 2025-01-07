from django.http import HttpRequest, JsonResponse

from products.models import Product


def test(request: HttpRequest):
    product = Product.objects.first()
    sku = getattr(product, "sku", None)

    return JsonResponse({"sku": sku})
