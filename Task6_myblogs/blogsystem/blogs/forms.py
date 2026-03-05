from django import forms
from .models import blog
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class productForm(forms.ModelForm):
    class Meta:
        model = blog
        fields = "__all__"

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=[False])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
