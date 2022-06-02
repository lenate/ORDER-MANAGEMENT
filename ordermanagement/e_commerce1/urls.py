from collections import UserList
from django import views
from django.urls import include, path
# from e_commerce1 import views
from . import views 
from .views import *

urlpatterns = [
    # login api and logout api
    path('login/', Login.as_view(), name="login"),
    path('logout/',Logout.as_view(), name="logout"),

    # users listing api
    path('listUser/', UsersList.as_view(), name="register"), 

    # product add,edit,list,delete API's
    path('product/add/', ProductAddView.as_view(), name="product/add/"),
    path('product/<str:object_id>/edit/', ProductEditView.as_view(), name="product/edit/"),
    path('product/listing/', ProductListView.as_view(), name="product_list"),
    path("product-delete/<str:object_id>/",views.ProductDestroyView.as_view(),name="product_delete"),

    # order add,edit,delete,list API's
    path('order/add/', OrderAddView.as_view(), name="order_create"),
    path('order/<str:object_id>/edit/', OrderEditView.as_view(), name="order_edit"),
    path('order-delete/<str:object_id>/', OrderDestroyView.as_view(), name="order_delete"),
    path('order/list/', OrderListView.as_view(), name="order_list"),


]