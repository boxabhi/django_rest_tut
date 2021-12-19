from django.db import models

# Create your models here.


class YoutubeThumbnails(models.Model):
    video = models.FileField(upload_to="youtube")
    

class GeneratedThumbnails(models.Model):
    youtube = models.ForeignKey(YoutubeThumbnails , on_delete=models.CASCADE)
    path = models.TextField()