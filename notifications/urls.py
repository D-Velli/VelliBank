from django.urls import path
from .views import index

app_name = "notifications"

urlpatterns =[
    path('', index, name='index'),
]