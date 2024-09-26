from django.urls import path
import random
from .views import dashboard,compte, carte, gestion_carte

app_name = "accounts"

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('compte/<str:numero_compte>', compte, name='compte'),
    path('compte/carte/<int:carte_id>', carte, name='carte'),
    path('compte/carte/gestion-carte/<int:carte_id>', gestion_carte, name='gestion_carte'),
]