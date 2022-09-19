# coding:utf-8
import copy

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil.fnc import utl_fnc_obj_abs

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class TextureExporter(
    utl_fnc_obj_abs.AbsDccTextureExport
):
    FIX_NAME_BLANK = 'fix_name_blank'
    USE_TX = 'use_tx'
    WITH_REFERENCE = 'width_reference'
    OPTION = {
        FIX_NAME_BLANK: False,
        USE_TX: False,
        WITH_REFERENCE: True,
        'ignore_missing_texture': False,
    }
    def __init__(self, tgt_dir_path, src_dir_path, root=None, option=None):
        self._directory_path_dst = tgt_dir_path
        self._directory_path_base = src_dir_path
        self._root = None
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self._option:
                    self._option[k] = v

    def set_run(self):
        asset_workspace = ktn_dcc_objects.AssetWorkspace()
        #
        location = asset_workspace.get_geometry_location()
        #
        fix_name_blank = self._option[self.FIX_NAME_BLANK]
        use_tx = self._option[self.USE_TX]
        with_reference = self._option[self.WITH_REFERENCE]
        #
        texture_references = ktn_dcc_objects.TextureReferences()
        dcc_shaders = asset_workspace.get_all_dcc_geometry_shader_by_location(location)
        dcc_objs = texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        self._set_copy_as_src_(
            directory_path_dst=self._directory_path_dst, 
            directory_path_base=self._directory_path_base,
            dcc_objs=dcc_objs,
            fix_name_blank=fix_name_blank,
            use_tx=use_tx,
            with_reference=with_reference,
            ignore_missing_texture=True,
            remove_expression=True,
            use_environ_map=True,
            repath_fnc=texture_references.set_obj_repath_to,
        )
