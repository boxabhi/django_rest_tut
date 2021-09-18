import re
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializer import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from rest_framework import status, viewsets
from rest_framework.decorators import action




def home(request):
    return render(request , 'home.html')


def login(request):
    return HttpResponse("not login")

# CRUD
# Student - CU RD  CRUD

# {
#     'status' : 200,
#     'message' : 'Student retireved successfully'
#     'data' : [

#     ]
# }
from rest_framework import status
from django.db.models import Q

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self , request):
        objs = self.queryset.all()
        search = request.GET.get('search')
        if search:
            objs = objs.filter(
                Q(student_department__department_name__icontains = search) |
                Q(student_name__icontains = search) |
                Q(stundent_id__icontains = search)       
                )

        serializer = self.serializer_class(objs , many = True)
        return Response({
            'status' : 200,
            'message' : 'Student retireved successfully',
            'data' : serializer.data   
        })

    


    @action(methods=['post'], detail=True)
    def show_action(self , request,pk):
        print(request.GET.get('params'))
        return Response({'status' : 200 , 'message' : 'I am action'})


# class StudentMixin():



class RegisterView(APIView):

    def post(self , request):
        return Response({})


class LoginView(APIView):

    def post(self , request):
        try:
            data  = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                username = serializer.data['username']
                password = serializer.data['password']

                if not User.objects.filter(username = username).exists():
                    return Response({'status' : 400 , 'message' : 'invalid credentials'})
                    
                user = authenticate(email = username , password = password)


                jwt_token = RefreshToken(user)
                print(jwt_token)
                return Response({'status' : 200 ,
                 'message' : 'login success' , 
                'token' : str(jwt_token)
                 })





            return Response({'status' : 400 , 'errors' : serializer.errors})
        
        except Exception as e:
            print(e)
        
        return Response({'status' : 500  , 'message' : 'something went wrong'})



class StudentAPI(APIView):
    def get(self , request):
        objs = StudentSerializer(Student.objects.all() , many = True)
        
        return Response({'data' : objs.data})
    def post(self , request):
        try:
            data = request.data
            serializer = StudentSerializer(data = data)
            if not serializer.is_valid():
                return Response({'status' : 400 , 'errors' : serializer._errors})
            
            serializer.save()

            return Response({
                'status' : 200 , 
                'message' : 'Student created',
                'data' : serializer.data
            })
        except Exception as e:
            print(e)
        
        return Response({'status' : 400 , 'message' : 'somethign went wrong'})