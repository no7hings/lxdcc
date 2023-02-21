# coding:utf-8
name = 'lxdcc'

version = '0.0.114'

description = ''

authors = ['']

tools = []

requires = [
    'lxdcc_lib',
    'lxdcc_gui',
    'lxdcc_rsc'
]


def commands():
    import platform
    #
    env.LXDCC_BASE = '{root}'
    env.LYNXI_SCHEME = 'default'
    env.LYNXI_CONFIGURES.append('{root}/script/configure')
    # bin
    env.PATH.append('{root}/script/bin')
    if platform.system() == 'Linux':
        env.PATH.append('{root}/script/bin/linux')
    elif platform.system() == 'Windows':
        env.PATH.append('{root}/script/bin/windows')
    # script
    env.PYTHONPATH.append('{root}/script/python')
    # resouces
    # env.LYNXI_RESOURCES.append('{root}/script/python/.resources')
    # startup in dcc
    # maya
    env.PYTHONPATH.append('{root}/script/python/.setup/maya/scripts')
    # houdini-setup
    env.HOUDINI_PATH.append('{root}/script/python/.setup/houdini:&')
    # katana-setup
    env.KATANA_RESOURCES.append('{root}/script/python/.setup/katana')
    # arnold-setup
    # env.ARNOLD_PLUGIN_PATH.append('{root}/script/python/.setup/arnold/shaders')
    # clarisse
    # env.CLARISSE_STARTUP_SCRIPT.append('{root}/script/python/.setup/clarisse/startup_script.py')


timestamp = 1639389924

format_version = 2
