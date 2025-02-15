from django.contrib.auth.models import BaseUserManager
from django.db.models import Manager

from .choices import OrderStatusChoices, ProductStatusChoices, ProductStockChoices, ReviewStatusChoices, StatusChoices


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    
class ActivityStatusManager(Manager):
    def IS_ACTIVE(self):
        return self.filter(status=StatusChoices.ACTIVE)
    
    def IS_INACTIVE(self):
        return self.filter(status=StatusChoices.INACTIVE)
    
    def IS_REMOVED(self):
        return self.filter(status=StatusChoices.REMOVED)
    
    
class ProductStockChoicesManager(Manager):
    def IS_IN_STOCK(self):
        return self.filter(availability=ProductStockChoices.IN_STOCK)
    
    def IS_OUT_OF_STOCK(self):
        return self.filter(availability=ProductStockChoices.OUT_OF_STOCK)
    
    
class ProductStatusChoicesManager(Manager):
    def IS_DRAFT(self):
        return self.filter(status=ProductStatusChoices.DRAFT)
    
    def IS_PUBLISHED(self):
        return self.filter(status=ProductStatusChoices.PUBLISHED)
    
    def IS_REMOVED(self):
        return self.filter(status=ProductStatusChoices.REMOVED)
    

class OrderStatusChoiceManager(Manager):
    def IS_PROCESSING(self):
        return self.filter(status=OrderStatusChoices.PROCESSING)
    
    def IS_SHIPPED(self):
        return self.filter(status=OrderStatusChoices.SHIPPED)
    
    def IS_DELIVERED(self):
        return self.filter(status=OrderStatusChoices.DELIVERED)
    
    
class ReviewStatusChoiceManager(Manager):
    def IS_REVIEWED(self):
        return self.filter(review_status=ReviewStatusChoices.REVIEWED)
    
    def IS_NOT_REVIEWED(self):
        return self.filter(review_status=ReviewStatusChoices.NOT_REVIEWED)


class OrganizationManager(ActivityStatusManager):
    def IS_ACTIVE(self):
        return super().IS_ACTIVE()
    
    def IS_INACTIVE(self):
        return super().IS_INACTIVE()
    
    def IS_REMOVED(self):
        return super().IS_REMOVED()
    

class UserOrganizationManager(ActivityStatusManager):
    def IS_ACTIVE(self):
        return super().IS_ACTIVE()
    
    def IS_INACTIVE(self):
        return super().IS_INACTIVE()
    
    def IS_REMOVED(self):
        return super().IS_REMOVED()
    

class CategoryManager(ActivityStatusManager):
    def IS_ACTIVE(self):
        return super().IS_ACTIVE()
    
    def IS_INACTIVE(self):
        return super().IS_INACTIVE()
    
    def IS_REMOVED(self):
        return super().IS_REMOVED()


class ProductManager(ProductStatusChoicesManager, ProductStockChoicesManager):
    def IS_DRAFT(self):
        return super().IS_DRAFT()
    
    def IS_PUBLISHED(self):
        return super().IS_PUBLISHED()
    
    def IS_REMOVED(self):
        return super().IS_REMOVED()
    
    def IS_IN_STOCK(self):
        return super().IS_IN_STOCK()
    
    def IS_OUT_OF_STOCK(self):
        return super().IS_OUT_OF_STOCK()


class OrderManager(OrderStatusChoiceManager, ReviewStatusChoiceManager):
    def IS_PROCESSING(self):
        return super().IS_PROCESSING()
    
    def IS_SHIPPED(self):
        return super().IS_SHIPPED()
    
    def IS_DELIVERED(self):
        return super().IS_DELIVERED()
    
    def IS_REVIEWED(self):
        return super().IS_REVIEWED()
    
    def IS_NOT_REVIEWED(self):
        return super().IS_NOT_REVIEWED()
    

class OrderItemManager(OrderStatusChoiceManager, ReviewStatusChoiceManager):
    def IS_PROCESSING(self):
        return self.filter(delivery_status = OrderStatusChoices.PROCESSING)
    
    def IS_SHIPPED(self):
        return self.filter(delivery_status = OrderStatusChoices.SHIPPED)
    
    def IS_DELIVERED(self):
        return self.filter(delivery_status = OrderStatusChoices.DELIVERED)
    
    def IS_REVIEWED(self):
        return super().IS_REVIEWED()
    
    def IS_NOT_REVIEWED(self):
        return super().IS_NOT_REVIEWED()
