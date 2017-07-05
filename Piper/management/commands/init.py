from django.core.management.base import BaseCommand
from PiperDjango.settings import BASE_DIR, GIT_CONFIG
from Piper.select_result import removeFolders
import os.path, git


class Command(BaseCommand):
    help = (
        "Can be run as a cronjob or directly to clean out expired sessions "
        "(only with the database backend at the moment)."
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.pro_dir = os.path.join(BASE_DIR, GIT_CONFIG["GIT_REPO"])

    def handle(self, **options):
        print("waiting...")
        try:
            if os.path.exists(self.pro_dir):
                repo = git.Repo(self.pro_dir)
                repo.remotes.origin.pull()
            else:
                git.Repo.clone_from(GIT_CONFIG['GIT'], self.pro_dir)
        except Exception as err:
            print(err)
        print("init done!")
