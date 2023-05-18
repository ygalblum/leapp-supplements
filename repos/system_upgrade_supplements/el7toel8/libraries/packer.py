from collections import namedtuple
import os
import tarfile


class Packer(object):

    @staticmethod
    def pack(tarfile_path, packer_directories):
        with tarfile.open(name=tarfile_path, mode="w:gz") as tar:
            for directory in packer_directories:
                if os.path.exists(directory.path):
                    tar.add(directory.path, filter=directory.filter)

    @staticmethod
    def unpack(tarfile_path, destination_path):
        with tarfile.open(name=tarfile_path, mode="r") as tar:
            tar.extractall(destination_path)


PackerDirectory = namedtuple("PackerDirectory", ["path", "filter"])
