from rest_framework import viewsets, permissions
from .models import Product, Order, Category
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer

from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Mahsulotlar uchun ViewSet
# views.py
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
    # self.queryset o'rniga modeldan foydalanish xavfsizroq
        queryset = Product.objects.all() 
        category = self.request.query_params.get('category')
    
    # 'all' bo'lmagan va bo'sh bo'lmagan holatni tekshirish
        if category and category != 'all':
            queryset = queryset.filter(category_id=category)
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# Buyurtmalar uchun ViewSet
# views.py
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # AGAR ADMIN BO'LSA - HAMMASINI KO'RADI, AKS HOLDA FAQA O'ZINIKINI
        if self.request.user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })
    


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Hamma ro'yxatdan o'ta oladi
    serializer_class = RegisterSerializer # Mana shu qator HTML formani chizib beradi