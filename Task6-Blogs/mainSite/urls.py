"""
URL configuration for mainSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # a bunch of urls for the accounts app, we will be using the built-in auth views for login and logout
    # path('accounts/', include('django.contrib.auth.urls')), 
    path('', include('blog.urls'))
]

# this would be the main page for our studying for this project
# django does not have a regestiration page
# but it does have a login page and a logout page out-of-the-box
# for my deep study of forms and such here is some interesting facts
# i should probebly write this in notion of obsidian but oh well
# There is a normal form and a model form
# a normal form is just a form that you create yourself and it does not have any connection to a model
# a model form is a form that is connected to a model and it will automatically create the form fields based on the model fields
# cerf token, just saying
