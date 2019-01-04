# Django Imports
from django.conf.urls import url, include

# Project Imports
from .views import (
    activate, UserDetailsView, LoginView, BuyerRegistrationView, SellerRegistrationView
)

urlpatterns = [
    url(r'^accounts/login/$', LoginView.as_view()),
    url(r'^accounts/registration/buyer/$', BuyerRegistrationView.as_view()),
    url(r'^accounts/registration/seller/$', SellerRegistrationView.as_view()),
    url(r'^accounts/user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^accounts/login/$', LoginView.as_view()),

]
