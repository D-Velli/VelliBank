from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('members/', include('members.urls')),
    path('notifications/', include('notifications.urls')),
    path('accounts/', include('accounts.urls')),
]
