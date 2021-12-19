from django.db import reset_queries
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework.response import Response



def home(request , socket_url = None):
    return render(request , 'home.html')


import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer
from .helpers import *

def generate_thumbnails(socket_url , path):
    channel_layer = get_channel_layer()
    images = extractImages(path)

    async_to_sync(channel_layer.group_send)(
            'socket_url%s' % socket_url,{
                'type': 'send_thumbnails',
                'value': json.dumps({'images' : images})
            }
        )


@api_view(['POST'])
def upload(request):
    data = request.data
    youtube  = YoutubeSerializer(data = request.data)
    print(youtube)
    if youtube.is_valid():
        youtube.save()
        socket_url = data.get('socket_url')
        print(socket_url)
        print(youtube.data['video'])
        generate_thumbnails(socket_url , youtube.data['video'] )
        return Response({
            'status' : 200,
            'message' : 'Uploaded'
        })
    
    return Response({
        'status' : 400,
        'message' :  youtube.errors
    })
    




