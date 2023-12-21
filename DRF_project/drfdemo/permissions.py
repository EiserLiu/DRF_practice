from rest_framework.permissions import BasePermission


class IsXiaoMingPermission(BasePermission):
    """
    自定义权限，可用于全局配置，也可以用于局部配置
    """

    def has_permission(self, request, view):
        """
        视图权限
        返回结果未True则表示允许访问视图类
        request: 本次客户端提交的请求对象
        view: 本次客户端访问的视图类
        """
        # 写在自己要实现认证的代码过程返回值为True，则表示通行
        return bool(request.user and request.user.username=="xiaoming")

    def has_object_permission(self, request, view, obj):
        """
        模型权限，写了视图权限(has_permission)方法，一般就不需要写这个了。
        返回结果未True则表示允许操作模型对象
        """
        from school.models import Student
        if isinstance(obj, Student):
            # 限制只有小明才能操作Student模型
            user = request.query_params.get("user")
            return user == "xiaoming"  # 如果不是xiaoming，返回值为False，不能操作
        else:
            # 操作其他模型，直接放行
            return True