import re
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import ValidationError
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
from rest_framework.pagination import PageNumberPagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage

def paginate(data, paginator, pagenumber):
    """
    This method to create the paginated results in list API views.
    """

    if int(pagenumber) > paginator.num_pages:
        raise ValidationError("Not enough pages", code=404)
    try:
        previous_page_number = paginator.page(
            pagenumber).previous_page_number()
    except EmptyPage:
        previous_page_number = None
    try:
        next_page_number = paginator.page(pagenumber).next_page_number()
    except EmptyPage:
        next_page_number = None

    data_to_show = paginator.page(pagenumber).object_list

    return {
        'pagination': {
            'previous_page': previous_page_number,
            'is_previous_page': paginator.page(pagenumber).has_previous(),
            'next_page': next_page_number,
            'is_next_page': paginator.page(pagenumber).has_next(),
            'start_index': paginator.page(pagenumber).start_index(),
            'end_index': paginator.page(pagenumber).end_index(),
            'total_entries': paginator.count,
            'total_pages': paginator.num_pages,
            'page': int(pagenumber)
        },
        'results': data_to_show
    }

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StandardResultsSetPagination

    def list(self , request):
        objs = self.queryset.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(objs, 2)
        data = paginate(objs ,paginator , page )

        serializer = self.serializer_class(data['results'] , many = True)
        print(serializer.data)
        data['results'] = serializer.data

        return Response({
            'status' : 200,
            'message' : 'Student retireved successfully',
            'data' : data 
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