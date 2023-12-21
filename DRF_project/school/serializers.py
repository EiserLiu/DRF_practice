from rest_framework import serializers

from school.models import Teacher, Student


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class StudentModel2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
