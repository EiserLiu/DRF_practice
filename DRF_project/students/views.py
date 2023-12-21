from django.db.models import Model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from stuapi.models import Student
from .serializers import Student2ModelSerializer


# Create your views here.
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = Student2ModelSerializer

