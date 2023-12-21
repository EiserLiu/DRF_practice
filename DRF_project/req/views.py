from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponse
from django.views import View
from rest_framework import status


# Create your views here.

class StudentView(View):
    def get(self, request):  # django提供的View视图,在视图方法中传入的request变量是 WSGIHttpRequest
        print(request)  # WSGIHttpRequest---> 父类 --> django.http.response.HttpResponse
        return HttpResponse("ok")


class StudentAPIView(APIView):
    def get(self, request):
        print(f"drf.request={request}")  # rest_framework.response.Response 是属于DRF单独声明的请求处理对象,与django提供的HttpResponse没有关系
        print(f"django.request={request._request}")

        """获取查询参数/查询字符串"""
        print(f"request.query_params={request.query_params}")

        return Response({"msg": "ok"}, status=status.HTTP_201_CREATED, headers={"company": "py37"})

    def post(self, request):
        # 添加数据
        # 获取请求体数据
        print(f"request.data={request.data}")
        return Response({"msg": "ok"})

    def put(self, request):
        # 更新数据
        return Response({"msg": "ok"})
