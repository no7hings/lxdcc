# coding:utf-8


def set_texture_tiles_repair():
    import glob
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    # noinspection PyUnresolvedReferences
    import maya.mel as mel
    #
    import platform
    #
    fs = cmds.ls(type='file')
    #
    for i in fs:
        i_m = cmds.getAttr('{}.uvTilingMode'.format(i))
        if i_m == 3:
            i_v = cmds.getAttr('{}.fileTextureName'.format(i))
            if '<UDIM>' in i_v:
                if platform.system() == 'Windows':
                    i_v = i_v.replace('\\', '/')
                    for j_0, j_1 in [('/l/', 'L:/')]:
                        if i_v.startswith(j_0):
                            i_v = j_1 + i_v[len(j_0):]
                elif platform.system() == 'Linux':
                    for j_0, j_1 in [('L:/', '/l/'), ('l:/', '/l/')]:
                        if i_v.startswith(j_0):
                            i_v = j_1 + i_v[len(j_0):]
                #
                i_results = glob.glob(i_v.replace('<UDIM>', '[0-9]' * 4))
                if i_results:
                    cmds.setAttr(
                        '{}.fileTextureName'.format(i), i_results[0], type='string'
                    )
                    print 'repair "{}" tile mode'.format(i)
    #
    for i in fs:
        mel.eval('generateUvTilePreview {}'.format(i))


if __name__ == '__main__':
    set_texture_tiles_repair()

