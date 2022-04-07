"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', app.views.login, name='login'), # think both lines needed for redirect 
    path('', app.views.login, name='login'),
    path('register', app.views.register, name='register'),
    path('homepage', app.views.homepage, name='homepage'),
    path('index', app.views.index, name='index'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('myCalculators/<str:id>',app.views.myCalculators, name='myCalculators'),
    path('myCalculators/editAvailability/<str:id>',app.views.editAvailability, name='editAvailability'),
    path('hot', app.views.hot, name='hot'),
    path('myCalculators/<str:id>/addCalculator', app.views.addCalculator, name='addCalculator'),
    path('findCalculators', app.views.findCalculators, name='findCalculators'),
    path('findCalculators_time', app.views.findCalculators_time, name='findCalculators_time'),
    path('findCalculators_location', app.views.findCalculators_location, name='findCalculators_location'),
    path('findCalculators_type', app.views.findCalculators_type, name='findCalculators_type'),
    path('findCalculators_time_loc', app.views.findCalculators_time_loc, name='findCalculators_time_loc'),
    path('findCalculators_time_type', app.views.findCalculators_time_type, name='findCalculators_time_type'),
    path('findCalculators_loc_type', app.views.findCalculators_loc_type, name='findCalculators_loc_type'),
    path('findCalculators_all', app.views.findCalculators_all, name='findCalculators_all'),
    path('logout/',  app.views.logout, name = 'logout')
]
