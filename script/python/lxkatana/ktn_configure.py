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

    SCRIPT_FILE = '{}/ktn_script.py'.format(ROOT)


class Util(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
