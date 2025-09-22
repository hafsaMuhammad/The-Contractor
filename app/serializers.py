from dynamic_rest.serializers import DynamicModelSerializer, DynamicRelationField
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem, Category, Unit, Option

User = get_user_model()



class UserSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "full_name", "phone",
                  "default_location_text", "default_latitude", "default_longitude")
        read_only_fields = ("id",)



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role", "full_name", "phone")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        # ensure role default
        role = validated_data.get("role", User().role if hasattr(User(), "role") else "customer")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        if hasattr(user, "role"):
            user.role = role
        user.save()
        return user


class CategorySerializer(DynamicModelSerializer):

    class Meta:
        model = Category
        fields = ("id","name","created_at","updated_at")

class UnitSerializer(DynamicModelSerializer):

    class Meta:
        model = Unit
        fields = ("id","name","created_at","updated_at")

class OptionSerializer(DynamicModelSerializer):

    class Meta:
        model = Option
        fields = ("id","name", "price", "product","created_at","updated_at")


class ProductSerializer(DynamicModelSerializer):
    category =CategorySerializer(embed=True, read_only=True)
    unit = UnitSerializer(embed=True, read_only=True)
    

    class Meta:
        model = Product
        fields = ("id","name","category","unit","description","price_per_unit","available_quantity","created_at", "updated_at")
        read_only_fields = ("id","created_at")

class OrderItemSerializer(DynamicModelSerializer):
    product = ProductSerializer(embed=True, read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source="product")

    class Meta:
        model = OrderItem
        fields = ("id","product","product_id","quantity","price_at_order")
        read_only_fields = ("id","price_at_order")

class OrderSerializer(DynamicModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id","user","contact_name","contact_phone","location_text","latitude","longitude","note","status","created_at","updated_at","items")
        # read_only_fields = ("id","status","created_at","user")

    def create(self, validated_data):
        items_data = validated_data.pop("items", []) 
        request = self.context.get("request")
        user = request.user if (request and request.user and request.user.is_authenticated) else None

        # if user provided and fields are empty → copy from user defaults
        if user:
            if not validated_data.get("contact_name") and getattr(user, "full_name", None):
                validated_data["contact_name"] = user.full_name
            if not validated_data.get("contact_phone") and getattr(user, "phone", None):
                validated_data["contact_phone"] = user.phone
            if not validated_data.get("location_text") and getattr(user, "default_location_text", None):
                validated_data["location_text"] = user.default_location_text
            if not validated_data.get("latitude") and getattr(user, "default_latitude", None):
                validated_data["latitude"] = user.default_latitude
            if not validated_data.get("longitude") and getattr(user, "default_longitude", None):
                validated_data["longitude"] = user.default_longitude



        order = Order.objects.create(user=user, **validated_data)

        for it in items_data:
            prod = it.get("product") or it.get("product_id")
            qty = it.get("quantity", 1)
            price = prod.price_per_unit if prod and prod.price_per_unit else 0

            try:
                prod.reduce_stock(qty)
            except ValueError as e:
                raise serializers.ValidationError(str(e))

            OrderItem.objects.create(
                order=order,
                product=prod,
                quantity=qty,
                price_at_order=price
            )

        return order
    
    def update(self, instance, validated_data):
        new_status = validated_data.get("status", instance.status)
        if instance.status != "cancelled" and new_status == "cancelled":
            instance.restore_stock()

        return super().update(instance, validated_data)
