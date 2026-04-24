from django.db import models

class Profile(models.Model):
    profile_id = models.CharField(max_length=100, unique=True, primary_key=True, default="default_id")  # Default value
    profile_picture = models.CharField(max_length=1000, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150)
    followers = models.IntegerField(default=0)
    vlog = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    des = models.CharField(max_length=15000, blank=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.username


