"""
URL configuration for newswatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('@<str:username>/', include('app.urls')),
    path('@<str:username>/vlog', include('app.urls')),
    path('@<str:username>/vlog/publish', include('app.urls')),
    path('accounts/', include('allauth.urls')),
    path('view', include('app.urls')),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('app/@<str:username_2>/follow', include('app.urls')),
    path('vlog/show/<str:vlog_id>', include('app.urls')),
    path('vlog/<str:vlog_id>', include('app.urls')),
    path('login/auth', include('app.urls')),
    path('signup', include('app.urls')),
    path('signup/auth', include('app.urls')),
    path('otp/verify', include('app.urls')),
    path('@<str:username>/edit', include('app.urls')),
    path('profile/edited', include('app.urls')),
    path('otp', include('app.urls')),
    path('search', include('app.urls')),
    path('search/quary', include('app.urls')),
    path('coment', include('app.urls')),
    path('coment/add', include('app.urls')),
    path('coment/count', include('app.urls'))
]
