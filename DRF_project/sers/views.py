import json

from django.views import View
from django.http.response import JsonResponse

from .serializers import Student1Serializer, Student2Serializer, StudentModelSerializer
from stuapi.models import Student


# Create your views here.

class Student1View(View):
    def get1(self, request):
        """序列化器-序列化调用-序列化一个模型对象"""
        # 1. 获取数据集
        student = Student.objects.first()
        # 2. 实例化序列化器,得到序列化对象
        serializer = Student1Serializer(instance=student)
        # 3. 调用序列化对象的data属性方法获取转换后的数据
        data = serializer.data
        # 4. 响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={"ensure_ascii": False})

    def get2(self, request):
        """序列化器-序列化阶段的调用"""
        # 1. 获取数据集
        student_list = Student.objects.all()
        # 2. 实例化序列化器,得到序列化对象[传递到序列化器的模型对象如果是多个,务必many=True]
        serializer = Student1Serializer(instance=student_list, many=True)
        # 3. 调用序列化对象的data属性方法获取转换后的数据
        data = serializer.data
        # 4. 响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={"ensure_ascii": False})

    def get3(self, request):
        """反序列化-采用字段选项来验证数据"""
        # 1. 接受客户端提交的数据
        # data = json.dumps(request.body)
        # 模拟客户端数据
        data = {
            "name": "小红",
            "age": 30,
            "sex": True,
            "classmate": "301",
            "description": "这家伙很懒,什么都没有留下"
        }
        # 1.1 实例化序列化器,获取序列化对象
        serializer = Student2Serializer(data=data)
        # 1.2 调用序列化器进行数据验证
        ret = serializer.is_valid(raise_exception=True)  # 抛出异常
        # ret = serializer.is_valid()                     # 不抛出异常
        print(ret)
        # 1.3 获取验证以后的结构
        if ret:
            return JsonResponse(dict(serializer.validated_data))
        else:
            return JsonResponse(dict(serializer.errors))
        # 2. 操作数据库

        # 3. 返回结果

    def get4(self, request):
        """反序列化-采用字段选项来验证数据[验证失败抛出异常,工作中最常用]"""
        # 1. 接受客户端提交的数据
        # 模拟客户端数据
        data = {
            "name": "小明",
            "age": 30,
            "sex": True,
            "classmate": "3071",
            "description": "这家伙很懒,什么都没有留下"
        }
        # 1.1 实例化序列化器,获取序列化对象
        serializer = Student2Serializer(data=data)
        # 1.2 调用序列化器进行数据验证
        ret = serializer.is_valid(raise_exception=True)  # 抛出异常,代码不向下执行

        # 1.3 获取验证以后的结构
        print(serializer.validated_data)

        # 2. 操作数据库

        # 3. 返回结果
        return JsonResponse({})

    def get5(self, request):
        """反序列化-验证完成后,添加数据入库"""
        # 1. 接受客户端提交的数据
        # 模拟客户端数据
        data = {
            "name": "小海",
            "age": 26,
            "sex": True,
            "classmate": "301",
            "description": "这家伙很懒,什么都没有留下",
        }
        # 1.1 实例化序列化器,获取序列化对象
        serializer = Student2Serializer(data=data)
        # 1.2 调用序列化器进行数据验证
        serializer.is_valid(raise_exception=True)  # 抛出异常,代码不向下执行

        # 2. 获取验证以后的结果,操作数据库
        serializer.save()  # 会根据实例化序列化器的时候,是否传入instance属性,来自动调用create或者update方法.传入instance属性,自动调用update方法;没有传入instance属性,则自动调用create

        # 3. 返回结果

        return JsonResponse(serializer.data, status=201)

    def get6(self, request):
        """反序列化-验证完成后,更新数据入库"""
        # 1. 根据客户端访问的url地址中,获取pk值

        pk = 5
        try:
            student = Student.objects.get(pk=pk)
        except:
            return JsonResponse({"errors": "当前学生不存在!"}, status=400)
        # 2.接收客户端提交的修改数据
        # 模拟来自客户端的数据
        data = {
            "name": "小李",
        }

        # 3. 修改操作中的实例化序列化器对象
        serializer = Student2Serializer(instance=student, data=data, partial=True)
        # 4. 验证数据
        serializer.is_valid(raise_exception=True)
        # 5. 入库
        serializer.save()

        # 6. 返回结果
        return JsonResponse(serializer.data, status=201)


class StudentView(View):
    def get1(self, request):
        """模型序列化器"""
        # 1. 获取数据集
        student = Student.objects.first()
        student.nickname = "小学生"
        # 2. 实例化序列化器,得到序列化对象
        serializer = StudentModelSerializer(instance=student)
        # 3. 调用序列化对象的data属性方法获取转换后的数据
        data = serializer.data
        # 4. 响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={"ensure_ascii": False})

    def get2(self, request):
        """序列化器-序列化阶段的调用"""
        # 1. 获取数据集
        student_list = Student.objects.all()
        # 2. 实例化序列化器,得到序列化对象[传递到序列化器的模型对象如果是多个,务必many=True]
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3. 调用序列化对象的data属性方法获取转换后的数据
        data = serializer.data
        # 4. 响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={"ensure_ascii": False})

    def get3(self, request):
        """反序列化-采用字段选项来验证数据"""
        # 1. 接受客户端提交的数据
        # data = json.dumps(request.body)
        # 模拟客户端数据
        data = {
            "name": "小红",
            "age": 13,
            "sex": True,
            "classmate": "301",
            "description": "这家伙很懒,什么都没有留下"
        }
        # 1.1 实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(data=data)
        # 1.2 调用序列化器进行数据验证
        ret = serializer.is_valid(raise_exception=True)  # 抛出异常
        # ret = serializer.is_valid()                     # 不抛出异常
        print(ret)
        # 1.3 获取验证以后的结构
        if ret:
            return JsonResponse(dict(serializer.validated_data))
        else:
            return JsonResponse(dict(serializer.errors))
        # 2. 操作数据库

        # 3. 返回结果

    def get4(self, request):
        """反序列化-采用字段选项来验证数据[验证失败抛出异常,工作中最常用]"""
        # 1. 接受客户端提交的数据
        # 模拟客户端数据
        data = {
            "name": "小明",
            "age": 30,
            "sex": True,
            "classmate": "3071",
            "description": "这家伙很懒,什么都没有留下"
        }
        # 1.1 实例化序列化器,获取序列化对象
        serializer = Student2Serializer(data=data)
        # 1.2 调用序列化器进行数据验证
        ret = serializer.is_valid(raise_exception=True)  # 抛出异常,代码不向下执行

        # 1.3 获取验证以后的结构
        print(serializer.validated_data)

        # 2. 操作数据库

        # 3. 返回结果
        return JsonResponse({})

    def get5(self, request):
        """反序列化-验证完成后,添加数据入库"""
        # 1. 接受客户端提交的数据
        # 模拟客户端数据
        data = {
            "name": "小海",
            "age": 26,
            "sex": True,
            "classmate": "301",
            "description": "这家伙很懒,什么都没有留下"
        }
        # 1.1 实例化序列化器,获取序列化对象
        serializer = Student2Serializer(data=data)
        # 1.2 调用序列化器进行数据验证
        serializer.is_valid(raise_exception=True)  # 抛出异常,代码不向下执行

        # 2. 获取验证以后的结果,操作数据库
        serializer.save()  # 会根据实例化序列化器的时候,是否传入instance属性,来自动调用create或者update方法.传入instance属性,自动调用update方法;没有传入instance属性,则自动调用create

        # 3. 返回结果

        return JsonResponse(serializer.data, status=201)

    def get6(self, request):
        """反序列化-验证完成后,更新数据入库"""
        # 1. 根据客户端访问的url地址中,获取pk值

        pk = 5
        try:
            student = Student.objects.get(pk=pk)
        except:
            return JsonResponse({"errors": "当前学生不存在!"}, status=400)
        # 2.接收客户端提交的修改数据
        # 模拟来自客户端的数据
        data = {
            "name": "小李",
        }

        # 3. 修改操作中的实例化序列化器对象
        serializer = Student2Serializer(instance=student, data=data, partial=True)
        # 4. 验证数据
        serializer.is_valid(raise_exception=True)
        # 5. 入库
        serializer.save()

        # 6. 返回结果
        return JsonResponse(serializer.data, status=201)
