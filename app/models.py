from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CUSTOMER = "customer"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_ADMIN, "Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    default_location_text = models.TextField(blank=True, null=True)
    default_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    default_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return self.username
    



class TimestampModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Creation Date/Time", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Update Date/Time", auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


        

class Category(TimestampModel):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Unit(TimestampModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Option(TimestampModel):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='options')



    def __str__(self):
        return self.name

class Product(TimestampModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_quantity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def reduce_stock(self, quantity):
        if self.available_quantity >= quantity:
            self.available_quantity -= quantity
            self.save()
        else:
            raise ValueError("Requested quantity exceeds available stock")
    



class Order(TimestampModel):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (IN_PROGRESS, "In Progress"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    contact_name = models.CharField(max_length=200,  null=True, blank=True)
    contact_phone = models.CharField(max_length=30, null=True, blank=True)
    location_text = models.TextField( null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Order #{self.id} - {self.contact_phone}"

    def restore_stock(self):
        """Return stock to products if this order is cancelled"""
        for item in self.items.all():
            product = item.product
            product.available_quantity += item.quantity
            product.save()

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    #so when the actual price changes, the order price is recorded in the previous orders
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price_at_order:
            self.price_at_order = self.product.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.quantity * self.price_at_order
    
