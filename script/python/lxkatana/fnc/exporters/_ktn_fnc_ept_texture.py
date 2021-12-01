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
    def _set_copy_as_src_(cls, target_tgt_dir_path, target_src_dir_path, fix_name_blank, use_tx):
        texture_reference_objs = ktn_dcc_objects.TextureReferences().get_objs()
        if texture_reference_objs:
            ps = utl_core.Progress.set_create(
                len(texture_reference_objs)
            )
            for obj in texture_reference_objs:
                utl_core.Progress.set_update(ps)
                for port_path, file_path in obj.reference_raw.items():
                    texture = utl_dcc_objects.OsFile(file_path)
                    texture_path = texture.path
                    target_texture_path = texture.get_target_file_path(target_tgt_dir_path, fix_name_blank=fix_name_blank)
                    if texture_path != target_texture_path:
                        # copy
                        exists_files = texture.get_exists_files()
                        for exists_file in exists_files:
                            exists_file.set_copy_as_src(
                                target_tgt_dir_path,
                                target_src_dir_path,
                                fix_name_blank=fix_name_blank
                            )
                        # repath
                        if use_tx is True:
                            target_texture_path = texture.get_target_file_path(
                                target_tgt_dir_path,
                                fix_name_blank=fix_name_blank,
                                ext_override='.tx'
                            )
                            if utl_dcc_objects.OsFile(target_texture_path).get_is_exists() is True:
                                target_texture_path = target_texture_path
                            else:
                                utl_core.Log.set_module_warning_trace(
                                    'texture-search',
                                    u'file="{}" is Non-exists'.format(target_texture_path)
                                )
                        #
                        port = obj.get_port(port_path)
                        ktn_dcc_objects.TextureReferences._set_real_file_path_(
                            port,
                            target_texture_path
                        )
            #
            utl_core.Progress.set_stop(ps)

    def set_run(self):
        fix_name_blank = self._option[self.FIX_NAME_BLANK]
        use_tx = self._option[self.USE_TX]
        self._set_copy_as_src_(
            self._tgt_dir_path, self._src_dir_path,
            fix_name_blank=fix_name_blank, use_tx=use_tx
        )
