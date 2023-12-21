from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from drfdemo.permissions import IsXiaoMingPermission
from opt.paginations import StudentPageNumberPagination
from school.models import Student
from school.serializers import StudentModel2Serializer


class ExampleView(APIView):
    # 类属性
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request):
        print(request.user)
        if request.user.id:
            print("通过验证")
        else:
            print("未通过验证")
        return Response({"msg": "ok"})


# Create your views here.
class HomeAPIView(APIView):
    # authentication_classes = [CustomAuthentication, ]
    def get(self, request):
        """单独设置认证方式"""
        print(request.user)  # 在中间件AuthenticationMiddleware中完成用户身份识别的，如果没有登录request.user值为AnonymousUser
        if request.user.id is None:
            return Response("未登录用户：游客")
        else:
            return Response(f"已登录用户：{request.user}")


class HomeInfoAPIView(APIView):
    # 内置权限
    # permission_classes = [IsAuthenticated,]   # 仅通过登录认证的站点会员
    # permission_classes = [IsAdminUser]  # 仅管理员用户
    # permission_classes = [IsAuthenticatedOrReadOnly]  # 游客只能查看,登录后可以任意操作
    # 自定义权限
    permission_classes = [IsXiaoMingPermission]

    def get(self, request):
        return Response({"msg", "ok"})

    def post(self, request):
        return Response({"msg", "ok"})


class StudentInfoAPIView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModel2Serializer
    permission_classes = [IsAuthenticated]

    # 限流局部配置[这里需要配合在全局配置中的DEFAULT_THROTTLE_RATES来设置频率]
    throttle_classes = [UserRateThrottle]


class DemoAPIView1(APIView):
    """自定义限流"""
    permission_classes = [IsAuthenticated]

    throttle_scope = "member"

    def get(self, request):
        return Response({"msg", "ok"})


class DemoAPIView2(APIView):
    """自定义限流"""
    permission_classes = [IsAuthenticated]

    throttle_scope = "vip"

    def get(self, request):
        return Response({"msg", "ok"})


class DemoAPIView3(APIView):
    """自定义限流"""

    permission_classes = [IsAuthenticated]

    throttle_scope = "vvip"

    def get(self, request):
        return Response({"msg", "ok"})


class DemoAPIView4(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModel2Serializer

    # 局部过滤
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # 过滤字段
    # filter_fields = ["sex", "classmate"]

    # 数据排序
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'age']




class DemoAPIView5(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModel2Serializer

    # # 关闭全局分页器
    # pagination_class = None
    pagination_class = StudentPageNumberPagination
