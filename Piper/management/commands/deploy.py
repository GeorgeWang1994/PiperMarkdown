#-*- coding:utf-8 –*-
from django.core.management.base import BaseCommand
from PiperDjango.settings import GIT_CONFIG, BASE_DIR
from git import Repo
import os.path
import pprint


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
        config.set_value("user", "email", GIT_CONFIG["GIT_EMAIL"])
        config.set_value("user", "name", GIT_CONFIG["GIT_USERNAME"])
        files = repo.git.diff(None, name_only=True)
        files = files.split('\n')

        try:
            for f in files:
                repo.git.add(f)
                repo.git.commit('-m', 'commit')
            repo.git.status(repo.heads.master)
            repo.git.push()
            print('----done----')
        except Exception as e:
            pprint.pprint(e)
            print('----error----')