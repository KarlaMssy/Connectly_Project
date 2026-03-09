from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from authors.views import AuthorViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),

    # Login endpoint
    path('api/login/', obtain_auth_token),
    path('api/token/', obtain_auth_token, name='api_token_auth'),  # for obtaining auth token

    # Custom post URLs (feed, like, comment)
    path('api/posts/', include('posts.urls')),  
]