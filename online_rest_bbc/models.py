from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True) # URL uchun qulay nom

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

# 1. Mahsulotlar modeli
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # Mahsulot haqida ma'lumot
    price = models.DecimalField(max_digits=10, decimal_places=2)
    countInStock = models.IntegerField(default=0) # Omboradagi soni
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# 2. Buyurtma (asosiy qismi)
class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Kutilmoqda'), ('completed', 'Tugallangan')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # Yangi maydonlar:
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    PAYMENT_METHODS = [
        ('cash', 'Naqd pul orqali'),
        ('card', 'Online (Payme/Click)'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    is_paid = models.BooleanField(default=False)

    payment_method = models.CharField(max_length=20, default='cash') # Yangi qo'shildi
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)


# 3. Buyurtma ichidagi mahsulotlar (OrderItem)
# Bu model Order va Product o'rtasidagi ko'pga-ko'p bog'liqlikni ta'minlaydi
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"