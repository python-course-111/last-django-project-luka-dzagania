"""
URL configuration for last django project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from main_app.views import index, about, contact, blog, register_request, login_request, catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about.html/', about, name='about'),
    path('contact.html/', contact, name='contact_view'),
    path('blog.html/', blog, name="view_contact_data"),
    path("register.html/", register_request, name="register"),
    path('login.html/', login_request, name="login_request"),
    path('catalog.html/', catalog, name='catalog'),
]
