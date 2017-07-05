#-*- coding:utf-8 –*-
from django.core.management.base import BaseCommand
from PiperDjango.settings import GIT_CONFIG, BASE_DIR
from git import Repo
import os.path
import pprint


class NewRepo(Repo):
    """add some convenience methods to git.Repo"""

    def commit_all(self, msg, author=None):
        """commit the changes that have been made in the repository.
            msg = the commit message
            author = a git.util.Actor(name, email)
        """
        if self.is_dirty()!=True:
            return False
        else:
            changed_files = self.untracked_files \
                        + [diff.a_blob.path for diff in self.index.diff(None)
                            if os.path.exists(diff.a_blob.abspath)]
            if len(changed_files) > 0:
                self.index.add(changed_files)

            deleted_files = [diff.a_blob.path for diff in self.index.diff(None)
                                if not os.path.exists(diff.a_blob.abspath)]
            print(deleted_files)
            if len(deleted_files) > 0:
                self.index.remove(deleted_files)

            self.index.commit(msg, author=author)


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

        print("wait...")

        repo = NewRepo.init(path=self.pro_dir)
        repo.git.status()
        config = repo.config_writer()
        config.set_value("user", "email", GIT_CONFIG["GIT_EMAIL"])
        config.set_value("user", "name", GIT_CONFIG["GIT_USERNAME"])

        repo.commit_all("commit")

        # files = repo.git.diff(None, name_only=True)
        # files = files.split('\n')
        #
        # try:
        #     for f in files:
        #         print(f)
        #         continue
        #         repo.git.add(f)
        #         repo.git.commit('-m', 'commit')
        #     repo.git.status(repo.heads.master)
        #     repo.git.push()
        #     print("deploy done!")
        # except Exception as e:
        #     pprint.pprint(e)
        #     print("deploy error!")