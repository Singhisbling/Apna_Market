# Django Imports
from django.conf.urls import url, include

# Project Imports
from .views import (
    activate, CustomUserDetailsView, LoginView, UserRegistrationView
)

urlpatterns = [
    url(r'^auth/login/$', LoginView.as_view()),
    url(r'^auth/registration/$', UserRegistrationView.as_view()),
    url(r'^auth/user/$', CustomUserDetailsView.as_view(),
        name='rest_user_details'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url(r'^password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
