# coding:utf-8


def get_exists_map():
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    return cmds.dirmap(getAllMappings=1)


def set_directory_map_create():
    import platform
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    #
    if platform.system() == 'Windows':
        map_dict = {
            'L:': ['/l', r'\l'],
            'L:/prod': ['/prod'],
            'O:': ['/o'],
            'Q:': ['/depts:']
        }
    elif platform.system() == 'Linux':
        map_dict = {
            '/l': ['l:', 'L:'],
            '/o': ['o:', 'O:'],
            '/depts': ['q:', 'Q:']
        }
    else:
        raise TypeError()
    #
    print 'directory remap: start'
    cmds.dirmap(enable=1)
    for k, v in map_dict.items():
        for i in v:
            print 'create directory map: "{}" >> "{}"'.format(i, k)
            cmds.dirmap(mapDirectory=(i, k))
    print 'directory remap: complete'
