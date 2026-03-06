from django.urls import path
from .views import FeedView, like_post, comment_post, get_comments

urlpatterns = [
    # News Feed
    path('feed/', FeedView.as_view(), name='feed'),

    # Post interactions
    path('<int:id>/like/', like_post, name='like_post'),
    path('<int:id>/comment/', comment_post, name='comment_post'),
    path('<int:id>/comments/', get_comments, name='get_comments'),
]