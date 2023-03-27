from rest_framework import serializers
from .models import Categories,Products,Carts,Orders,Contact
from django.contrib.auth.models import User
from django.core.mail import send_mail

class UserSerializerr(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Categories
        fields=[
            "id",
            "category_name",
            "is_active",

        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields="__all__"

class CartSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    created_date=serializers.DateField(read_only=True)
    status=serializers.CharField(read_only=True)
    qty=serializers.IntegerField(read_only=True)
    class Meta:
        model=Carts
        fields=[
            "user",
            "product",
            "qty",
            "created_date",
            "status",
            "qty"
        ]
    def create(self,validated_date):
        user=self.context.get("user")
        product=self.context.get("product")
        qty=self.context.get("qty")
        return Carts.objects.create(user=user,product_id=product,qty=qty)

class OrderSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    date=serializers.DateField(read_only=True)
    status=serializers.CharField(read_only=True)
    expected_delivery_date=serializers.DateField(read_only=True)
    class Meta:
        model=Orders
        fields=[
            "user",
            "product",
            "date",
            "status",
            "expected_delivery_date",
            "deliver_address"
        ]
    def create(self,validated_date):
        user=self.context.get("user")
        qs=User.objects.get(id=user.id)
        email=qs.email
        send_mail(
            "Employee:Employee Portal",
            f"Your order is placed.........",
            "remyatestwork@gmail.com",
            [email]
        )
        product=self.context.get("product")
        return Orders.objects.create(**validated_date,user=user,product=product)

class ContactSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Contact
        fields="__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        return Contact.objects.create(**validated_data,user=user)
