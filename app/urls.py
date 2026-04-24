from django.urls import path
from .import views

urlpatterns = [
 path('', views.home, name='home_page'),
 path('app/@<str:username_2>/follow',views.follow,name='follow'),
 path('logout/', views.logout_view, name='logout'),
 path('@<str:username>/edit',views.profilebin,name='profile'),
 path('profile/edited',views.profiledit,name='profile edit'),
 path('@<str:username>/', views.profile, name='profile'),
 path('login', views.login_view, name='login'),
 path('app/view/name', views.usernameedit, name='username edit'),
 path('login/auth', views.login_view, name='login'),
 path('signup', views.signup_view, name='signup'),
 path('signup/auth', views.signup_view, name='signup'),
 path('otp', views.otp_view, name='otp'),
 path('otp/verify', views.otp_view, name='otp'),
 ]
