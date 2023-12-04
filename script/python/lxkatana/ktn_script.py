# coding:utf-8
import sys

argv = sys.argv

fnc, args = argv[1], argv[2]


def set_scene_new():
    # noinspection PyUnresolvedReferences
    from Katana import KatanaFile

    import lxbasic.core as bsc_core

    file_path = args

    bsc_core.StgFileOpt(file_path).create_directory()
    KatanaFile.New()
    KatanaFile.Save(file_path)


if __name__ == '__main__':
    eval('{}()'.format(fnc))
