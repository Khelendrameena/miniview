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
from app.views import google_login, google_callback
from django.conf.urls.static import static
from django.conf import settings
#from django.conf.urls import handler500

#handler500 = 'myapp.views.custom_500_error'

urlpatterns = [
    path('admin/6302a139-d03a-11ef-8903-5d0b6fd2483d', admin.site.urls),
    path('', include('app.urls')),
    path('Blog_@_mini_view_426/Meena@426/<str:vlog_id>/<str:thumbnail>/<str:title>/<str:description>/<str:user>/<str:content_html>/<str:vlog_labels>/<str:vlog_rate>', include('app.urls')),
    path('@<str:username>/', include('app.urls')),
    path('@<str:username>/vlog', include('app.urls')),
    path('@<str:username>/vlog/publish', include('app.urls')),
    path('view', include('app.urls')),
    path('auth/login/', google_login, name='google_login'),
    path('auth/callback/', google_callback, name='google_callback'),
    path("login/", include('app.urls')),
    path('app/@<str:username_2>/follow', include('app.urls')),
    path('top/<str:para>', include('app.urls')),
    path('robots.txt',include('app.urls')),
    path('app/view/name/', include('app.urls')),
    path('about',include('app.urls')),
    path('vlog/show/<str:vlog_id>', include('app.urls')),
    path('vlog/internal/<int:index>', include('app.urls')),
    path('vlog/<str:vlog_id>', include('app.urls')),
    path('6302a139-d03a-11ef-8903-5d0b6fd2483d.xml',include('app.urls')),
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
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
