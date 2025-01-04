# Register your models here.
from django.contrib import admin
from app.models import MyModel
from app.models import comentconfig
from app.models import Profile
from app.models import Vlog
from app.models import UserReaction
from app.models import param

admin.site.register(MyModel)
admin.site.register(comentconfig)
admin.site.register(Profile)
admin.site.register(UserReaction)
admin.site.register(Vlog)
admin.site.register(param)
