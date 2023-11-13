# coding:utf-8
from lxusd.warp import *

import os

import jinja2

import lxuniverse.configure as unr_configure


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


class Type(object):
    if USD_FLAG is True:
        MAPPER = {
            unr_configure.Type.CONSTANT_BOOLEAN: Sdf.ValueTypeNames.Bool,
            unr_configure.Type.CONSTANT_INTEGER: Sdf.ValueTypeNames.Int,
            unr_configure.Type.CONSTANT_FLOAT: Sdf.ValueTypeNames.Float,
            unr_configure.Type.CONSTANT_STRING: Sdf.ValueTypeNames.String,
            #
            unr_configure.Type.COLOR_COLOR3: Sdf.ValueTypeNames.Color3f,
            unr_configure.Type.ARRAY_COLOR3: Sdf.ValueTypeNames.Color3fArray,
            #
            unr_configure.Type.ARRAY_STRING: Sdf.ValueTypeNames.StringArray,
        }


class JinJa2(object):
    ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(Data.DATA_PATH)
    )
