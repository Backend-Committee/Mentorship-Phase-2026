from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from .forms import ProfileCreationForm

def register(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)

        if form.is_valid():
            logout(request)
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = ProfileCreationForm()

    return render(request, "auth_and_accounts/register.html", {"form": form})
