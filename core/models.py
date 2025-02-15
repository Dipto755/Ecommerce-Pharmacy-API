import uuid

from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField


from .choices import (
    GenderChoices,
    OrderCreateChoices,
    OrderStatusChoices,
    ProductStatusChoices,
    ProductStockChoices,
    ReviewStatusChoices,
    RoleChoices,
    StatusChoices,
)
from .managers import (
    CategoryManager,
    OrderItemManager,
    OrderManager,
    OrganizationManager,
    ProductManager,
    UserManager,
    UserOrganizationManager,
)
from .utils import (
    generate_cart_item_slug,
    generate_cart_slug,
    generate_category_slug,
    generate_order_item_slug,
    generate_order_slug,
    generate_organization_slug,
    generate_product_category_slug,
    generate_product_slug,
    generate_user_organization_slug,
    generate_user_slug,
)


class MediaRoom(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    file = VersatileImageField(upload_to="images/", blank=True, null=True)


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_user_slug, unique=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices, blank=True)
    address = models.CharField(max_length=255, blank=True)
    thana = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True)
    image = VersatileImageField("Image", upload_to="images/user/", blank=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices, default=StatusChoices.ACTIVE
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email


class Organization(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_organization_slug, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = PhoneNumberField(blank=True)
    trade_license = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    thana = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True)
    logo = VersatileImageField("Image", upload_to="images/organization/", blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices, default=StatusChoices.ACTIVE
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    REQUIRED_FIELDS = ["name", "email", "trade_license"]
    objects = OrganizationManager()

    def __str__(self):
        return self.name


class UserOrganization(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_user_organization_slug, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(choices=RoleChoices, blank=True)
    status = models.CharField(choices=StatusChoices, default=StatusChoices.ACTIVE)
    salary = models.FloatField()
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    objects = UserOrganizationManager()
    
    def __str__(self):
        return self.user.username + " " + self.role


class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_category_slug, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=StatusChoices, default=StatusChoices.ACTIVE
    )
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_product_slug, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    price = models.FloatField()
    image = models.ManyToManyField(MediaRoom, through="MediaRoomConnector")
    stock = models.IntegerField(default=20)
    availability = models.CharField(
        max_length=20, choices=ProductStockChoices, default=ProductStockChoices.IN_STOCK
    )
    avg_rating = models.FloatField(default=0, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ProductStatusChoices,
        default=ProductStatusChoices.PUBLISHED,
    )
    category = models.ManyToManyField(Category, through="ProductCategory")
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    review = models.ManyToManyField(
        "Review", through="ProductReview", related_name="review"
    )
    
    objects = ProductManager()

    def __str__(self):
        return self.name


# class ProductOrganization(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     slug = AutoSlugField(populate_from = generate_product_organization_slug, unique=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     manufacturing_date = models.DateField()
#     expired_date = models.DateField()
#     price = models.FloatField()
#     image = models.ManyToManyField(MediaRoom, through="MediaRoomConnector")
#     availability = models.CharField(
#         max_length=20, choices=ProductStockChoices, default=ProductStockChoices.INSTOCK
#     )
#     stock = models.IntegerField(default=20)
#     avg_rating = models.FloatField(default=0, blank=True)
#     # brand = models.CharField(max_length=255)
#     status = models.CharField(
#         max_length=20,
#         choices=ProductStatusChoices,
#         default=ProductStatusChoices.PUBLISHED,
#     )
#     category = models.ManyToManyField(Category, through="ProductCategory")
#     date_joined = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True)
#     review = models.ManyToManyField(
#         "Review", through="ProductReview", related_name="review"
#     )

#     def __str__(self):
#         return f"{self.organization.name}-{self.product.name}"


class ProductCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_product_category_slug, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.category.name}"


class Cart(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_cart_slug, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - cart"


class CartItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_cart_item_slug, unique=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product name - {self.product.name}"


class Order(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_order_slug, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    added_on = models.DateField(default=timezone.now)
    delivery_date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=OrderStatusChoices, default=OrderCreateChoices.NEW
    )
    review_status = models.CharField(
        max_length=30,
        choices=ReviewStatusChoices,
        default=ReviewStatusChoices.NOT_REVIEWED,
    )
    
    objects = OrderManager()

    def __str__(self):
        return f"{self.user.username} - order"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.delivery_date = self.calculate_delivery_date()

        if self.status == OrderStatusChoices.DELIVERED:
            self.delivery_date = timezone.now().date()

        super().save(*args, **kwargs)

    def calculate_delivery_date(self):
        return timezone.now().date() + timedelta(days=5)


class OrderItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from=generate_order_item_slug, unique=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.IntegerField(default=0)
    delivery_status = models.CharField(
        max_length=20, choices=OrderStatusChoices, default=OrderCreateChoices.NEW
    )
    review_status = models.CharField(
        max_length=20,
        choices=ReviewStatusChoices,
        default=ReviewStatusChoices.NOT_REVIEWED,
    )
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = OrderItemManager()

    def __str__(self):
        return f"Product name - {self.product.name}"


class Review(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True)
    comment = models.TextField(blank=True)
    image = models.ManyToManyField(MediaRoom, through="MediaRoomConnector")
    added_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from="uid", unique=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - review"


class ProductReview(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="product_reviews"
    )
    added_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        prod = Product.objects.get(pk=self.product.pk)
        super().save(*args, **kwargs)
        prod.avg_rating = self.calculate_avg_rating()
        prod.save()

    def calculate_avg_rating(self):
        reviews = ProductReview.objects.filter(product=self.product.pk)
        if reviews.count() == 0:
            return 0

        avg = sum(review.review.rating for review in reviews) / reviews.count()
        return round(avg, 2)


class MediaRoomConnector(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mediaroom = models.ForeignKey(MediaRoom, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, related_name="product_image"
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
