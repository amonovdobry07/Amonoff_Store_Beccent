from rest_framework import serializers
from .models import Product, Order, OrderItem, Category
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        # Hamma maydonlarni ko'rsatish uchun '__all__' yoki ro'yxat:
        fields = ['id', 'name', 'description', 'price', 'countInStock', 'image', 'category', 'category_name', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name') # Reactda ko'rish oson bo'lishi uchun

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity']

# online_rest_bbc/serializers.py

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        # 'total_price' ni ro'yxatga qo'shdik:
        fields = ['id', 'user', 'created_at', 'status', 'items', 'total_price', 'phone_number', 'address', 'payment_method' ]

    def get_total_price(self, obj):
        # Buyurtma ichidagi barcha mahsulotlar narxini hisoblash
        total = sum(item.product.price * item.quantity for item in obj.items.all())
        return total

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
    
        for item_data in items_data:
            item = OrderItem.objects.create(order=order, **item_data)
        
        # Mahsulot omboridagi sonini kamaytiramiz
            product = item.product
            if product.countInStock >= item.quantity:
                product.countInStock -= item.quantity
                product.save()
            else:
            # Agar mahsulot yetarli bo'lmasa xato qaytaramiz
                raise serializers.ValidationError(f"{product.name} omborda yetarli emas!")
            
        return order


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Parol faqat yozish uchun, qaytib chiqmaydi

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Foydalanuvchini parolini shifrlab yaratish
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user