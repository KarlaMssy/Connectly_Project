from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from authors.models import Author

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Ensure posts only have valid authors
    def create(self, request, *args, **kwargs):
        author_id = request.data.get('author')
        if not author_id:
            return Response({"error": "Author is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().create(request, *args, **kwargs)
