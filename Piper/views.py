# coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from .select_result import read_file, write_file
from .models import Post, PiperPost, OtherPost
from PiperDjango.settings import BASE_DIR, MENU_DIR
import os.path, tqdm, glob


# 主界面
def index(request):
    post_dir = os.path.join(BASE_DIR, 'posts')
    posts = []
    for md_dir in tqdm.tqdm(glob.glob(os.path.join(post_dir, '*.md'))):
        basename = os.path.basename(md_dir)
        markdown = read_file(md_dir)
        try:
            post = PiperPost(basename, markdown)
        except Exception as e:
            raise Exception("parse '%s', %s" % (basename, e)) from None
        posts.append(post)
    sorted(posts, key=lambda d:d.post_date, reverse=True)
    return render(request, 'home/index.html', {'posts': posts, 'recents':posts[:5]})


# 关于
def about_me(request):
    about_dir = os.path.join(MENU_DIR, 'about-me.md')
    basename = os.path.basename(about_dir)
    markdown = read_file(about_dir)
    post = OtherPost(basename, markdown)
    return render(request, 'home/post.html', {'post': post})


# 链接
def link(request):
    link_dir = os.path.join(MENU_DIR, 'links.md')
    basename = os.path.basename(link_dir)
    markdown = read_file(link_dir)
    post = OtherPost(basename, markdown)
    return render(request, 'home/post.html', {'post': post})


# 目录
def archives(request):
    post_dir = os.path.join(BASE_DIR, 'posts')
    local_archives = {}
    count = 0
    for md_dir in tqdm.tqdm(glob.glob(os.path.join(post_dir, '*.md'))):
        basename = os.path.basename(md_dir)
        markdown = read_file(md_dir)
        try:
            post = PiperPost(basename, markdown)
        except Exception as e:
            raise Exception("parse '%s', %s" % (basename, e)) from None
        count+= 1
        year = post.last_modify_date.split('-')[0]
        if year in local_archives:
            local_archives[year].append(post)
        else:
            local_archives[year] = [post]

    # 排序
    local_archives = sorted(local_archives.items(), key=lambda x: x[0], reverse=True)

    return render(request, 'home/archives.html', {'archives': local_archives, 'count': count})


# 标签
def tag(request, tag_name):
    post_dir = os.path.join(BASE_DIR, 'posts')
    local_taglist = {}
    for md_dir in tqdm.tqdm(glob.glob(os.path.join(post_dir, '*.md'))):
        basename = os.path.basename(md_dir)
        markdown = read_file(md_dir)
        try:
            post = PiperPost(basename, markdown)
        except Exception as e:
            raise Exception("parse '%s', %s" % (basename, e)) from None
        if post.tag_arr:
            for tag in post.tag_arr:
                if tag.name in local_taglist:
                    local_taglist[tag.name].append(post)
                else:
                    local_taglist[tag.name] = [post]
    return render(request, 'home/tag.html', {'posts': local_taglist[tag_name]})


# 标签列表
def taglist(request):
    post_dir = os.path.join(BASE_DIR, 'posts')
    local_taglist = {}
    count = 0
    for md_dir in tqdm.tqdm(glob.glob(os.path.join(post_dir, '*.md'))):
        basename = os.path.basename(md_dir)
        markdown = read_file(md_dir)
        try:
            post = PiperPost(basename, markdown)
        except Exception as e:
            raise Exception("parse '%s', %s" % (basename, e)) from None
        count += 1
        if post.tag_arr:
            for tag in post.tag_arr:
                if tag in local_taglist:
                    local_taglist[tag].append(post)
                else:
                    local_taglist[tag] = [post]

    sorted(local_taglist.items(), key= lambda x: x[0].last_modified_time, reverse=True)

    tags = {}
    for tag, posts in local_taglist.items():
        posts.sort(key=lambda p: p.last_modify_date, reverse=True)
        tags[tag.name] = posts

    return render(request, 'home/taglist.html', {'tags': tags})


# 项目
def projects(request):
    projects_dir = os.path.join(MENU_DIR, 'projects.md')
    basename = os.path.basename(projects_dir)
    markdown = read_file(projects_dir)
    post = OtherPost(basename, markdown)
    return render(request, 'home/post.html', {'post': post})


def post(request, title):
    post_dir = os.path.join(BASE_DIR, 'posts')
    for md_dir in tqdm.tqdm(glob.glob(os.path.join(post_dir, '*.md'))):
        basename = os.path.basename(md_dir)
        markdown = read_file(md_dir)
        try:
            post = PiperPost(basename, markdown)
            if post.title == title:
                return render(request, 'home/post.html', {'post': post})
        except Exception as e:
            raise Exception("parse '%s', %s" % (basename, e)) from None
    return render(request, 'home/e404.html')
