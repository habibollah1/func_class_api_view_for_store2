from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


# router = SimpleRouter()
router = DefaultRouter()
# ثبت ProductViewSet در روتر
router.register('products', views.ProductViewSet, 'product')  # including: product-list | product-detail
router.register('category', views.CategoryViewSet, basename='category')  # Even if you don't give it a bass-name,
# it will recognize it based on the model

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = router.urls
