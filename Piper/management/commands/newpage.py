from django.core.management.base import BaseCommand, CommandError
from PiperDjango.settings import BASE_DIR
from datetime import datetime
import os


PAGE_PRE_CONENT = {
    'title': '',
    'post_date': '',
    'last_modify_date': '',
    'tags': '',
}


class Command(BaseCommand):
    missing_args_message = 'Enter the page name which you want to create'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.post_dir = os.path.join(BASE_DIR, 'posts')
        if not os.path.exists(self.post_dir):
            os.mkdir(self.post_dir)

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='page_name', nargs='+')

    def handle(self, *args, **options):
        for page in args:
            page_dir = self.post_dir + '/' + page+'.md'
            if not os.path.exists(page_dir):
                with open(page_dir, 'a+') as fp:
                    for line in PAGE_PRE_CONENT:
                        if line == 'title':
                            fp.write('* ' + line + ': ' + page)
                        elif line == 'post_date':
                            fp.write('* ' + line + ': ' + datetime.fromtimestamp(os.path.getctime(page_dir)).strftime('%Y-%m-%d %H:%M:%S'))
                        elif line == 'last_modify_date':
                            fp.write('* ' + line + ': ' + datetime.fromtimestamp(os.path.getmtime(page_dir)).strftime('%Y-%m-%d %H:%M:%S'))
                        elif line == 'tags':
                            fp.write('* ' + line + ': ,')
                        fp.write('\n')
                    fp.write('---\n')
                    fp.write('your post\n')
            else :
                print('the page {0} is existed, please rename it'.format(page))
