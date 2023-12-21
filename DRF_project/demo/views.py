from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from stuapi.models import Student
from .serializers import StudentModelSerializer

"""
GET     /demo/students  获取所有学生信息
POST    /demo/students  添加一个学生信息

GET     /demo/students<pk>  获取一个学生信息
PUT     /demo/students<pk>  更新一个学生信息
DELETE  /demo/students<pk>  删除一个学生信息
"""

"""APIView基本视图类"""


class StudentAPIView(APIView):
    def get(self, request):
        """获取所有学生信息"""
        # 1. 从数据库中读取学生列表信息
        student_list = Student.objects.all()
        # 2. 实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一条数据"""
        # 1. 获取客户端提交的数据,实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(data=request.data)
        # 2. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfoAPIView(APIView):
    def get(self, request, pk):
        """获取一条数据"""
        # 1. 使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(instance=student)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def put(self, request, pk):
        """更新数据"""
        # 1. 使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student, data=request.data)

        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        # 1. 使用pk作为条件获取模型对象,并删除
        try:
            student = Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            pass
        # 2. 返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""GenericAPIView通用视图类"""


class StudentGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有数据"""
        # 1. 从数据库中读取模型列表信息
        queryset = self.get_queryset()  # GenericAPIView提供的get_queryset
        # 2. 实例化序列化器,获取序列化对象
        serializer = self.get_serializer(instance=queryset, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一条数据"""
        # 1. 获取客户端提交的数据,实例化序列化器,获取序列化对象
        serializer = self.get_serializer(data=request.data)

        # 2. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentInfoGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        """获取一条数据"""
        # 1. 使用pk作为条件获取模型对象
        student = self.get_object()
        # 2. 实例化序列化器,获取序列化对象
        serializer = self.get_serializer(instance=student)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def put(self, request, pk):
        """更新数据"""
        # 1. 使用pk作为条件获取模型对象
        instance = self.get_object()
        # 2. 获取客户端提交的数据
        serializer = self.get_serializer(instance=instance, data=request.data)

        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        # 1. 使用pk作为条件获取模型对象,并删除
        self.get_object().delete()
        # 2. 返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
使用drf内置的模型扩展类[混入类]结合GenericAPIView实现通用视图方法的简写操作
from rest_framework.mixins import ListModelMixin   获取多条数据，返回响应结果    list
from rest_framework.mixins import CreateModelMixin 添加一条数据，返回响应结果    create
from rest_framework.mixins import RetrieveModelMixin 获取一条数据，返回响应结果  retrieve
from rest_framework.mixins import UpdateModelMixin 更新一条数据，返回响应结果    update(更新全部字段)和partial_update(更新单个或部分字段，例如修改密码，修改头像)
from rest_framework.mixins import DestroyModelMixin 删除一条数据，返回响应结果   destroy
"""
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin


class StudentMixinView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有数据"""
        return self.list(request)

    def post(self, request):
        """添加一条数据"""
        return self.create(request)


class StudentInfoMixinView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


"""
视图子类是通用视图类 和 模型拓展类的子类
"""
"""
上面的接口代码还可以继续更加的精简，drf在使用GenericAPIView和Mixins进行组合以后，还提供了视图子类。
视图子类，提供了各种的视图方法调用mixins操作

    ListAPIView = GenericAPIView + ListModelMixin         获取多条数据的视图方法
    CreateAPIView = GenericAPIView + CreateModelMixin     添加一条数据的视图方法
    RetrieveAPIView = GenericAPIView + RetrieveModelMixin 获取一条数据的视图方法
    UpdateAPIView = GenericAPIView + UpdateModelMixin     更新一条数据的视图方法
    DestroyAPIView = GenericAPIView + DestroyModelMixin   删除一条数据的视图方法
组合视图子类
    ListCreateAPIView = ListAPIView + CreateAPIView
    RetrieveUpdateAPIView = RetrieveAPIView + UpdateAPIView
    RetrieveDestroyAPIView = RetrieveAPIView + DestroyAPIView
    RetrieveUpdateDestroyAPIView = RetrieveAPIView + UpdateAPIView + DestroyAPIView
"""
# from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# class StudentView(ListAPIView, CreateAPIView):
class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


# class StudentInfoView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
class StudentInfoView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
上面的接口在实现过程中,存在两个问题
1. 路由合并
2. get方法重复
ViewSet --> APIView
"""

from rest_framework.viewsets import ViewSet


class StudentViewSet(ViewSet):
    def get_student_list(self, request):
        """获取所有学生信息"""
        # 1. 从数据库中读取学生列表信息
        student_list = Student.objects.all()
        # 2. 实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一条数据"""
        # 1. 获取客户端提交的数据,实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(data=request.data)
        # 2. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_student_info(self, request, pk):
        """获取一条数据"""
        # 1. 使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 实例化序列化器,获取序列化对象
        serializer = StudentModelSerializer(instance=student)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def update(self, request, pk):
        """更新数据"""
        # 1. 使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student, data=request.data)

        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        # 1. 使用pk作为条件获取模型对象,并删除
        try:
            student = Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            pass
        # 2. 返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""GenericViewSet 通用视图集"""
from rest_framework.viewsets import GenericViewSet


class StudentGenericViewSet(GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def list(self, request):
        """获取所有数据"""
        # 1. 从数据库中读取模型列表信息
        queryset = self.get_queryset()  # GenericAPIView提供的get_queryset
        # 2. 实例化序列化器,获取序列化对象
        serializer = self.get_serializer(instance=queryset, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def create(self, request):
        """添加一条数据"""
        # 1. 获取客户端提交的数据,实例化序列化器,获取序列化对象
        serializer = self.get_serializer(data=request.data)

        # 2. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        """获取一条数据"""
        # 1. 使用pk作为条件获取模型对象
        student = self.get_object()
        # 2. 实例化序列化器,获取序列化对象
        serializer = self.get_serializer(instance=student)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def update(self, request, pk):
        """更新数据"""
        # 1. 使用pk作为条件获取模型对象
        instance = self.get_object()
        # 2. 获取客户端提交的数据
        serializer = self.get_serializer(instance=instance, data=request.data)

        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        # 1. 使用pk作为条件获取模型对象,并删除
        self.get_object().delete()
        # 2. 返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""GenericViewSet 通用视图集 + 混入类"""


class StudentMixinViewSet(GenericViewSet, ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
ReadOnlyModelViewSet = mixins.RetrieveModelMixin + mixins.ListModelMixin + GenericViewSet
"""

from rest_framework.viewsets import ReadOnlyModelViewSet


class StudentReadOnlyMixinViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


# ModelViewSet 五个API接口都有
from rest_framework.viewsets import ModelViewSet  # 万能视图集
from rest_framework.decorators import action


class StudentModelViewSet(ModelViewSet):
    """
    学生信息模型
    create：添加一个学生信息
    read：查询一个学生信息
    """
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    @action(methods=["get"], detail=True, url_path="user/login")
    def login(self, request, pk):
        """登录视图"""
        return Response({"msg": "登录成功"})
