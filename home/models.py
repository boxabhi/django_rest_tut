from django.db import models
from django.db.models.fields import related

# Create your models here.
# CS-123DF

class Color(models.Model):
    color_name = models.CharField(max_length=100)


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    short_form = models.CharField(max_length=5)

class Student(models.Model):
    student_name = models.CharField(max_length = 100)
    stundent_id = models.CharField(max_length=100 , unique=True)
    student_department = models.ForeignKey(Department , related_name='department'  , on_delete=models.CASCADE)


class FileUpload(models.Model):
    file = models.FileField(upload_to='home')