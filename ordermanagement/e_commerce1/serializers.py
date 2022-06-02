from django.contrib.auth.models import User, Group
from rest_framework.serializers import (
    SerializerMethodField,
)
from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User,Product,Order
from django.core.exceptions import ValidationError
from uuid import uuid4
import logging
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=50)
    # User.objects.create()
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'user_type'
        )


class LoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        if not user_id and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in user_id:
            user = User.objects.filter(
                Q(email=user_id) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=user_id)
        else:
            user = User.objects.filter(
                Q(username=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(username=user_id)
        if user.if_logged:
            raise ValidationError("User already logged in.")
        user.if_logged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'user_id',
            'password',
            'token'

        )

        read_only_fields = (
            'token',
        )


class LogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.if_logged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.if_logged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    user = SerializerMethodField(read_only=True)
    product = SerializerMethodField(read_only=True)
    
    def get_user(self, obj):
        try:
            if obj.user:
                user_dict = {
                    "id": obj.user.id,
                    "name": obj.user.username,
                }
                return user_dict
            return None
        except Exception as exception:
            logger.exception(
                "Getting Exception while Fetching Risk Category as %s", exception
            )
            return None

    def get_product(self, obj):
        try:
            if obj.product:
                products_list = obj.product.all()
        
                product_dict = [{
                    "id": items.id,
                    "product_name": items.name} for items in products_list]
                return product_dict
            return None
        except Exception as exception:
            logger.exception(
                "Getting Exception while Fetching Risk Category as %s", exception
            )
            return None

    class Meta:
        model = Order
        fields =  ["id","object_id","order_id","product","user"]
