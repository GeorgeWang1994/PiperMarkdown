from django.db import models
from datetime import datetime
from .markdown import render_markdown
import re

class BasePost:
    # 文件名为  自己定义的内容|时间
    def __init__(self, basename, markdown):
        self.meta = {}
        self.header, self.body = re.split(r"\n-{3,}", markdown, 1)

        self.meta['body'] = self.body
        self.body_html = render_markdown(self.body)
        self.meta['body_html'] = self.body_html
        self.summary = self.body_html[:200]
        self.meta['summary'] = self.summary
        self._get_meta(self.header)

    def _get_meta(self, header):
        header = render_markdown(header)
        uls = re.match(r"<ul>(.*?)</ul>", header, re.S)
        lis = re.findall(r'<li>(.*?)</li>', uls.group(1), re.S)
        for li in lis:
            item = li.split(':', maxsplit=1)
            pre = item[0].strip()
            if pre == 'title':
                self.title = item[1].strip()
                self.meta['title'] = self.title
            elif pre == 'cover':
                self.cover = item[1].strip()
                self.meta['cover'] = self.cover
            elif pre == 'post_date':
                self.post_date = item[1].strip()
                self.meta['post_date'] = self.post_date
            elif pre == 'last_modify_date':
                self.last_modify_date = item[1].strip()
                self.meta['last_modify_date'] = self.last_modify_date
            elif pre == 'tags':
                self.tag_arr = []
                if item[1].strip() == '' or item[1].strip().find(',') == -1:
                    continue
                tags = item[1].strip().split(',')
                for tag in tags:
                    if tag is '':
                        continue
                    # obj = Tag.objects.filter(name=tag.strip())
                    # if obj is None:
                    #     print('add tag to database')
                    #     pass
                    # else:
                    #     print(tag)
                    tag = PiperTag(tag)
                    self.tag_arr.append(tag)
                self.meta['tags'] = self.tag_arr
            elif pre == 'can_comment':
                if item[1].strip() == 'True':
                    self.can_comment = True
                else:
                    self.can_comment = False
                self.meta['can_comment'] = self.can_comment
            elif pre == 'visible':
                if item[1].strip() == 'True':
                    self.visible = True
                else:
                    self.visible = False
                self.meta['visible'] = self.visible
            elif pre == 'passward':
                if item[1].strip() is not '':
                    self.pwd = item[1].strip()
                else:
                    self.pwd = ''
                self.meta['pwd'] = self.pwd
            elif pre == 'top':
                if item[1].strip() == 'True':
                    self.top = True
                else:
                    self.top = False
                self.meta['top'] = self.top
        return self.meta


# Piper post
class PiperPost(BasePost):
    def __init__(self, basename, markdown):
        super().__init__(basename, markdown)


# 其它 post
class OtherPost(BasePost):
    def __init__(self, basename, markdown):
        super().__init__(basename, markdown)


class PiperTag:
    def __init__(self, name):
        self.name = name
        self.created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_modified_time = self.created_time
