from django.conf.urls import url
from . import views as piper_views

app_name = 'Piper'

urlpatterns = [
    url(r'^$', piper_views.index, name='index'),
    url(r'^about_me/$', piper_views.about_me, name='about_me'),
    url(r'^link/$', piper_views.link, name='link'),
    url(r'^projects/$', piper_views.projects, name='projects'),
    url(r'^archives/$', piper_views.archives, name='archives'),
    url(r'^tag/(?P<tag_name>.*)$', piper_views.tag, name='tag'),
    url(r'^taglist/$', piper_views.taglist, name='taglist'),
    url(r'^post/(?P<title>.*)$', piper_views.post, name='post'),
]