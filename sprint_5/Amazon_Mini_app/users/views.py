from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm, LoginForm


# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        if SignUpForm(request.POST).is_valid():
            SignUpForm(request.POST).save()
            return redirect('login')
    return render(request, 'users/sign_up.html', {'form': SignUpForm})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try :
                user = User.objects.get(username=username, password=password)

                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('product_list')
            except User.DoesNotExist:
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout(request):
    request.session.flush()
    return redirect('product_list')
