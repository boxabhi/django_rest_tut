from django.db.models.fields.files import FileField
from home import models
from rest_framework import serializers
from .models import *
import uuid

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    stundent_id = serializers.CharField(required = False , allow_null = True , allow_blank = True)
    #student_department = DepartmentSerializer(many = True , read_only = True)
    department = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'
        #depth = 1

    def has_number(self,value):
        return any(c.isdigit() for c in value) 

    def validate(self, data):
        
        if self.has_number(data['student_name']):
            raise serializers.ValidationError('name cannot contains number')
        
        return data

    def get_department(self , obj):
        return obj.student_department.department_name



    def create(self, validated_data):
        print(validated_data)
        student_id = validated_data['student_department'].short_form + str(uuid.uuid4())[0:6]
        obj = Student.objects.create(
            student_name = validated_data['student_name'],
            stundent_id = student_id,
            student_department = validated_data['student_department'])    

        return obj

