# coding:utf-8
import os


class Util(object):
    pass


class DataFile(object):
    NODE = '{}/.data/arnold_5-node.json'.format(os.path.dirname(__file__))
    GEOMETRY = '{}/.data/arnold_5-geometry.json'.format(os.path.dirname(__file__))
    MATERIAL = '{}/.data/arnold_5-material.json'.format(os.path.dirname(__file__))
