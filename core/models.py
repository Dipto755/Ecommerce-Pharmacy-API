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
        StatusChoices, 
        RoleChoices, 
        ProductStockChoices, 
        ProductStatusChoices,
        OrderStatusChoices,
        OrderCreateChoices,
        ReviewStatusChoices
    )
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from = 'username', unique=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.CHOICES, blank=True)
    address = models.CharField(max_length=255, blank=True)
    thana = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True)
    image = VersatileImageField('Image', upload_to='images/user/', blank=True,)
    status = models.CharField(max_length=10, choices=StatusChoices.CHOICES, default=StatusChoices.Active)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email

    
class UserOrganization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=RoleChoices.CHOICES, blank=True)
    status = models.CharField(choices=StatusChoices.CHOICES, default=StatusChoices.Active)
    date_joined = models.DateField(default=timezone.now)
    salary = models.FloatField()
      
    def __str__(self):
        return self.user.username +  " " + self.role
    
def generate_slug(instance):
    return f"{instance.brand}-{instance.name}".lower()

class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    manufacturing_date = models.DateField()
    expired_date = models.DateField()
    price = models.FloatField()
    image = VersatileImageField('Image', upload_to='images/product/', blank=True)
    availability = models.CharField(max_length=20, choices=ProductStockChoices.CHOICES, default=ProductStockChoices.InStock)
    avg_rating = models.FloatField(default=0, blank=True)
    brand = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=ProductStatusChoices.CHOICES, default=ProductStatusChoices.Published)
    category = models.ManyToManyField(Category, through='ProductCategory')
    slug = AutoSlugField(
        populate_from=generate_slug,
        unique=True
    )
    review = models.ManyToManyField('Review', through='ProductReview', related_name='review')

    def __str__(self):
        return self.name
    
    
class ProductCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.category.name}"

class Cart(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from = 'uid', unique=True)
    
    def __str__(self):
        return f"{self.user.username} - cart"
    
class CartItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', blank=True, null=True)
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Product name - {self.product.name}"
    
class Order(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    added_on = models.DateField(default=timezone.now)
    delivery_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=OrderStatusChoices.CHOICES, default=OrderCreateChoices.New)
    review_status = models.CharField(max_length=30, choices=ReviewStatusChoices.CHOICES, default=ReviewStatusChoices.NotReviewed)
    
    def __str__(self):
        return f"{self.user.username} - order"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.delivery_date = self.calculate_delivery_date()
            
        if self.status == OrderStatusChoices.Delivered:
            self.delivery_date = timezone.now().date()
            
        super().save(*args, **kwargs)

    def calculate_delivery_date(self):
        return timezone.now().date() + timedelta(days=5)
    
class OrderItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.IntegerField(default=0)
    review_status = models.CharField(max_length=20, choices=ReviewStatusChoices.CHOICES, default=ReviewStatusChoices.NotReviewed)
    
    def __str__(self):
        return f"Product name - {self.product.name}"


class Review(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i ,i) for i in range(1, 6)], blank=True)
    comment = models.TextField(blank=True)
    image = VersatileImageField('Image', upload_to='images/reviews', blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from = 'uid', unique=True)
    
    def __str__(self):
        return f"{self.user.username} - review"
    
    
class ProductReview(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='product_reviews')
    added_on = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        prod = Product.objects.get(pk = self.product.pk)
        super().save(*args, **kwargs)
        prod.avg_rating = self.calculate_avg_rating()
        prod.save()
        
        
    def calculate_avg_rating(self):
        reviews = ProductReview.objects.filter(product=self.product.pk)
        if reviews.count() == 0:
            return 0
        
        avg = sum(review.review.rating for review in reviews) / reviews.count()
        return round(avg, 2)
