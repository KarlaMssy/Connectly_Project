from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PostListCreateView, FeedView, PostCommentsView, like_post, AddCommentView

urlpatterns = [
    # Posts — list & create
    path('', PostListCreateView.as_view(), name='post-list-create'),

    # Feed
    path('feed/', FeedView.as_view(), name='feed'),

    # Comments
    path('<int:post_id>/comments/', PostCommentsView.as_view(), name='get_comments'),  # GET
    path('<int:post_id>/comment/', AddCommentView.as_view(), name='add_comment'),      # POST

    # Likes
    path('<int:post_id>/like/', like_post, name='post-like'),

    # JWT Authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]