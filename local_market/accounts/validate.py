from rest_framework.exceptions import AuthenticationFailed
from .models import User


def validate_email_password(data):
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