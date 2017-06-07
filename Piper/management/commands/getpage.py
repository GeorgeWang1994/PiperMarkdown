from django.core.management.base import BaseCommand
from PiperDjango.settings import BASE_DIR, STATIC_ROOT, MENU_DIR, BLOG_CONFIG
from Piper.select_result import read_file, write_file, removeFolders, copyFiles
from Piper.models import PiperPost, OtherPost
from django.template.loader import get_template
import os.path, tqdm, glob


class Command(BaseCommand):
    help = (
        "Can be run as a cronjob or directly to clean out expired sessions "
        "(only with the database backend at the moment)."
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.post_dir = os.path.join(BASE_DIR, 'posts')

        self.index_template = get_template('home/index.html')
        self.post_template = get_template('home/post.html')
        self.taglist_template = get_template('home/taglist.html')
        self.tag_template = get_template('home/tag.html')
        self.notfound_template = get_template('home/e404.html')
        self.archives_template = get_template('home/archives.html')

    def handle(self, **options):

        if os.path.exists(BASE_DIR + '/public'):
            removeFolders(BASE_DIR + '/public')
        os.mkdir(BASE_DIR + '/public')

        self.public_dir = os.path.join(BASE_DIR, 'public')

        os.mkdir(self.public_dir + '/static')
        copyFiles(STATIC_ROOT, self.public_dir + '/static')

        os.mkdir(os.path.join(self.public_dir, 'posts'))
        self.public_post_dir = os.path.join(self.public_dir, 'posts')

        self.posts = []
        for md_dir in tqdm.tqdm(glob.glob(os.path.join(self.post_dir, '*.md'))):
            basename = os.path.basename(md_dir)
            markdown = read_file(md_dir)
            try:
                post = PiperPost(basename, markdown)
            except Exception as e:
                raise Exception("parse '%s', %s" % (basename, e)) from None
            self.posts.append(post)

        sorted(self.posts, key=lambda d: d.post_date, reverse=True)

        self.handleIndex()
        self.handleOther()
        self.handleArchives()
        self.handleTagList()
        self.handlePost()

    # 渲染主界面
    def handleIndex(self):
        post_html = self.index_template.render(context={'posts': self.posts,
                                                        'recents': self.posts[:5], 'BLOG_CONFIG': BLOG_CONFIG})
        write_file(os.path.join(self.public_dir, 'index.html'), post_html)

    # 渲染关于/链接/项目
    def handleOther(self):
        urls = ['about_me', 'link', 'projects']
        files = ['about-me.md', 'links.md', 'projects.md']
        for i, file in enumerate(files):
            file_dir = os.path.join(self.public_dir, urls[i])
            os.mkdir(file_dir)
            markdown = read_file(os.path.join(MENU_DIR, file))
            post = OtherPost(file[:-3], markdown)
            file_html = self.post_template.render(context={'post': post, 'BLOG_CONFIG': BLOG_CONFIG})
            write_file(os.path.join(file_dir, 'index.html'), file_html)

    # 渲染目录
    def handleArchives(self):
        file_dir = os.path.join(self.public_dir, 'archives')
        os.mkdir(file_dir)

        local_archives = {}
        count = 0

        for post in self.posts:
            year = post.last_modify_date.split('-')[0]
            count += 1
            if year in local_archives:
                local_archives[year].append(post)
            else:
                local_archives[year] = [post]

        # 排序
        local_archives = sorted(local_archives.items(), key=lambda x: x[0], reverse=True)
        file_html = self.archives_template.render(context={'archives': local_archives,
                                                           'count': count, 'BLOG_CONFIG': BLOG_CONFIG})
        write_file(os.path.join(file_dir, 'index.html'), file_html)

    # 渲染标签列表
    def handleTagList(self):
        file_dir = os.path.join(self.public_dir, 'taglist')
        os.mkdir(file_dir)

        local_taglist = {}
        for post in self.posts:
            if post.tag_arr:
                for tag in post.tag_arr:
                    if tag.name in local_taglist:
                        if post not in local_taglist[tag.name]:
                            local_taglist[tag.name].append(post)
                    else:
                        local_taglist[tag.name] = [post]

        tags = {}
        for tagname, posts in local_taglist.items():
            posts.sort(key=lambda p: p.last_modify_date, reverse=True)
            tags[tagname] = posts

            tag_file_dir = os.path.join(file_dir, tagname)
            os.mkdir(tag_file_dir)

            tag_file_html = self.tag_template.render(context={'name': tagname,
                                                              'posts': posts, 'BLOG_CONFIG': BLOG_CONFIG})
            write_file(os.path.join(tag_file_dir, 'index.html'), tag_file_html)

            for post in posts:
                post_html_dir = os.path.join(tag_file_dir, post.title)
                os.mkdir(post_html_dir)
                post_html = self.post_template.render(context={'post': post, 'BLOG_CONFIG': BLOG_CONFIG})
                write_file(os.path.join(post_html_dir, 'index.html'), post_html)

        file_html = self.taglist_template.render(context={'tags': tags, 'BLOG_CONFIG': BLOG_CONFIG})
        write_file(os.path.join(file_dir, 'index.html'), file_html)


    # 渲染文章
    def handlePost(self):
        for post in self.posts:
            post_html_dir = os.path.join(self.public_post_dir, post.title)
            os.mkdir(post_html_dir)
            post_html = self.post_template.render(context={'post': post, 'BLOG_CONFIG': BLOG_CONFIG})
            write_file(os.path.join(post_html_dir, 'index.html'), post_html)