# coding:utf-8
import sys

argv = sys.argv

fnc, args = argv[1], argv[2]


def set_scene_new():
    # noinspection PyUnresolvedReferences
    from Katana import KatanaFile

    from lxbasic import bsc_core

    file_path = args

    bsc_core.StorageFileOpt(file_path).set_directory_create()
    KatanaFile.New()
    KatanaFile.Save(file_path)


if __name__ == '__main__':
    eval('{}()'.format(fnc))
