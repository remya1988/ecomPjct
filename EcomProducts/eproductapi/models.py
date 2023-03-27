from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

class Products(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="images",null=True)
    price=models.PositiveIntegerField()
    description=models.CharField(max_length=250,null=True)
    offer_discount=models.CharField(max_length=200,null=True)
    available_number=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product_name

class Carts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True,null=True)
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=120,choices=options,default="in-cart")
    qty=models.PositiveIntegerField(default=1)


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True)
    options = (
        ("order-placed", "order-placed"),
        ("dispatched", "dispatched"),
        ("intransit", "intransit"),
        ("delivered", "delivered"),
        ("cancelled", "cancelled")
    )
    status = models.CharField(max_length=120, choices=options, default="order-placed")
    deliver_address = models.CharField(max_length=250, null=True)
    expected_date=models.DateTimeField(null=True)

class Contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ph_no=models.CharField(max_length=12)
    contact_address=models.CharField(max_length=300)
