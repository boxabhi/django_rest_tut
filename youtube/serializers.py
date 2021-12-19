from rest_framework import serializers
from .models import *



class YoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeThumbnails
        fields = '__all__'