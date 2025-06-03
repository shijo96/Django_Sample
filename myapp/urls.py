"""
URL configuration for Django_Sample_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
    path('login',views.login,name='login'),
    path('user_view_profile',views.user_view_profile,name='user_view_profile'),
    path('edit_profile/<id>',views.edit_profile,name='edit_profile'),


    path('admin_view_customer', views.admin_view_customer, name='admin_view_customer'),
    path('logout_user', views.logout_user, name='logout_user'),
]
