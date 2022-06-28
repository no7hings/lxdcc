# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxmaya.dcc.dcc_objects as ma_dcc_objects

import lxmaya.modifiers as ma_modifiers

from lxarnold import and_core

from lxutil import utl_core


@ma_modifiers.set_undo_mark_mdf
def set_convert_tx_texture_to_origin():
    frs = ma_dcc_objects.FileReferences()
    nds = frs.get_objs()
    for i in nds:
        for port in i.get_file_ports():
            fph = port.get()
            f = utl_dcc_objects.OsTexture(fph)
            if f.get_ext_is_tx():
                org_fph = f.get_tx_orig_path()
                if org_fph is not None:
                    port.set(org_fph)


@ma_modifiers.set_undo_mark_mdf
def set_texture_color_spaces_switch():
    texture_reference_objs = ma_dcc_objects.TextureReferences().get_objs()
    if texture_reference_objs:
        ps = utl_core.Progress.set_create(len(texture_reference_objs))
        for texture_reference in texture_reference_objs:
            utl_core.Progress.set_update(ps)
            file_port = None
            if texture_reference.type == 'file':
                file_port = texture_reference.get_port('fileTextureName')
            elif texture_reference.type == 'aiImage':
                file_port = texture_reference.get_port('filename')
            #
            if file_port is not None:
                file_path = file_port.get()
                stg_file = utl_dcc_objects.OsFile(file_path)
                if stg_file.get_is_exists() is True:
                    color_space = and_core.AndTextureOpt(stg_file.path).get_color_space()
                    #
                    texture_reference.get_port('ignoreColorSpaceFileRules').set(True)
                    if color_space == 'sRGB':
                        aces_color_space = 'Utility - sRGB - Texture'
                    elif color_space == 'linear':
                        aces_color_space = 'Utility - Linear - sRGB'
                    else:
                        raise TypeError()
                    #
                    color_space_port = texture_reference.get_port('colorSpace')
                    #
                    if color_space_port.get() != color_space:
                        color_space_port.set(aces_color_space)
                        utl_core.Log.set_module_result_trace(
                            'color-space switch',
                            'obj="{}", color-space="{}"'.format(texture_reference.path, aces_color_space)
                        )
        #
        utl_core.Progress.set_stop(ps)


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

