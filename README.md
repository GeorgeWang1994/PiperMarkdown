# PiperMarkdown

Blog for Django1.11，Python 3.6，based on Markdown，[网址](https://github.com/GeorgeWang1994/PiperMarkdown)，希望大家能给个star，谢谢！

# 什么是PiperMarkdown

这是一个快速、简洁而且高效的博客，它基于Django1.11，并且使用了高效的`mistune` Markdown渲染引擎来解析文章，参考了一位博主的博客的CSS样式。

![](http://odwv9d2u8.bkt.clouddn.com/17-7-6/92051778.jpg)

# 特点

## 一键部署

只需要一条指令就可以将你的代码上传到Github Pages。

## 支持Markdown

支持Markdown的语法。

## 更快的渲染速度

使用了`mistune` 渲染引擎，目前这个渲染引擎也是最快的，具体参考[这篇文章](http://lepture.com/en/2014/markdown-parsers-in-python)。

# 如何使用

1. 在settting文件中进行配置；
2. `python3 run manage.py init` 进行初始化；
3. `python3 run manage.py newpage` 创建新的md文件；
4. `python3 run manage.py getpage` 渲染所有文件；
5. `python3 run manage.py deploy` 将你的代码上传到Github；

# 注意事项

1. 在用命令行操作的时候，先进行初始化；
2. 拉取项目的速度取决于你的网速；
3. 使用一键部署可能还有点问题；
4. 等待补充；
