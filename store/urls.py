from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('category/<int:category_id>/', views.CategoryProductListView.as_view(), name='category_products'),
    path('discounted/', views.DiscountedProductListView.as_view(), name='discounted_products'),

    path('product/new/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]
