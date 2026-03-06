from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Post, Like
from .serializers import PostSerializer, CommentSerializer
from authors.models import Author


# -----------------------
# Post ViewSet
# -----------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')  # newest first
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # Ensure posts only have valid authors
    def create(self, request, *args, **kwargs):
        author_id = request.data.get('author')

        if not author_id:
            return Response(
                {"error": "Author is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return super().create(request, *args, **kwargs)


# -----------------------
# Like Post
# -----------------------
@api_view(['POST'])
def like_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        return Response(
            {"error": "You already liked this post"},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {"message": "Post liked successfully"},
        status=status.HTTP_201_CREATED
    )


# -----------------------
# Comment on Post
# -----------------------
@api_view(['POST'])
def comment_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------
# Get Comments
# -----------------------
@api_view(['GET'])
def get_comments(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    comments = post.comments.all().order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


# -----------------------
# News Feed View
# -----------------------
class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 1️ Get all posts
        posts = Post.objects.all()

        # 2️ Sort newest first
        posts = posts.order_by('-created_at')

        # 3️ Paginate
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)