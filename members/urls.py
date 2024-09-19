from django.urls import path
from .views import login, register, reset_password, dashboard, logout

app_name = 'members'
urlpatterns = [
    path('auth/login', login, name='login'),
    path('auth/register', register, name='register'),
    path('reset_password', reset_password, name='reset_password'),
    path('dashboard', dashboard, name='dashboard'),
    path('logout', logout, name='logout'),

]