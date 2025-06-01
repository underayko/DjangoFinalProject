# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import Item

# # GET all items or filter items
# def get_items(request):
#     search_query = request.GET.get('search', None)
#     items = Item.objects.all()

#     if search_query:
#         items = items.filter(name__icontains=search_query)

#     data = list(items.values())
#     return JsonResponse({'items': data}, safe=False)

# # GET a single item
# def get_item(request, item_id):
#     try:
#         item = Item.objects.get(id=item_id)
#         return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description})
#     except Item.DoesNotExist:
#         return JsonResponse({'error': 'Item not found'}, status=404)

# # POST - Add a new item
# @csrf_exempt
# def add_item(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         item = Item.objects.create(name=data['name'], description=data.get('description', ''))
#         return JsonResponse({'message': 'Item added!', 'id': item.id})

# # PUT - Update an item
# @csrf_exempt
# def update_item(request, item_id):
#     try:
#         item = Item.objects.get(id=item_id)
#         data = json.loads(request.body)
#         item.name = data.get('name', item.name)
#         item.description = data.get('description', item.description)
#         item.save()
#         return JsonResponse({'message': 'Item updated!'})
#     except Item.DoesNotExist:
#         return JsonResponse({'error': 'Item not found'}, status=404)

# # DELETE - Delete an item
# @csrf_exempt
# def delete_item(request, item_id):
#     try:
#         item = Item.objects.get(id=item_id)
#         item.delete()
#         return JsonResponse({'message': 'Item deleted!'})
#     except Item.DoesNotExist:
#         return JsonResponse({'error': 'Item not found'}, status=404)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import json
from .models import Item
from ua.serializers import RegisterSerializer  # Since your serializer is inside ua app
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from dashboard.models import Post
from ua.models import Profile
from .serializers import ItemSerializer, PostSerializer, ProfileSerializer

# Register endpoint - only responds with JSON
class RegisterView(APIView):
    renderer_classes = [JSONRenderer]  # Disables DRF browsable API form

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "Registration successful!",
            "user": {
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Existing item views
def get_items(request):
    search_query = request.GET.get('search', None)
    items = Item.objects.all()

    if search_query:
        items = items.filter(name__icontains=search_query)

    data = list(items.values())
    return JsonResponse({'items': data}, safe=False)

def get_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        return JsonResponse({'id': item.id, 'name': item.name, 'description': item.description})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item = Item.objects.create(name=data['name'], description=data.get('description', ''))
        return JsonResponse({'message': 'Item added!', 'id': item.id})

@csrf_exempt
def update_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        data = json.loads(request.body)
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.save()
        return JsonResponse({'message': 'Item updated!'})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

@csrf_exempt
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'message': 'Item deleted!'})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

# CRUD for Item
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

# CRUD for Post
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

# CRUD for Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]