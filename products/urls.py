from django.urls import path

from products import views

urlpatterns = [
    path("list", views.test, name="test"),
]
