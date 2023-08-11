from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
