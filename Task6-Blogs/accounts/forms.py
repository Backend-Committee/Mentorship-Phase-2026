from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model= User
        fields = ('username', 'email', 'password1', 'password2')
        # widgets={
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     # these two won't work, we have to override the default widgets
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }
        
    # this is better than the meta approach because it will work even if we change the fields in the future
    def __init__(self,*args,**kwargs):
        super(RegisterUserForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['username'].widget.attrs['autofocus'] = True
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        
        for field in self.fields.values():
            field.help_text = None
            field.error_messages = {'required': 'This field is required.'}
            field.widget.attrs['class'] = 'form-control'
            field.label = ''