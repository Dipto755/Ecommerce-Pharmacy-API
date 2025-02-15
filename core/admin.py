from django.contrib import admin

from .models import (
    User,
    UserOrganization,
    Organization,
    Category,
    Product,
    ProductCategory,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    ProductReview,
    MediaRoom,
    MediaRoomConnector
)

#Just to test github push!!
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["username", "first_name", "last_name", "status"]

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    ordering=["id"]
    list_display = ["name", "email", "phone"]

@admin.register(UserOrganization)
class UserOrganizationAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["user", "organization", "role", "status"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["name", "description"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["name", "organization", "stock", "expiry_date", "price"]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["product", "category", "added_on"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["get_username", "added_on"]

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "username"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["get_cart_uid", "get_product_name", "quantity"]

    def get_cart_uid(self, obj):
        return obj.cart.uid

    get_cart_uid.short_description = "cart_uid"

    def get_product_name(self, obj):
        return obj.product.name

    get_product_name.short_description = "product_name"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "get_username",
        "added_on",
        "delivery_date",
        "status",
        "review_status",
    ]

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "username"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["get_order_uid", "get_product_name", "quantity"]

    def get_order_uid(self, obj):
        return obj.order.uid

    get_order_uid.short_description = "order_uid"

    def get_product_name(self, obj):
        return obj.product.name

    get_product_name.short_description = "product_name"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["get_username", "get_order_uid", "added_on"]

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "username"

    def get_order_uid(self, obj):
        return obj.order.uid

    get_order_uid.short_description = "order_uid"



@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["get_product_name", "added_on"]

    def get_product_name(self, obj):
        return obj.product.name

    get_product_name.short_description = "product_name"
    
@admin.register(MediaRoom)
class MediaRoomAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['file']
    
    
@admin.register(MediaRoomConnector)
class MediaRoomConnectorAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['get_media_name']
    
    def get_media_name(self, obj):
        return obj.mediaroom.file
    get_media_name.short_description = "media_name"
