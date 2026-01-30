import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User, Post

# --- USER VIEWS ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # This locks the door!
def get_users(request):
    try:
        users = list(User.objects.values('id', 'username', 'email', 'created_at'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    try:
        data = json.loads(request.body)
        user = User.objects.create(username=data['username'], email=data['email'])
        return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# --- POST VIEWS ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    try:
        posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    try:
        data = json.loads(request.body)
        author = User.objects.get(id=data['author'])
        post = Post.objects.create(content=data['content'], author=author)
        return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Author not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)