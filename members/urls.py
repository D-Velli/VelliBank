from django.urls import path
from .views import LoginView


app_name = 'members'
urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
]