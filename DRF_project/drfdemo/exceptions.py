from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from django.db import DataError

def custom_exception_handler(exc, context):
    """
    自定义异常函数
    :param exc: 本次发生的异常对象
    :param context: 本次发生异常时的上下文环境信息，字典，
                    所谓的执行上下文就是python解释器在执行代码时保存在内存中的变量、函数、类、对象、模块等一系列的信息组成的环境信息。
    :return:
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        """发生异常，def没有处理"""
        if isinstance(exc, ZeroDivisionError):
            response = Response({"detail": "0不能作为除数"})
        if isinstance(exc,DataError):
            response = Response({"detail": "数据库异常"})


    return response
