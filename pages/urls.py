from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutUsPageView.as_view(), name='about_us'),
    path('contact/', views.contact_us_page_view, name='contact_us'),
]
