# coding:utf-8
import os


class Root(object):
    MAIN = os.path.dirname(__file__.replace('\\', '/'))
    DATA = '{}/.data'.format(MAIN)


class Data(object):
    MAIN = os.path.dirname(__file__.replace('\\', '/'))
    DATA = '{}/.data'.format(MAIN)
    #
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    LOOK_KATANA_WORKSPACE_CONFIGURE_PATH = '{}/.data/look-katana-workspace-configure.yml'.format(ROOT)

    SCRIPT_FILE = '{}/ktn_script.py'.format(ROOT)


class DataFile(object):
    TEXTURE_RESOURCE_SHADER_GROUP_CONFIGURE = '{}/texture-resource-shader-group-configure.yml'.format(Root.DATA)


class Util(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
