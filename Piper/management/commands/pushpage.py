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
        self.public_dir = os.path.join(BASE_DIR, 'public')
        self.remote_git = 'https://github.com/GeorgeWang1994/GeorgeWang1994.github.io.git'
        self.repo = Repo.init(path=BASE_DIR)

    def handle(self, **options):
        self.repo.git.status()
        config = self.repo.config_writer()
        config.set_value("user", "email", "georgewang1994@163.com")
        config.set_value("user", "name", "GeorgeWang1994")
        files = self.repo.git.diff(None, name_only=True)
        for f in files.split('\n'):
            self.repo.git.add(f)
            self.repo.git.commit('-m', 'first commit')
        self.repo.git.status(self.repo.heads.master)
        self.repo.git.push()
        print('----done----')