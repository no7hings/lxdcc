# coding:utf-8
import copy

import lxobj.core_objects as core_dcc_objects

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxmaya import ma_configure


class TextureExporter(object):
    FIX_NAME_BLANK = 'fix_name_blank'
    USE_TX = 'use_tx'
    WITH_REFERENCE = 'width_reference'
    #
    OPTION = {
        FIX_NAME_BLANK: False,
        USE_TX: False,
        WITH_REFERENCE: True
    }
    #
    def __init__(self, tgt_dir_path, src_dir_path, root=None, option=None):
        self._tgt_dir_path = tgt_dir_path
        self._src_dir_path = src_dir_path
        self._root = root
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self._option:
                    self._option[k] = v
    @classmethod
    def _set_copy_as_src_(cls, tgt_dir_path, src_dir_path, objs, fix_name_blank, use_tx, with_reference):
        if objs:
            copy_cache = []
            with utl_core.log_progress_bar(maximum=len(objs), label='texture export') as l_p:
                for obj in objs:
                    l_p.set_update()
                    for j_port_path, j_file_path in obj.reference_raw.items():
                        j_file = utl_dcc_objects.OsFile(j_file_path)
                        j_texture_path_src = j_file.path
                        # map path to current platform
                        j_texture_path_src = utl_core.Path.set_map_to_platform(j_texture_path_src)
                        j_file = utl_dcc_objects.OsFile(j_texture_path_src)
                        #
                        j_texture_path_tgt = j_file.get_target_file_path(
                            tgt_dir_path,
                            fix_name_blank=fix_name_blank
                        )
                        if j_texture_path_src != j_texture_path_tgt:
                            # copy
                            j_file_tiles = j_file.get_exists_files()
                            if j_file_tiles:
                                for k_file_tile in j_file_tiles:
                                    k_file_tile_path = k_file_tile.path
                                    if k_file_tile_path not in copy_cache:
                                        copy_cache.append(k_file_tile_path)
                                        k_file_tile.set_copy_as_src(
                                            tgt_dir_path,
                                            src_dir_path,
                                            fix_name_blank=fix_name_blank,
                                            force=True
                                        )
                            else:
                                utl_core.Log.set_module_warning_trace(
                                    'texture search',
                                    u'file="{}" is Non-exists'.format(j_texture_path_src)
                                )
                                continue
                            # repath
                            if use_tx is True:
                                j_texture_tx_path_tgt = j_file.get_target_file_path(
                                    tgt_dir_path,
                                    fix_name_blank=fix_name_blank,
                                    ext_override='.tx'
                                )
                                if utl_dcc_objects.OsFile(j_texture_tx_path_tgt).get_is_exists() is True:
                                    j_texture_path_tgt = j_texture_tx_path_tgt
                                else:
                                    utl_core.Log.set_module_warning_trace(
                                        'texture-tx search',
                                        u'file="{}" is Non-exists'.format(j_texture_tx_path_tgt)
                                    )
                            #
                            tgt_texture_file_obj = utl_dcc_objects.OsFile(j_texture_path_tgt)
                            if tgt_texture_file_obj.get_exists_files():
                                port = obj.get_port(j_port_path)
                                if port.get() != j_texture_path_tgt:
                                    port.set(j_texture_path_tgt)
                                    utl_core.Log.set_module_result_trace(
                                        'texture repath',
                                        u'"{}" >> "{}"'.format(j_texture_path_src, j_texture_path_tgt)
                                    )
                            else:
                                utl_core.Log.set_module_warning_trace(
                                    'texture search',
                                    u'file="{}" is Non-exists'.format(j_texture_path_tgt)
                                )
    #
    def set_run(self):
        fix_name_blank = self._option[self.FIX_NAME_BLANK]
        use_tx = self._option[self.USE_TX]
        with_reference = self._option[self.WITH_REFERENCE]
        #
        root = self._root
        #
        root_dag_path = core_dcc_objects.ObjDagPath(root)
        root_mya_dag_path = root_dag_path.set_translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        #
        root_mya_obj = mya_dcc_objects.Group(root_mya_dag_path.path)
        if root_mya_obj.get_is_exists() is True:
            objs = root_mya_obj.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(objs)
            includes = objs_look_opt.get_texture_reference_paths()
            if includes:
                objs = mya_dcc_objects.TextureReferences._get_objs_(includes)
                #
                self._set_copy_as_src_(
                    self._tgt_dir_path, self._src_dir_path,
                    objs=objs,
                    fix_name_blank=fix_name_blank,
                    use_tx=use_tx,
                    with_reference=with_reference
                )
