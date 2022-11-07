# coding:utf-8
import os


class Setup(object):
    def __init__(self):
        pass

    def run(self):
        print 'lx-dcc menu setup: is started'
        from lxclarisse import crs_concifgure, crs_setup
        crs_setup.MenuBuilder._create_by_yaml_(
            '{}/menus.yml'.format(
                crs_concifgure.Root.DATA
            )
        )
        print 'lx-dcc menu setup: is completed'


if __name__ == '__main__':
    Setup().run()
