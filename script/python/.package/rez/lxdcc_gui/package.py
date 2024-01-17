# coding:utf-8
name = 'lxdcc_gui'

version = '0.0.106'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    env.LXDCC_GUI_BASE = '{root}'
    #
    env.PYTHONPATH.append('{root}/script/python')


timestamp = 1637923804

format_version = 2
