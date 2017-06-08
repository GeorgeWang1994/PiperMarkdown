from django.core.management.base import BaseCommand
from PiperDjango.settings import GIT_CONFIG, BASE_DIR
from git import Repo
import os.path


class Command(BaseCommand):
    help = (
        "push the page to github",
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.pro_dir = os.path.join(BASE_DIR, GIT_CONFIG["GIT_REPO"])

    def handle(self, **options):
        if not os.path.exists(self.pro_dir):
            print('Please init first')
            return

        repo = Repo.init(path=self.pro_dir)
        repo.git.status()
        config = repo.config_writer()
        config.set_value("user", "email", "georgewang1994@163.com")
        config.set_value("user", "name", "GeorgeWang1994")
        files = repo.git.diff(None, name_only=True)
        for f in files.split('\n'):
            repo.git.add(f)
            repo.git.commit('-m', 'commit')
        repo.git.status(repo.heads.master)
        repo.git.push()
        print('----done----')