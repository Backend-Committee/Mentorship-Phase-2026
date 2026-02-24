from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.


class login_view(LoginView):
    template_name = 'Auth/login.html'
    next_page = 'index'

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('Accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'Auth/register.html', {'form': form})