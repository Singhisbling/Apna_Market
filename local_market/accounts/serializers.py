# -*- coding: utf-8 -*-

# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer
from rest_framework import exceptions, serializers
from rest_framework.exceptions import AuthenticationFailed

# Project Imports

from .models import User, Seller, Buyer
from .validate import validate_email_password

# Get the UserModel
UserModel = get_user_model()


class CustomTokenSerializer(TokenSerializer):
    """
    Serializer for Token model.
    """
    class Meta:
        model = TokenModel
        fields = ('key', 'user')


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = (
            'pk', 'email',
            'user_type',
        )
        read_only_fields = ('email', )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        if email and password:
            user = authenticate(email=email, password=password)
            if not User.objects.get(email=email).is_active:
                data = {
                    "message": "This account is inactive. Please activate "
                               "your account using the verification link sent "
                               "over to your email.",
                    "success": "false"
                }
                raise AuthenticationFailed(data)
        else:
            data = {
                "message": 'Must include "email" and "password".',
                "success": "false"
            }
            raise AuthenticationFailed(data)

        return user

    def validate(self, attrs):
        user = None
        user_obj = None
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user_obj = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            pass

        if user_obj:
            user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            data = {
                "message": "Unable to log in with provided credentials.",
                "success": "false"
            }
            raise AuthenticationFailed(data)

        attrs['user'] = user
        return attrs


class BuyerRegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for User Registration
    """
    password1 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = Buyer
        fields = (
            'first_name',
            'last_name', 'profile_pic', 'phone_number', 'password1', 'password2',
        )

    def create(self, validated_data):
        # Check if the two password fields & email are valid
        validate_email_password(validated_data)
        user = User.objects.create_user(email=validated_data.get('email', ''),
                            user_type="buyer",
                            password=validated_data.get('password1', ''),
                            )
        user_qs = Buyer.objects.create(
            user=user,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            profile_pic=validated_data.get('profile_pic', ''),
        )
        user = authenticate(
            email=validated_data.get('email', ''),
            password=validated_data.get('password1', '')
        )
        token, created = TokenModel.objects.get_or_create(user=user)
        user_qs.is_active = False
        user_qs.save()
        data = {
            "user": {
                "id": user_qs.pk,
                "email": validated_data.get('email', '')
            },
            "access_token": token.key,
            "authenticate_user": user,
            "success": True
        }
        return data


class SellerRegistrationSerializer(serializers.ModelSerializer):
    """
    serializer for User Registration
    """
    password1 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = Seller
        exclude = ('account_verified', 'user')

    def create(self, validated_data):
        # Check if the two password fields & email are valid
        validate_email_password(validated_data)
        user = User.objects.create_user(email=validated_data.get('email', ''),
                                        user_type="seller",
                                        password=validated_data.get('password1', ''),
                                        )
        user_qs = Seller.objects.create(
            user=user,
            shop_owner_first_name=validated_data.get('shop_owner_first_name', ''),
            shop_owner_last_name=validated_data.get('shop_owner_last_name', ''),
            shop_owner_phone_number=validated_data.get('shop_owner_phone_number', ''),
            shop_owner_profile_pic=validated_data.get('shop_owner_profile_pic', ''),
            shop_type=validated_data.get('shop_type', ''),
            shop_name=validated_data.get('shop_name', ''),
            shop_number=validated_data.get('shop_number', ''),

        )
        user = authenticate(
            email=validated_data.get('email', ''),
            password=validated_data.get('password1', '')
        )
        token, created = TokenModel.objects.get_or_create(user=user)
        user_qs.is_active = False
        user_qs.save()
        data = {
            "user": {
                "id": user_qs.pk,
                "email": validated_data.get('email', '')
            },
            "access_token": token.key,
            "authenticate_user": user,
            "success": True
        }
        return data
