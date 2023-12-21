from django.urls import path
from . import views
urlpatterns = [
    path("students/",views.StudentAPIView.as_view()),
    path("students1/",views.StudentView.as_view())
]