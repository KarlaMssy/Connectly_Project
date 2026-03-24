from django.db.models import Q
from requests import post
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.exceptions import PermissionDenied  

# -----------------
# Posts — List & Create
# -----------------
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Guest: only public posts
        if getattr(user, 'role', None) == 'guest':
            return Post.objects.filter(privacy='public').order_by('-created_at')
        # Users/Admin: public + own private posts
        return Post.objects.filter(Q(privacy='public') | Q(user=user)).order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user

        # Only users with role 'admin' or 'user' can create posts
        if user.role not in ['admin', 'user']:
              from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Guests cannot create posts")

        serializer.save(user=user)


# -----------------
# Feed — list all posts
# -----------------
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # Guests: only public posts
        
        posts = Post.objects.filter(Q(privacy='public') | Q(user=user)).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response({
            "count": posts.count(),
            "results": serializer.data
        })


# -----------------
# Get comments for a post
# -----------------
class PostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        # Guest cannot see comments of private posts
        user = self.request.user
        if post.privacy == 'private' and getattr(user, 'role', None) == 'guest' and post.user != user:
            return Comment.objects.none()
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')


# -----------------
# Add a comment to a post
# -----------------
class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user  # ✅ get the user

        # Only admins and regular users can comment
        if user.role not in ['admin', 'user']:
            raise PermissionDenied("Guests cannot comment")

        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)

        # Prevent commenting on others' private posts
        if post.privacy == 'private' and post.user != user:
            raise PermissionDenied("Cannot comment on others' private posts")

        serializer.save(user=user, post=post)
# -----------------
# Like a post
# -----------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Guests cannot like posts
    if getattr(user, 'role', None) == 'guest':
        return Response({"error": "Guests cannot like posts"}, status=status.HTTP_403_FORBIDDEN)

    # Users cannot like private posts they do not own
    if post.privacy == 'private' and post.user != user:
        return Response({"error": "Cannot like other users' private posts"}, status=status.HTTP_403_FORBIDDEN)

    like, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        return Response({"error": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": f"Post {post.id} liked successfully"}, status=status.HTTP_201_CREATED)
