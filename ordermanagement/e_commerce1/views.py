import logging

# Create your views here.
from django.contrib.auth.models import User
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User,Product
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateAPIView)
from .serializers import *
from .functions import gen_object_id

logger = logging.getLogger(__name__)

class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = LoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = LogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

class UsersList(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


# add product api
class ProductAddView(CreateAPIView):
    
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                project = serializer.save(object_id=gen_object_id(Product))
                data["status"] = "success"
                data["message"] = "created successfully"
                data["code"] = 201
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] = "something_went_wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


# edit product api
class ProductEditView(RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by("id").all()
    lookup_field = "object_id"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                project = serializer.save()   
                data["message"] = "updated successfully"
                data["status"] = "success"
                data['code'] = 200
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)

# list product api
class ProductListView(ListAPIView):

    serializer_class = ProductSerializer

    # overriding the method

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()
        queryset_list=Product.objects.all()

        return queryset_list

# delete product api
class ProductDestroyView(DestroyAPIView):
    """
    Product Delete API View
    """
    queryset = Product.objects.order_by("id").all()
    serializer_class = ProductSerializer

    lookup_field = "object_id"

    def perform_destroy(self, instance):
        data = {}
        try:
            object_id = self.kwargs.get("object_id")
            policy_obj = Product.objects.get(object_id=object_id)

            policy_obj.delete()
            data["status"] = True
            data["message"] = "deleted"
            data["code"] = 200

        except Exception as exception:
            logger.exception("Exception occuring while fetching Request %s", exception)
            data["message"] = "something_went_wrong"
            data["status"] = "failed"
            data["code"] = 500
        return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        http_code = data.pop("code", None)
        return Response(data=data, status=http_code)


# add order api
class OrderAddView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                user=self.request.data.get('user')
                usertype=User.objects.get(id=user)
                product_type=self.request.data.get('product')
                product=Product.objects.get(id=product_type)
                if usertype.user_type == 'Consumer':
                    serializer.save(object_id=gen_object_id(Order),
                    user=usertype,product=product)
                    data["status"] = "success"
                    data["message"] = "created successfully"
                    data["code"] = 201
                else:
                    data["message"] = "Not Consumer User"
                    data["status"] = "failed"
                    data["code"] = 422
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] = "something_went_wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)

# edit order api
class OrderEditView(RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.order_by("id").all()
    lookup_field = "object_id"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                user_id=self.request.data.get('user')
                usertype=User.objects.get(id=user_id)
                product_type=self.request.data.get('product')
                product=Product.objects.get(id=product_type)
                if usertype.user_type == 'Consumer':
                    serializer.save(object_id=gen_object_id(Order),
                    user=usertype,product=product)   
                    data["message"] = "updated successfully"
                    data["status"] = "success"
                    data['code'] = 200
                else:
                    data["message"] = "not consumer user"
                    data["status"] = "failed"
                    data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)

# list order api
class OrderListView(ListAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()
        queryset_list=Order.objects.all()

        return queryset_list

# delete order api
class OrderDestroyView(DestroyAPIView):
    """
    Order Delete API View
    """
    queryset = Order.objects.order_by("id").all()
    serializer_class = OrderSerializer
    lookup_field = "object_id"

    def perform_destroy(self, instance):
        data = {}
        try:
            # print("hi")
            object_id = self.kwargs.get("object_id")
            order_obj = Order.objects.get(object_id=object_id)
            # print(order_obj)

            order_obj.delete()
            data["status"] = True
            data["message"] = "deleted"
            data["code"] = 200

        except Exception as exception:
            logger.exception("Exception occuring while fetching Request %s", exception)
            data["message"] = "something_went_wrong"
            data["status"] = "failed"
            data["code"] = 500
        return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        http_code = data.pop("code", None)
        return Response(data=data, status=http_code)