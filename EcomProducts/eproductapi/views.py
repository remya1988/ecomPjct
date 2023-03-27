from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Categories,Products,Carts,Orders,Contact
from .serializer import (CategorySerializer,UserSerializerr,ProductSerializer,CartSerializer,
                         OrderSerializer,ContactSerializer)
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import  generics
from .permissions import IsAdmin
from django.contrib.auth import authenticate,login,logout
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import authentication,permissions,status
import django_filters
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from django.db.models.fields import DateTimeField
from datetime import datetime, timedelta
from django.core.mail import send_mail
from  django.views.generic  import DetailView
# Create your views here.
class UserModelViewsetView(ModelViewSet):
    serializer_class = UserSerializerr
    queryset = User.objects.all()

class CategoryApiView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    search_fields = ['category_name']
    filter_backends = (SearchFilter,)
    queryset = Categories.objects.all()

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    class Meta:
        model = Products
        fields = ["product_name","price","category_id"]


class ProductListViewsetView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductRetrieveViewsetView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Products.objects.all()

class ProductViewForAdmin(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    permission_classes=[IsAdmin]
    serializer_class = ProductSerializer
    queryset = Products.objects.all()

class ListProductWithOfferandDiscounts(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        pdcts=Products.objects.filter(offer_discount__isnull=False)
        if pdcts:
            serializer=ProductSerializer(pdcts,many=True)
            return Response(serializer.data)
        else:
            return Response("No offers or discount for products")

class ProductAddCart(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        id = request.POST['product_id']
        product = Products.objects.get(id=id)
        user = request.user
        qty=request.POST['qty']
        serializer = CartSerializer(data=request.data, context={"user": user, "product": product.id,"qty":qty})

        if serializer.is_valid():
        #     print(serializer.data)
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def list(self, request, *args, **kwargs):
        user    = request.user
        cart=Carts.objects.filter(user=user,status="in-cart")
        serializer=CartSerializer(cart,many=True)
        return Response({"Product In Cart":"","Your cart items":serializer.data})

class CheckOut(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
            # id = request.POST['product_id']
            # product = Products.objects.get(id=id)
            id =request.POST['cart_id']
            cart=Carts.objects.get(id=id)
            product=Products.objects.get(id=cart.product_id)
            user = request.user
            user_tb=User.objects.get(id=user.id)
            if user_tb.is_superuser==1:
                return Response("You dont have access to this....")
            else:
                serializer = OrderSerializer(data=request.data, context={"user": user, "product": product})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Status":"Order placed","Order Details":serializer.data} )
                else:
                    return Response(data=serializer.errors)

class OrderDetailsViewByAdmin(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    permission_classes=[IsAdmin,]
    def post(self, request, *args, **kwargs):
        due_days = 5
        id=kwargs.get("pk")
        print(id)
        qs=Orders.objects.get(id=id)
        user=User.objects.get(id=qs.user_id)
        email=user.email
        due_date = datetime.now()+timedelta(days=due_days)
        qs.status=request.POST["status"]
        qs.expected_date=due_date
        qs.save()
        send_mail(
            "Employee:Employee Portal",
            f"Your order is Dispatched......... Expected delivery date is {due_date}",
            "remyapillai1988@gmail.com",
            [email]
        )
        return Response({"Email sent and expected delivery date is ":due_date})

class ContactDetailsView(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contact.objects.all()
    def create(self, request, *args, **kwargs):
        user=request.user
        serializer=ContactSerializer(data=request.data,context={"user": user} )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"Message":"Lgout successfully"})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)