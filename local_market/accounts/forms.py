from django import forms
from .models import User
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from custom_user.forms import EmailUserCreationForm


class UserCreateAdminForm(EmailUserCreationForm):
    """
    Solr format rule custom validation
    """
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        """
        To avoid invalid creation of solr format rule
        """
        super(UserCreateAdminForm, self).clean()
        cleaned_data = self.cleaned_data
        user_type = cleaned_data.get('user_type')
        shop_type = cleaned_data.get('shop_type')
        if user_type == 'seller':
            if not shop_type:
                self._errors['shop_type'] = ErrorList([mark_safe(
                        'if the user is seller then it has to select shop type')])
        return cleaned_data


class UserEditAdminForm(forms.ModelForm):
    """
    Solr format rule custom validation
    """
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        """
        To avoid invalid creation of solr format rule
        """
        super(UserEditAdminForm, self).clean()
        cleaned_data = self.cleaned_data
        user_type = cleaned_data.get('user_type')
        shop_type = cleaned_data.get('shop_type')
        if not cleaned_data.get('id'):
            if user_type == 'seller':
                if not shop_type:
                    self._errors['shop_type'] = ErrorList([mark_safe(
                            'if the user is seller then it has to select shop type')])
            return cleaned_data
