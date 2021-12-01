# coding:utf-8
import os


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    LOOK_KATANA_WORKSPACE_CONFIGURE_PATH = '{}/.data/look-katana-workspace-configure.yml'.format(ROOT)


class Util(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
