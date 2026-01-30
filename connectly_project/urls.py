from django.contrib import admin
from django.urls import path, include
# Import the views for your Security Enhancement task
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # The "Security Doors" for your Milestone 1 task
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # This points down to the posts/urls.py file you just fixed
    path('', include('posts.urls')), 
]