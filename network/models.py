from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="postUser")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,blank=True,related_name="postLikes")

    def __str__(self):
        return f"{self.user} posted on {self.timestamp.strftime('%m/%d/%Y, %H:%M:%S')}"
    
    def numberOfLikes(self):
        return self.likes.all().count()


class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followUser")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followFollowing")

    def __str__(self):
        return f"{self.user} is followed by {self.following}"
