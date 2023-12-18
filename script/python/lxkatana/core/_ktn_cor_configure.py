# coding:utf-8
import os


class KtnBase(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))

    DATA_ROOT = '{}/.data'.format(ROOT)


class Util(object):
    OBJ_PATHSEP = '/'
    PORT_PATHSEP = '.'
