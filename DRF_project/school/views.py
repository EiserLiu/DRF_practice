from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serializers import StudentModel2Serializer

class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModel2Serializer
