# coding:utf-8
from django.http import HttpResponse


# 主界面
def index(request):
    return HttpResponse('<h2>OK</h2>')


# 关于
def about_me(request):
    return HttpResponse('<h2>OK</h2>')


# 链接
def link(request):
    return HttpResponse('<h2>OK</h2>')


# 目录
def archives(request):
    return HttpResponse('<h2>OK</h2>')


# 标签
def taglist(request, tag_name):
    return HttpResponse('<h2>OK</h2>')


# 标签列表
def taglist(request):
    return HttpResponse('<h2>OK</h2>')


# 项目
def projects(request):
    return HttpResponse('<h2>OK</h2>')


# 文章
def posts(request, title):
    return HttpResponse('<h2>OK</h2>')
