import subprocess


def run_non_existing_bin(arg):
    return _subprocess_call(["/opt/non_existing/bin/run", arg])


def _subprocess_call(args):
    subprocess.call(args)
