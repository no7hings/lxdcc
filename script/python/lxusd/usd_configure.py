# coding:utf-8
import os

import jinja2

from lxutil import utl_configure


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_PATH = '{}/.data'.format(ROOT)
    #
    SET_USDA_ARGUMENT_CONFIGURE_PATH = '{}/.data/set-usda-argument-configure.yml'.format(ROOT)


class ObjCategory(object):
    LYNXI = 'lynxi'


class ObjType(object):
    Xform = 'Xform'
    Mesh = 'Mesh'
    NurbsCurves = 'NurbsCurves'
    BasisCurves = 'BasisCurves'
    #
    GeometrySubset = 'GeomSubset'


class Obj(object):
    PATHSEP = '/'


class JinJa2(object):
    ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(Data.DATA_PATH)
    )
