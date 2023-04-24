# coding:utf-8
import os


class Setup(object):
    def __init__(self):
        pass

    def run(self):
        print 'lx-dcc menu setup: is started'
        from lxbasic import bsc_core

        from lxclarisse import crs_setup

        crs_setup.MenuSetup._create_by_yaml_(
            bsc_core.CfgFileMtd.get_yaml('clarisse/gui/menu')
        )
        print 'lx-dcc menu setup: is completed'


if __name__ == '__main__':
    Setup().run()
