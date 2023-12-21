from rest_framework import serializers
from stuapi.models import Student


class Student2ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        # fields = ["id","name"]
