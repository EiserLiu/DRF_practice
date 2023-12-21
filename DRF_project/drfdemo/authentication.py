from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model


class CustomAuthentication(BaseAuthentication):
    """
    自定义认证方式
    """

    def authenticate(self, request):
        """
        认证方法
        request: 本次客户端发送过来的http请求对象
        """
        user = request.query_params.get("user")
        # pwd = request.query_params.get("pwd")
        # if user != "Eiser" or pwd != "aize":
        #     return None
        # get_user_model获取当前系统中用户表对应的用户模型类
        # user = get_user_model().objects.first()
        user = get_user_model().objects.filter(username=user).first()
        return (user, None)  # 按照固定的返回格式填写 （用户模型对象, None）
