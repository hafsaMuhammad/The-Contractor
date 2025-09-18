from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import  Product, Order, OrderItem, Category, Unit, Option
from django.utils.html import format_html


User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role", "is_staff")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    @admin.display(description="Image")
    def get_image(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}"><img src="{0}" style=" width:40px; hieght: 40px;"></a>'.format(
                    obj.image.url
                )
            )
        else:
            return None
        
    list_display = ("name","get_image","category","unit","price_per_unit","available_quantity")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("contact_name","contact_phone","status", "user","created_at")
    inlines = [OrderItemInline]
    search_fields = ["contact_name"]
    list_filter = ("status",  "user", "contact_name", "created_at")
