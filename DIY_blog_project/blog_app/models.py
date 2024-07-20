from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000)
    phone_number = models.IntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)


class Blog(BaseModel):
    name = models.CharField(max_length=100)
    content = models.TextField(max_length=1500)
    blogger = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=400)
