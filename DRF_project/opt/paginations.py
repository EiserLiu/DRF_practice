from rest_framework.pagination import PageNumberPagination


# PageNumberPagination，以页码作为分页条件
# page=1&page_size=10      第1页
# page=2&page_size=10      第2页
# ...
# LimitOffsetPagination，以数据库查询的limit和offset数值作为分页条件
# limit=10&offset=0   第1页
# limit=10&offset=10  第2页
# ...

# 自定义分页器，PageNumberPagination
class StudentPageNumberPagination(PageNumberPagination):
    page_query_param = "page"  # 查询字符串中代表页码的变量名
    page_size_query_param = "size"  # 查询字符串中代表每一页数据的变量名
    page_size = 10  # 每一页的数据量
    max_page_size = 100  # 允许客户端通过查询字符串调整的最大单页数据量
