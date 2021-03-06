# coding:utf-8
import copy

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class TextureExporter(object):
    FIX_NAME_BLANK = 'fix_name_blank'
    USE_TX = 'use_tx'
    OPTION = {
        FIX_NAME_BLANK: False,
        USE_TX: False,
    }
    def __init__(self, tgt_dir_path, src_dir_path, root=None, option=None):
        self._tgt_dir_path = tgt_dir_path
        self._src_dir_path = src_dir_path
        self._root = None
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self._option:
                    self._option[k] = v
    @classmethod
    def _set_copy_as_src_(cls, tgt_dir_path, src_dir_path, fix_name_blank, use_tx):
        objs = ktn_dcc_objects.TextureReferences().get_objs()
        if objs:
            copy_cache = []
            with utl_core.log_progress_bar(maximum=len(objs), label='texture export') as l_p:
                for i_obj in objs:
                    l_p.set_update()
                    for j_port_path, j_file_path in i_obj.reference_raw.items():
                        j_file_src = utl_dcc_objects.OsFile(j_file_path)
                        j_texture_path_src = j_file_src.path
                        # map path to current platform
                        j_texture_path_src = utl_core.Path.set_map_to_platform(j_texture_path_src)
                        j_file_src = utl_dcc_objects.OsFile(j_texture_path_src)
                        #
                        j_texture_path_tgt = j_file_src.get_target_file_path(tgt_dir_path, fix_name_blank=fix_name_blank)
                        if j_texture_path_src != j_texture_path_tgt:
                            # copy
                            j_file_tiles = j_file_src.get_exists_files()
                            for k_file_tile in j_file_tiles:
                                k_file_tile_path = k_file_tile.path
                                if k_file_tile_path not in copy_cache:
                                    copy_cache.append(k_file_tile_path)
                                    #
                                    k_file_tile.set_copy_as_src(
                                        tgt_dir_path,
                                        src_dir_path,
                                        fix_name_blank=fix_name_blank,
                                        force=True,
                                    )
                            # override to tx
                            if use_tx is True:
                                j_texture_tx_path_tgt = j_file_src.get_target_file_path(
                                    tgt_dir_path,
                                    fix_name_blank=fix_name_blank,
                                    ext_override='.tx'
                                )
                                if utl_dcc_objects.OsFile(j_texture_tx_path_tgt).get_is_exists() is True:
                                    j_texture_path_tgt = j_texture_tx_path_tgt
                                else:
                                    utl_core.Log.set_module_warning_trace(
                                        'texture search',
                                        u'file="{}" is non-exists'.format(j_texture_tx_path_tgt)
                                    )
                            #
                            j_port = i_obj.get_port(j_port_path)
                            ktn_dcc_objects.TextureReferences._set_real_file_path_(
                                j_port,
                                j_texture_path_tgt
                            )

    def set_run(self):
        fix_name_blank = self._option[self.FIX_NAME_BLANK]
        use_tx = self._option[self.USE_TX]
        self._set_copy_as_src_(
            self._tgt_dir_path, self._src_dir_path,
            fix_name_blank=fix_name_blank, use_tx=use_tx
        )
