"""EcomProducts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from eproductapi.views import (UserModelViewsetView,CategoryApiView,ProductListViewsetView,LogoutView,
                               ProductViewForAdmin,ProductRetrieveViewsetView,
                               ListProductWithOfferandDiscounts,ProductAddCart,CheckOut,
                               OrderDetailsViewByAdmin,ContactDetailsView)
router =  DefaultRouter()

router.register("account/signup",UserModelViewsetView,basename="account")
router.register("storeapi/category",CategoryApiView,basename="cat")
router.register("storeapi/product",ProductViewForAdmin,basename="prod")
router.register("storeapi/pdt/add-to-cart",ProductAddCart,basename="cart")
router.register("storeapi/pdt/check-out",CheckOut,basename="checkout")
router.register("storeapi/user/contact",ContactDetailsView,basename="contact")
# router.register("storeapi/admin-view/order",OrderDetailsViewByAdmin,basename="order-list")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('storeapi/user/login', TokenObtainPairView.as_view(),name="login"),
    path('storeapi/user/product-list/', ProductListViewsetView.as_view(),name="list-products"),
    path('storeapi/user/product-retrieve/<int:pk>', ProductRetrieveViewsetView.as_view(),name="retrieve-products"),
    path('storeapi/user/product-offer/', ListProductWithOfferandDiscounts.as_view(),name="products-offer"),
    path('storeapi/user/token/refresh', TokenRefreshView.as_view()),
    path("storeapi/admin-view/order/<int:pk>",OrderDetailsViewByAdmin.as_view()),
    # path('storeapi/user/product/add-to-cart/<int:pk>', ProductCartandCheckout.as_view({"post":"add_to_cart"})),
    path('storeapi/user/logout', LogoutView.as_view(), name="logout"),
]+router.urls
