from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from stuapi.models import Student

'''
serializers 是DRF提供给开发者调用的序列化器模块
里面声明了所有的可用序列化器的基类:
Serializer  序列化器基类,DRF中所有的序列化起类都必须继承于 Serializer 
ModelSerializer 模型序列化器,是序列化器基类的子类,在工作中,除了Serializer基类以为,最常用的序列化起类
'''


class Student1Serializer(serializers.Serializer):
    """学生信息序列化器"""
    # 1. 转换的字段声明
    # 客户端字段 = serializers.字段类型(选项=选项值,)
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    description = serializers.CharField()
    # 2. 如果当前序列化器继承的是ModelSerializer,则需要声明调用的模型信息
    # class Meta:
    #     model = 模型
    #     fields = ["字段1","字段2"....]

    # 3. 验证代码的对象方法
    # def validate(self, attrs): #validate是固定的
    #     pass
    #     return attrs

    # def validate_<字段名>(self, data):   #方法名的格式必须以validate_<字段名> 为名称,否则序列化起不识别!
    #     pass
    #     return data_

    # 4.模型操作方法
    # def create(self, validated_data):     #添加数据操作,添加数据后,自动实现了从字典变成模型对象的过程
    #     pass
    #
    # def update(self, instance, validated_data):   #更新数据操作,更新数据后,自动实现了从字典变成模型对象的过程
    #     pass


def check_classmate(data):
    """外部验证函数"""
    if len(data) != 3:
        raise serializers.ValidationError(detail="班级编号格式不正确!必须是三个字符", code="check_classmate")
    # 验证完成务必返回结果,否则验证结果没有该数据
    return data


class Student2Serializer(serializers.Serializer):
    """学生信息序列化器"""
    # 1. 转换的字段声明
    # 客户端字段 = serializers.字段类型(选项=选项值,)
    id = serializers.IntegerField(read_only=True)  # read_only=True在客户端提交数据时[反序列化阶段不会要求id字段]
    name = serializers.CharField(required=True)  # required=True 反序列化必填
    sex = serializers.BooleanField(default=True)  # default=True 反序列化借还没有提交,默认为True
    age = serializers.IntegerField(max_value=100, min_value=0, error_messages={
        "min_value": "The Age Filed Must Be 0 <= age",
        "max_value": "The Age Filed Must Be age <= 100"
    })  # 最大最小
    # validators 外部验证函数选项,值是一个列表,列表得到的成员是函数名,不能是字符串!!!
    classmate = serializers.CharField(validators=[check_classmate])
    description = serializers.CharField(allow_null=True,
                                        allow_blank=True)  # allow_null=True 允许客户端不填写内容,allow_blank=True 或者值为""

    # 2. 如果当前序列化器继承的是ModelSerializer,则需要声明调用的模型信息
    # class Meta:
    #     model = 模型
    #     fields = ["字段1","字段2"....]

    # 3. 验证代码的对象方法
    def validate(self, attrs):  # validate是固定的
        """
        验证来自客户端的所有数据
        类似会员注册的密码和确认密码,就只能在validate方法中校验
        validate是固定的方法名
        :param attrs: 是在序列化器实例化时的data选项数据
        :return:
        """
        # 307班只有女生
        if attrs.get("classmate") == "307" and attrs.get("sex"):
            raise serializers.ValidationError(detail="307班只能进去小姐姐~", code="validate")
        return attrs

    # def validate_<字段名>(self, data):   #方法名的格式必须以validate_<字段名> 为名称,否则序列化起不识别!
    #     pass
    #     return data_
    def validate_name(self, data):  # validate是固定的
        """验证单个字段
        方法名的格式必须以validate_<字段名> 为名称,否则序列化器不识别!
        validate开头的方法,会自动被is_valid调用
        """
        print(f"name{data}")
        if data in ["python", "django"]:
            # 在序列化器中,验证失败可以通过抛出异常的方式来告知 is_valid
            raise serializers.ValidationError(detail="学生姓名不能是python或django", code="validate_name")

        # 验证成功以后,必须返回数据,否则最终的验证结果中,就不会出现这个数据了
        return data

    # def validate_<字段名>(self, data):   #方法名的格式必须以validate_<字段名> 为名称,否则序列化起不识别!
    #     pass
    #     return data_

    # 4.模型操作方法
    def create(self, validated_data):
        """
        添加数据操作,
        方法名固定为create,
        固定参数validated_data就是验证成功后的结果,
        添加数据后,自动实现了从字典变成模型对象的过程
        """
        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        """
        更新数据操作,
        方法名固定为update,
        固定参数instance,实例化序列化器时,必须传入的模型对象
        固定参数validated_data就是验证成功后的结果
        更新数据后,自动实现了从字典变成模型对象的过程
        """
        # instance.name = validated_data["name"]
        # instance.age = validated_data["age"]
        # instance.sex = validated_data["sex"]
        # instance.classmate = validated_data["classmate"]
        # instance.description = validated_data["description"]
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()  # 调用模型对象的save方法,和视图中的serializer.save()不是同一个类的方法

        return instance


class StudentModelSerializer(serializers.ModelSerializer):
    """学生信息序列化器"""

    # 1. 转换的字段声明
    nickname = serializers.CharField(read_only=True, default="abc")

    # 2. 如果当前序列化器继承的是ModelSerializer,则需要声明调用的模型信息
    # 必须给Meat声明两个属性
    # class Meta:
    #    model = 模型    #必填
    #    fields = ["字段1","字段2"....] # 必填, 可以是字符串和列表/元组
    #    read_only_fields = [] #选填,只读字段列表,表示设置这里的字段只会在序列化阶段采用
    #    extra_kwargs = {   # 选填, 字段额外选项声明
    #        "字段名": {
    #           "选项": "选项值"
    #         }
    #       }
    class Meta:
        model = Student
        fields = ["id", "name", "age", "sex", "nickname"]
        # fields = "__all__"
        extra_kwargs = {   # 选填, 字段额外选项声明
            "age": {
                "min_value": 5,
                "max_value": 20,
                "error_messages": {
                    "min_value": "年龄最小值必须大于等于5",
                    "max_value": "年龄最大值必须小于等于20",
                }
            }
        }

    # 3. 验证代码的对象方法
    # def create(self, validated_data):
        # 密码加密
        # validated_data["passdowd"] = make_password(validated_data["passdowd"])
        # super().create(self, validated_data)

    # 4.模型操作方法
