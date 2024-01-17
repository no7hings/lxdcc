# coding:utf-8
name = 'lxdcc_lib'

version = '0.0.15'

description = ''

authors = ['']

tools = []

requires = []


def commands():
    import platform
    #
    env.LXDCC_LIB_BASE = '{root}'
    #
    env.PYTHONPATH.append('{root}/lib/python-2.7/site-packages')
    #
    if platform.system() == 'Linux':
        env.PYTHONPATH.append('{root}/lib/linux-python-2.7/site-packages')
        env.PYTHONPATH.append('{root}/lib/linux-x64-python-2.7/site-packages')
    else:
        env.PYTHONPATH.append('{root}/lib/windows-python-2.7/site-packages')
        env.PYTHONPATH.append('{root}/lib/windows-x64-python-2.7/site-packages')


timestamp = 1608028331

format_version = 2
