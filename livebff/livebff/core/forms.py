from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(input_formats=['%m/%d/%Y'], required=True)
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'full_name', 'password1', 'password2')
