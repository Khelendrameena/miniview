from django.urls import path
from .import views

urlpatterns = [
path('', views.home, name='home_page'),
path('view',views.view,name='views'),
path('meena@kh8656/6302a139-d03a-11ef-8903-5d0b6fd2483d/<str:quary>/<int:number>',views.api,name="api"),
path('app/@<str:username_2>/follow',views.follow,name='follow'),
path('@<str:username>/edit',views.profilebin,name='profile'),
path('profile/edited',views.profiledit,name='profile edit'),
path('@<str:username>/vlog', views.vlog, name='vlog'),
path('@<str:username>/vlog/publish', views.vlogpost, name='vlog publish'),
path('vlog/<str:vlog_id>', views.vlogrect, name='vlog rection'),
path('vlog/show/<str:vlog_id>', views.vlogshow, name='vlog view'),
path('vlog/internal/<int:index>', views.vlogshow, name='vlog view'),
path('@<str:username>/', views.profile, name='profile'),
path('top/<str:para>',views.most,name='best vlog'),
path('login', views.login_view, name='login'),
path('robots.txt',views.robots_txt, name='robots_txt'),
path('about',views.about,name='about page'),
path('6302a139-d03a-11ef-8903-5d0b6fd2483d.xml',views.custom_sitemap,name='sitemap xml'),
path('app/view/name', views.usernameedit, name='username edit'),
path('login/auth', views.login_view, name='login'),
path('signup', views.signup_view, name='signup'),
path('signup/auth', views.signup_view, name='signup'),
path('otp', views.otp_view, name='otp'),  
path('otp/verify', views.otp_view, name='otp'),
path('search',views.search,name='search'),
path('search/quary',views.searchquary,name='search'),
path('coment',views.coment,name='coment'),
path('coment/add',views.comentadd,name='comentadd'),
path('coment/count',views.comentlikeadd,name='comentlikeadd')
]

