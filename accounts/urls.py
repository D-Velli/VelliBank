from django.urls import path
from .views import dashboard,compte

app_name = "accounts"

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('compte/<str:numero_compte>', compte, name='compte'),
]