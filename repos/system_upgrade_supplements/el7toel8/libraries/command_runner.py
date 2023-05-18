import subprocess


class CommandRunner(object):
    @staticmethod
    def call(args):
        return subprocess.call(args)
