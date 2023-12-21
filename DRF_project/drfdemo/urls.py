"""drfdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticated

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="xxx项目接口文档",  # 必传
        default_version="v1.0.0",  # 必传
        description="描述信息",
        terms_of_service='',
        contact=openapi.Contact(email="1071519731@qq.com"),
        license=openapi.License(name="协议版本")
    ),
    public=True,  # 允许所有人访问
    permission_classes=[IsAuthenticated],  # 权限类
)

urlpatterns = [
    path('docs/', include_docs_urls(title='xxx接口文档')),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('admin/', admin.site.urls),
    # path('api/', include("stuapi.urls")),
    path('api/', include("students.urls")),
    path('sers/', include("sers.urls")),
    path('req/', include("req.urls")),
    path('demo/', include("demo.urls")),
    path('opt/', include("opt.urls"))

]
