from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from .models import  Product, Order, Category, Unit, Option
from .serializers import (
     ProductSerializer, OrderSerializer,
    RegisterSerializer, UserSerializer, CategorySerializer, UnitSerializer, OptionSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])  # or username
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response
    


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password") 

    user = authenticate(request, username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"detail": "Invalid credentials"}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()  # delete the token
    return Response({"detail": "Successfully logged out."})



class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class UserViewSet(DynamicModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(DynamicModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UnitViewSet(DynamicModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OptionViewSet(DynamicModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
 

class ProductViewSet(DynamicModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(DynamicModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer

    def get_permissions(self):
        # anyone can create an order (guest). reading list: admins see all, normal users see their own
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.request.user and self.request.user.is_authenticated:
            # admins get full access
            if getattr(self.request.user, "role", None) == "admin":
                return [permissions.IsAuthenticated()]
            # normal user: can view/update his own orders (we'll filter queryset)
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        # if admin -> return all
        if user and user.is_authenticated and getattr(user, "role", None) == "admin":
            return qs
        # if authenticated normal user -> only their orders
        if user and user.is_authenticated:
            return qs.filter(user=user)
        # unauthenticated -> no list (or you can return all pending guest orders if you want)
        return qs.none()




