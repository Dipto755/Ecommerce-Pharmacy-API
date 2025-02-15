from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserOrganization, Cart



@receiver(post_save, sender=User)
def update_userorganization_status_based_on_user_status(sender, instance, **kwargs):
    user_status = instance.status
    UserOrganization.objects.filter(user=instance).update(status = user_status)
    

@receiver(post_save, sender=User)
def create_cart_while_new_user_registers(sender, instance, **kwargs):
    if kwargs['created']:
        Cart.objects.create(user=instance)
        
