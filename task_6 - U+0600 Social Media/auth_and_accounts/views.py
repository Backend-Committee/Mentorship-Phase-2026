from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data['password1']
            )
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()

    return render(request, "auth_and_accounts/register.html", {"form": form})
