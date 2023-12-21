from django.urls import path, re_path

from . import views

urlpatterns = [
    path("example/", views.ExampleView.as_view()),
    path("home/", views.HomeAPIView.as_view()),
    path("home/info/", views.HomeInfoAPIView.as_view()),
    re_path("student/(?P<pk>\d+)", views.StudentInfoAPIView.as_view()),
    path("demo1/", views.DemoAPIView1.as_view()),
    path("demo2/", views.DemoAPIView2.as_view()),
    path("demo3/", views.DemoAPIView3.as_view()),
    path("demo4/", views.DemoAPIView4.as_view()),
    path("demo5/", views.DemoAPIView5.as_view()),

]
