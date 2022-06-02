from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

import uuid

# Create your models here.


CATEGORY = (
    ('Eletronics', 'Eletronics'),
    ('Food', 'Food'),
    ('Clothes', 'Clothes')
)

class User(models.Model):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    first_time_login = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255, null=True, unique=True)
    user_type = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    if_logged = models.BooleanField(default=False)
    password = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return "{}".format(self.username) 

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        user_id = 'US-{0}'.format(str(instance_id).zfill(3))
        instance.user_id = user_id
        instance.save()



class Product(models.Model):

    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=50, choices=CATEGORY, default='CharField')
    item_price = models.DecimalField(null=True,blank=True, max_digits=15, decimal_places=5, default=Decimal('000000.00'))
    available_quantity = models.IntegerField(null=True, blank=True)
   
    def __str__(self):
        return "{}".format(self.name) 

@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        product_id = 'PD-{0}'.format(str(instance_id).zfill(3))
        instance.product_id = product_id
        instance.save()


class Order(models.Model):

    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    product = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
       User, blank=True, null=True, on_delete=models.SET_NULL
    )
    order_id = models.CharField(max_length=30, blank=True, null=True)
   
    
   
    def __str__(self):
        return "{}".format(self.order_id) 


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        order_id = 'ORD-{0}'.format(str(instance_id).zfill(3))
        instance.order_id = order_id
        instance.save()