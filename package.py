# coding:utf-8
name = 'lxdcc'

version = '0.0.114'

description = ''

authors = ['']

tools = []

requires = [
    'lxdcc_lib',
    'lxdcc_prd',
    'lxdcc_fnc',
    'lxdcc_gui',
    'lxdcc_rsc'
]


def commands():
    import platform
    # module
    env.PYTHONPATH.append('{root}/lib/python/module/python-2.7')
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
    # houdini
    env.HOUDINI_PATH.append('{root}/script/python/.setup/houdini:&')
    # katana
    env.KATANA_RESOURCES.append('{root}/script/python/.setup/katana')
    # arnold
    # env.ARNOLD_PLUGIN_PATH.append('{root}/script/python/.setup/arnold/shaders')


timestamp = 1639389924

format_version = 2
