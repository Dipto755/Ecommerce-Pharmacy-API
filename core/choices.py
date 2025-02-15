from django.db.models import TextChoices


class GenderChoices(TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"

    # CHOICES = [
    #     (Male, 'Male'),
    #     (Female, 'Female'),
    #     (Other, 'Other'),
    # ]


class StatusChoices(TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    REMOVED = "REMOVED", "Removed"

    # CHOICES = [
    #     (ACTIVE, 'Active'),
    #     (INACTIVE, 'Inactive'),
    #     (REMOVED, 'Removed'),
    # ]


class RoleChoices(TextChoices):
    OWNER = "OWNER", "Owner"
    ADMIN = "ADMIN", "Admin"
    MANAGER = "MANAGER", "Manager"
    STAFF = "STAFF", "Staff"

    # CHOICES = [
    #     (OWNER, 'Owner'),
    #     (ADMIN, 'Admin'),
    #     (MANAGER, 'Manager'),
    #     (STAFF, 'Staff'),
    # ]


# class OwnerRoleChoices:
#     Admin = 'admin'
#     Manager = 'manager'
#     Staff = 'staff'

#     CHOICES = [
#         (Admin, 'Admin'),
#         (Manager, 'Manager'),
#         (Staff, 'Staff'),
#     ]

# class AdminRoleChoices:
#     Manager = 'manager'
#     Staff = 'staff'

#     CHOICES = [
#         (Manager, 'Manager'),
#         (Staff, 'Staff'),
#     ]

# class ManagerRoleChoices:
#     Staff = 'staff'

#     CHOICES = [
#         (Staff, 'Staff'),
#     ]


class ProductStockChoices(TextChoices):
    IN_STOCK = "IN_STOCK", "In Stock"
    OUT_OF_STOCK = "OUT_OF_STOCK", "Out of Stock"

    # CHOICES = [
    #     (INSTOCK, 'In Stock'),
    #     (OUTOFSTOCK, 'Out of Stock'),
    # ]


class ProductStatusChoices(TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    REMOVED = "REMOVED", "Removed"

    # CHOICES = [
    #     (DRAFT, 'Draft'),
    #     (PUBLISHED, 'Published'),
    #     (REMOVED, 'Removed')
    # ]


class OrderCreateChoices(TextChoices):
    NEW = "NEW", "New"

    # CHOICES = [
    #     (NEW, 'New'),
    # ]


class OrderStatusChoices(TextChoices):
    PROCESSING = "PROCESSING", "Processing"
    SHIPPED = "SHIPPED", "Shipped"
    DELIVERED = "DELIVERED", "Delivered"

    # CHOICES = [
    #     (PROCESSING, 'Processing'),
    #     (SHIPPED, 'Shipped'),
    #     (DELIVERED, 'Delivered'),
    # ]


class ReviewStatusChoices(TextChoices):
    REVIEWED = "REVIEWED", "Reviewed"
    NOT_REVIEWED = "NOT_REVIEWED", "Not Reviewed"

    # CHOICES = [
    #     (REVIEWED, 'Reviewed'),
    #     (NOTREVIEWED, 'Not Reviewed'),
    # ]


class ReviewStatusForOrderChoices(TextChoices):
    REVIEWED = "REVIEWED", "Reviewed"
    PARTIALLY_REVIEWED = "PARTIALLY_REVIEWED", "Partially Reviewed"
    NOT_REVIEWED = "NOT_REVIEWED", "Not Reviewed"

    # CHOICES = [
    #     (REVIEWED, 'Reviewed'),
    #     (PARTIALLYREVIEWED, 'Partially Reviewed'),
    #     (NOTREVIEWED, 'Not Reviewed'),
    # ]
