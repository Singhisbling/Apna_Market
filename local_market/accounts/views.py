# -*- coding: utf-8 -*-

# Python Imports
from __future__ import unicode_literals

# Django Imports
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters
from rest_auth.app_settings import JWTSerializer, create_token
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Project Imports
from .models import User
from .serializers import (
    CustomTokenSerializer, CustomUserDetailsSerializer, LoginSerializer,
    UserRegistrationSerializer
)
from .tokens import account_activation_token

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class CustomUserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return get_user_model().objects.none()


class UserRegistrationView(generics.CreateAPIView):
    """
    This API will be used to allow the users to SignUp for the WebApp.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args):
        new_user_serializer = UserRegistrationSerializer(data=request.data)
        if new_user_serializer.is_valid():
            new_user = new_user_serializer.create(request.data)
            response_data = new_user.get('success')
            if response_data:
                mail_subject = 'Activate your account'
                current_site = get_current_site(request)
                message = render_to_string(
                    'accounts/acc_active_email.html', {
                        'user': new_user.get('authenticate_user'),
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(
                            new_user.get('authenticate_user').pk
                        )),
                        'token': account_activation_token.make_token(
                            new_user.get('authenticate_user')
                        ),
                    }
                )
                email = EmailMultiAlternatives(
                    mail_subject, message, settings.DEFAULT_EMAIL_FROM,
                    to=[new_user.get('user').get('email')]
                )
                email.send()
                data = {
                    "success": "true",
                    "message": "Email confirmation has been sent. Please check"
                }
                return Response(
                    data, status=status.HTTP_201_CREATED
                )

            else:
                data = {
                    "message": "kindly select shop type",
                    "success": "false"
                }
                return Response(data)

        data = {
            "message": new_user_serializer.errors,
            "success": "false"
        }
        return Response(
            data, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def process_login(self):
        login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = CustomTokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(
                self.token_model, self.user, self.serializer
            )

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(
                instance=data,
                context={'request': self.request}
            )
        else:
            serializer = serializer_class(
                instance=self.token,
                context={'request': self.request}
            )

        uqs = User.objects.get(id=serializer.data.get('user'))
        data = {
            "success": "true",
            "user": {
                "id": uqs.id,
                "first_name": uqs.first_name,
                "last_name": uqs.last_name,
                "email": uqs.email
            },
            "access_token": serializer.data.get('key')
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data,
            context={'request': request}
        )
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Shop.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(
            'Thank you for your email confirmation. Now you can login to '
            'your account.'
        )
    else:
        return HttpResponse('Activation link is invalid!')
