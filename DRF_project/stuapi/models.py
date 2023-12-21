from django.db import models


# Create your models here.
class Student(models.Model):
    """学生信息"""
    name = models.CharField(max_length=255, verbose_name="姓名", help_text="姓名")
    sex = models.BooleanField(default=1, verbose_name="性别",help_text="性别")
    age = models.IntegerField(verbose_name="年龄")
    classmate = models.CharField(max_length=5, verbose_name="班级编号")
    description = models.TextField(max_length=1000, verbose_name="个性签名")


    class Meta:
        db_table = "student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name

