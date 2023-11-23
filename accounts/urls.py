from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('', views.account_page_view, name='accounts_hub'),
    #path('dashboard', views.dashboard_page_view, name='dashboard')
]
