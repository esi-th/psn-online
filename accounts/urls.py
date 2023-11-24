from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('', views.account_page_view, name='accounts_hub'),
    path('dashboard/', views.dashboard_page_view, name='dashboard'),
    path('dashboard/orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist_view, name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist_view, name='wishlist_remove'),
]
