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

from .models import User

# Get the UserModel
UserModel = get_user_model()


class CustomTokenSerializer(TokenSerializer):
    """
    Serializer for Token model.
    """
    class Meta:
        model = TokenModel
        fields = ('key', 'user')


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = (
            'pk', 'email', 'shop_name',
            'first_name',
            'last_name', 'user_type', 'phone_number'
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


class UserRegistrationSerializer(serializers.ModelSerializer):
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
        model = User
        fields = (
            'pk', 'email', 'shop_name',
            'first_name',
            'last_name', 'user_type', 'shop_type', 'phone_number', 'password1', 'password2',
        )

    def validate_email_password(self, data):
        json_data = {"success": "false"}
        email_validation = None
        try:
            email_validation = User.objects.get(
                email__iexact=data['email']
            )
        except User.DoesNotExist:
            pass

        if data['password1'] != data['password2'] and email_validation:
            json_data.update(
                {
                    "message": "The two password fields didn't match & the "
                               "email field must be unique."
                }
            )
            raise AuthenticationFailed(json_data)
        elif data['password1'] != data['password2']:
            json_data.update(
                {
                    "message": "The two password fields didn't match."
                }
            )
            raise AuthenticationFailed(json_data)
        elif email_validation:
            json_data.update(
                {
                    "message": "The email field must be unique."
                }
            )
            raise AuthenticationFailed(json_data)

        return data

    def create(self, validated_data):
        # Check if the two password fields & email are valid
        self.validate_email_password(validated_data)
        if (validated_data.get('user_type') == 'seller' and validated_data.get('shop_type')) or validated_data.get('user_type') == 'buyer':
            user_qs = User.objects.create_user(
                email=validated_data.get('email', ''),
                password=validated_data.get('password1', ''),
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                phone_number=validated_data.get('phone_number', ''),
                user_type=validated_data.get('user_type', ''),
                shop_name=validated_data.get('shop_name', ''),
                shop_type=validated_data.get('shop_type', ''),
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
                    "id": user_qs.id,
                    "email": validated_data.get('email', '')
                },
                "access_token": token.key,
                "authenticate_user": user,
                "success": True
            }
            return data
        else:
            data = {
                "success": False
            }
            return data
