from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework import status, generics,mixins
from rest_framework.decorators import api_view, APIView,permission_classes
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from accounts.serializers import CurrentUserPostsSerializer
from .permissions import ReadOnly, AuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

class CustomPaginator(PageNumberPagination):
    page_size=3
    page_query_param="page"
    page_size_query_param="page_size"

@api_view(http_method_names=["GET","POST"])
@permission_classes([AllowAny])
def homepage(request:Request):
    
    if request.method == "POST":
        data=request.data
        response={"message":"Hello World","data":data}
        return Response(data=response,status=status.HTTP_201_CREATED)
    
    response={"message":"Hello World"}
    return Response(data=response,status=status.HTTP_200_OK)

class PostListCreateView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    """
        a view for creating and lisiting posts
    """
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    queryset=Post.objects.all()
    pagination_class = CustomPaginator
    
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)
    
    @swagger_auto_schema(
        operation_summary="List all posts",
        operation_description="Returns a list of all posts"
    )
    
    def get(self, request:Request,*args,**kwargs):
        return self.list(request,*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="Creates a new post"
    )
    
    def post(self, request:Request,*args,**kwargs):
        return self.create(request,*args, **kwargs)

class PostRetrieveUpdateDeleteView(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class=PostSerializer
    permission_classes=[AuthorOrReadOnly]

    queryset=Post.objects.all()
    
    @swagger_auto_schema(
        operation_summary="Retrieve a post by id",
        operation_description="Returns a post by id"
    )

    
    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a post by id",
        operation_description="Updates a post by id"
    )

    def put(self, request:Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a post by id",
        operation_description="Deletes a post by id"
    )

    def delete(self, request:Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request:Request):
    user=request.user
    serializer=CurrentUserPostsSerializer(instance=user,context={"request":request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListPostsForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated]
    queryset=Post.objects.all()
    pagination_class = CustomPaginator

    def get_queryset(self):
        username=self.request.query_params.get("username") or None
        
        queryset=Post.objects.all()
        
        if username is not None:
            return Post.objects.filter(author__username=username)

        return queryset
    
    @swagger_auto_schema(
        operation_summary="List all posts for an author (user)",
        operation_description="Returns a list of all posts for an author"
    )

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)