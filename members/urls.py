from django.urls import path
from .views import login, register, reset_password, logout

app_name = 'members'
urlpatterns = [
    path('auth/login', login, name='login'),
    path('auth/register', register, name='register'),
    path('reset_password', reset_password, name='reset_password'),
    path('logout', logout, name='logout'),

]