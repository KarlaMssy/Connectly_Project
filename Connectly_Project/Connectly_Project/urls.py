from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from authors.views import AuthorViewSet
from posts.views import PostViewSet

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Token login endpoint
    path('api/login/', obtain_auth_token),

    # DRF router URLs
    path('api/', include(router.urls)),

    # Custom posts URLs (like feed, like, comment)
    path('api/posts/', include('posts.urls')),

    # Any auth_app URLs
    path('api/auth/', include('auth_app.urls')),
]