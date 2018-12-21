import os


class DirMaker:

    def __init__(self, path,*args):
        self.dir_ls = args
        self.path = path

    def make_dirs(self):
        for d in self.dir_ls:
            os.mkdir(self.path + d)
