from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
# flashes a message to the user, we will be using this to show a message when the user logs in or logs out
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm


# python classes should be PascalCase, 
class login_user(View):
    def get(self,request):
        return render(request, 'login.html',{})
    def post(self, request):
        username = request.POST.get('username');
        password = request.POST.get('password');
        user = authenticate(request, username = username, password = password);
        if user is not None:
            login(request, user)
            return redirect('blog:home')
        else:
            messages.error(request, "Invalid username or password.")
            # here you should render insteaed of redirecting, redirecting accumelated error messages
            return render(request, 'login.html',{messages: messages.get_messages(request)})

# you should only be able to log out with post request, this is a security measure to prevent CSRF attacks
class logout_user(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('blog:home')

class register_user(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'register.html',{'form':form})
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # the first password field is password1
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('blog:home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            return render(request, 'register.html', {'form': form})
        