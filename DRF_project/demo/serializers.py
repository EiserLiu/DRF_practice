from rest_framework import serializers
from stuapi.models import Student


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {   # 选填, 字段额外选项声明
            "age": {
                "min_value": 5,
                "max_value": 30,
                "error_messages": {
                    "min_value": "年龄最小值必须大于等于5",
                    "max_value": "年龄最大值必须小于等于30",
                }
            }
        }