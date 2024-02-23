from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Item_ordered

@receiver(post_save, sender=Item_ordered)
def update_save(sender, instance, created, **kwargs):
    """Amend order total with item creation or update """

    instance.order.order_total_update()

@receiver(post_delete, sender=Item_ordered)
def update_save(sender, instance, **kwargs):
    """Amend order total when item deleted """
    
    instance.order.order_total_update()