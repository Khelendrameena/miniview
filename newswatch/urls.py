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
from django.conf.urls import handler500

handler500 = 'app.views.custom_500_error'
urlpatterns = [
    path('admin/6302a139-d03a-11ef-8903-5d0b6fd2483d', admin.site.urls),

    path('', include('app.urls')),  # ✅ ONLY THIS

    path('auth/login/', google_login, name='google_login'),
    path('auth/callback/', google_callback, name='google_callback'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
