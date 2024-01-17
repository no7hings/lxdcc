# coding:utf-8
name = 'lxdcc_rsc'

version = '0.0.111'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    import platform
    #
    env.LXDCC_RSC_BASE = '{root}'
    # resources
    env.PAPER_EXTEND_RESOURCES.append('{root}/script/python/.resources')
    # arnold
    env.ARNOLD_PLUGIN_PATH.append('{root}/script/python/.setup/arnold/shaders')
    # maya
    env.LYNXI_MAYA_RESOURCES.append('{root}/script/python/.setup/arnold/maya')
    if platform.system() == 'Linux':
        env.PAPER_EXTEND_RESOURCES.append('/job/CFG/SOFTWARE-CFG/clarisse/resource')
    elif platform.system() == 'Windows':
        env.PAPER_EXTEND_RESOURCES.append('X:/CFG/SOFTWARE-CFG/clarisse/resource')


timestamp = 1639363837

format_version = 2
