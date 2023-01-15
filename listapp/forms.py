from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    c_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'c_password', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput()
        }

