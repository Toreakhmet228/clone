# urls.py
from django.contrib import admin
from django.urls import path
from shtoto_app.views import (
    RegisterUserView,
    LoginUserView,
    UserProfileView,
    PublicCategoryListView,  # Добавлено
    CategoryListView,
    SubCategoryListView,
    ProductListView,
    ProductDetailView,
    ProductReviewListView,
    CartView,
    OrderListView,

    CategoryDetailView,
SearchView  # Добавлено
)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from shtoto_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/item/<int:item_id>/', views.CartItemDeleteView.as_view(), name='cart-item-delete'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('categories/', views.PublicCategoryListView.as_view(), name='public-categories'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/reviews/', views.ProductReviewListView.as_view(), name='product-reviews'),
    path('subcategories/', views.SubCategoryListView.as_view(), name='subcategory-list'),
path('favorites/', views.FavoriteView.as_view(), name='favorites'),
    path('favorites/<int:product_id>/', views.FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('api/create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
path('webhook/', views.stripe_webhook, name='stripe-webhook'),
path('orders/<int:order_id>/status/', views.OrderStatusView.as_view(), name='order-status'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)