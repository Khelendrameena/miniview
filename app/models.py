from django.db import models


class MyModel(models.Model):
    id = models.CharField(
        max_length=100,  # Adjust length as needed
        primary_key=True,  # Make it the primary key
        unique=True,  # Ensure the ID is unique
    )
    views = models.IntegerField(default=0)  # Views field
    likes = models.IntegerField(default=0)  # Likes field

    def __str__(self):
        return f"ID: {self.id}, Views: {self.views}, Likes: {self.likes}"



class comentconfig(models.Model):
      mainid = id = models.CharField(
        max_length=100,  # Adjust length as needed
      )
      id = id = models.CharField(
        max_length=100,  # Adjust length as needed
        primary_key=True,
        unique=True
      )
      name = models.CharField(max_length=100)
      mess = models.TextField()
      like = models.IntegerField(default=0)

      def __str__(self):
        return f"{self.id}"

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

class Vlog(models.Model):     
    vlog_id = models.CharField(max_length=100, unique=True, primary_key=True, default="default_id")
    thumbnail = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_html = models.TextField()
    user = models.CharField(max_length=100)
    vlog_labels = models.CharField(max_length=100)
    vlog_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserReaction(models.Model):
    vlog_id = models.CharField(max_length=255,unique=True)  # Unique identifier for the vlog
    username = models.CharField(max_length=100)
    follow = models.IntegerField(default=0)
    follow_to = models.CharField(max_length=100,default='null')
    like = models.IntegerField(default=0)  # True for like (1), False for dislike (0)
    comment = models.IntegerField(default=0)  # True if commented, else False
    views = models.IntegerField(default=0)  # True if viewed, else False
    user_interest = models.CharField(max_length=200,default='null')
    interest_rate = models.FloatField(default=0.0)  # Rating or interest percentage

    def __str__(self):
        return f"Reaction by {self.username} on vlog {self.vlog_id}"
