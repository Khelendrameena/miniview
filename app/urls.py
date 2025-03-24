from django.urls import path
from .import views

urlpatterns = [
path('', views.home, name='home_page'),
path('login', views.login_view, name='login'),
path('about',views.about,name='about page'),
path('6302a139-d03a-11ef-8903-5d0b6fd2483d.xml',views.custom_sitemap,name='sitemap xml'),
path('login/auth', views.login_view, name='login'),
path('signup', views.signup_view, name='signup'),
path('signup/auth', views.signup_view, name='signup'),
path('otp', views.otp_view, name='otp'),  
path('otp/verify', views.otp_view, name='otp')
]
