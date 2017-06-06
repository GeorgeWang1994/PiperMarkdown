from PiperDjango.settings import BLOG_CONFIG


def global_setting(request):
    return {'BLOG_CONFIG': BLOG_CONFIG}
