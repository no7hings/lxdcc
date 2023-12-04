# coding:utf-8
import glob

import os

import fnmatch

import collections

import lxbasic.core as bsc_core

from lxutil import utl_core

import lxutil.abstracts as utl_abstracts

import lxutil.dcc.dcc_objects as utl_dcc_objects

import multiprocessing

CPU_COUNT = multiprocessing.cpu_count()


class DccTexturesOpt(object):
    def __init__(self, texture_references, includes=None, force=False):
        self._exts = []
        self._texture_references = texture_references
        if isinstance(includes, (tuple, list)):
            self._objs = includes
        else:
            self._objs = self._texture_references.get_objs()
        #
        self._force = force

    @classmethod
    def _get_tx_action_queue_(cls, objs, force=False, check_exists=True):
        tx_create_queue = []
        tx_repath_queue = []
        #
        if objs:
            for obj in objs:
                for j_port_path, j_file_path in obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(j_file_path)
                    if i_texture.get_ext_is_tx() is True:
                        i_texture_orig = i_texture.get_tx_orig()
                        i_texture_tx = i_texture
                    else:
                        i_texture_tx = i_texture.get_as_tx()
                        #
                        i_port = obj.get_port(j_port_path)
                        if check_exists is True:
                            tx_repath_queue.append(
                                (i_port, i_texture_tx)
                            )
                        else:
                            tx_repath_queue.append(
                                (i_port, (i_texture, i_texture_tx))
                            )
                        i_texture_orig = i_texture
                    #
                    if force is True:
                        i_texture_tx.set_delete()
                    #
                    if i_texture_orig is not None:
                        if i_texture_orig not in tx_create_queue:
                            tx_create_queue.append(i_texture_orig)
                    else:
                        bsc_core.Log.trace_method_warning(
                            'texture-tx create',
                            u'file="{}" orig is non-exists'.format(j_file_path)
                        )
        return tx_create_queue, tx_repath_queue

    #
    def set_tx_repath(self, check_exists=True):
        tx_create_queue, tx_repath_queue = self._get_tx_action_queue_(
            self._objs, check_exists=check_exists
        )
        return self._set_repath_queue_run_(tx_repath_queue)

    def set_tx_create_and_repath(self, force=False, check_exists=True):
        tx_create_queue, tx_repath_queue = self._get_tx_action_queue_(
            self._objs, force=force
        )
        self._set_tx_create_queue_run_(tx_create_queue)
        self._set_repath_queue_run_(tx_repath_queue)

    @classmethod
    def _set_tx_create_queue_run_(cls, queue):
        if queue:
            with bsc_core.LogProcessContext.create(maximum=len(queue), label='texture-tx create') as l_p:
                for i_texture_src in queue:
                    l_p.do_update()
                    if i_texture_src.get_is_exists_as_tx() is False:
                        i_texture_tiles = i_texture_src.get_exists_units()
                        if i_texture_tiles:
                            for j_texture_tile in i_texture_tiles:
                                if j_texture_tile.get_is_exists_as_tx() is False:
                                    utl_dcc_objects.OsTexture._set_unit_tx_create_by_src_(
                                        j_texture_tile.path,
                                        block=True
                                    )
                                    bsc_core.Log.trace_method_result(
                                        'texture-tx create',
                                        u'file="{}"'.format(j_texture_tile.path)
                                    )

    @classmethod
    def _get_jpg_action_queue_(cls, objs, force=False, check_exists=True):
        jpg_create_queue = []
        jpg_repath_queue = []
        #
        ext_tgt = '.jpg'
        #
        if objs:
            for obj in objs:
                for j_port_path, j_file_path in obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(j_file_path)
                    if i_texture.get_ext_is(ext_tgt) is True:
                        i_tgt_ext_texture_orig = i_texture.get_orig_as_tgt_ext(ext_tgt)
                        i_tgt_ext_texture = i_texture
                    else:
                        i_tgt_ext_texture = i_texture.get_as_tgt_ext(ext_tgt)
                        #
                        i_port = obj.get_port(j_port_path)
                        if check_exists is True:
                            jpg_repath_queue.append(
                                (i_port, i_tgt_ext_texture)
                            )
                        else:
                            jpg_repath_queue.append(
                                (i_port, (i_texture, i_tgt_ext_texture))
                            )
                        i_tgt_ext_texture_orig = i_texture
                    #
                    if force is True:
                        i_tgt_ext_texture.set_delete()
                    #
                    if i_tgt_ext_texture_orig is not None:
                        jpg_create_queue.append(i_tgt_ext_texture_orig)
                    else:
                        bsc_core.Log.trace_method_warning(
                            'texture-jpg create',
                            u'file="{}" orig is non-exists'.format(j_file_path)
                        )
        return jpg_create_queue, jpg_repath_queue

    def set_jpg_repath(self, check_exists=True):
        jpg_create_queue, jpg_repath_queue = self._get_jpg_action_queue_(
            self._objs, check_exists=check_exists
        )
        return self._set_repath_queue_run_(jpg_repath_queue)

    def set_jpg_create_and_repath(self, force=False):
        jpg_create_queue, jpg_repath_queue = self._get_jpg_action_queue_(
            self._objs, force=force
        )
        self._set_jpg_create_queue_run_(jpg_create_queue)
        self._set_repath_queue_run_(jpg_repath_queue)

    @classmethod
    def _set_jpg_create_queue_run_(cls, queue):
        if queue:
            with bsc_core.LogProcessContext.create(maximum=len(queue), label='texture-jpg create') as l_p:
                for i_texture in queue:
                    l_p.do_update()
                    if i_texture.get_is_exists_as_tx() is False:
                        i_texture_tiles = i_texture.get_exists_units()
                        if i_texture_tiles:
                            for j_texture_tile in i_texture_tiles:
                                utl_dcc_objects.OsTexture._set_unit_jpg_create_(
                                    j_texture_tile.path, block=True
                                )

    @classmethod
    def _set_copy_queue_run_(cls, queue):
        bsc_core.Log.trace_method_result(
            'texture copy',
            'start'
        )
        if queue:
            g_p = bsc_core.LogProcessContext(
                maximum=len(queue)
            )
            for i_src_stg_file, i_tgt_stg_file in queue:
                g_p.do_update()
                i_src_stg_file.set_copy_to_file(
                    i_tgt_stg_file.path
                )
            #
            g_p.set_stop()
        #
        bsc_core.Log.trace_method_result(
            'texture copy',
            'complete'
        )

    def _set_repath_queue_run_(self, queue, force=False):
        bsc_core.Log.trace_method_result(
            'texture repath',
            'start'
        )
        if queue:
            with bsc_core.LogProcessContext.create(maximum=len(queue), label='texture repath') as g_p:
                for i_port, i_args in queue:
                    g_p.do_update()
                    #
                    if isinstance(i_args, (tuple, list)):
                        check_file_obj, tgt_stg_file = i_args
                    else:
                        check_file_obj = tgt_stg_file = i_args
                    #
                    if check_file_obj.get_exists_units() or force is True:
                        self._set_port_repath_(i_port, tgt_stg_file)
                        color_space = tgt_stg_file.get_color_space_src()
                        if tgt_stg_file.get_exists_units() is True:
                            i_port.obj.set_color_space(color_space)
                    else:
                        bsc_core.Log.trace_method_warning(
                            'texture repath',
                            u'file="{}" is non-exists'.format(tgt_stg_file.path)
                        )
            #
            g_p.set_stop()
            #
            self._set_repath_post_run_()
        #
        bsc_core.Log.trace_method_result(
            'texture repath',
            'complete'
        )

    @bsc_core.Modifiers.run_as_ignore
    def _set_repath_post_run_(self):

        if bsc_core.ApplicationMtd.get_is_maya():
            import lxmaya.commands as mya_commands

            #
            mya_commands.set_texture_tiles_repair()

    def _set_port_repath_(self, port, stg_texture):
        self._texture_references._set_real_file_path_(
            port,
            stg_texture.path
        )
        bsc_core.Log.trace_method_result(
            'texture repath',
            u'attribute="{}", file="{}"'.format(port.path, stg_texture.path)
        )

    def set_check(self):
        pass

    def set_repair(self, use_deferred=False):
        return self.set_tx_create_and_repath()

    @classmethod
    def _get_search_dict_(cls, target_directory_paths):
        def _rcs_fnc(path_):
            _results = glob.glob(u'{}/*'.format(path_)) or []
            _results.sort()
            for _path in _results:
                if os.path.isfile(_path):
                    _directory_path = os.path.dirname(_path)
                    _name = os.path.basename(_path)
                    _name_base, _ext = os.path.splitext(_name)
                    #
                    _name_base_key = _name_base
                    _ext_key = _ext
                    #
                    if _name_base_key in search_dict:
                        _ext_search_dict = search_dict[_name_base_key]
                    else:
                        _ext_search_dict = {}
                        search_dict[_name_base_key] = _ext_search_dict
                    #
                    if _ext_key in _ext_search_dict:
                        _matches = _ext_search_dict[_ext_key]
                    else:
                        _matches = []
                        _ext_search_dict[_ext_key] = _matches
                    #
                    _matches.append(
                        (_directory_path, _name_base, _ext)
                    )
                elif os.path.isdir(_path):
                    _rcs_fnc(_path)

        search_dict = {}
        [_rcs_fnc(i) for i in target_directory_paths]
        return search_dict

    def set_search_from(self, target_directory_paths, ignore_source_resolved=True):
        objs = self._objs
        #
        repath_queue = []
        #
        search_dict = self._get_search_dict_(target_directory_paths)
        #
        if objs:
            g_p = bsc_core.LogProcessContext(
                maximum=len(objs)
            )
            for i_obj in objs:
                g_p.do_update()
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(j_file_path)
                    #
                    i_name_base_src = i_texture.name_base
                    i_ext_src = i_texture.ext
                    #
                    i_ext_key_src = i_ext_src.lower()
                    #
                    search_name_bases = search_dict.keys()
                    name_base_fnmatch_pattern = bsc_core.PtnMultiplyFileMtd.to_fnmatch_style(i_name_base_src)
                    #
                    match_name_base_keys = fnmatch.filter(search_name_bases, name_base_fnmatch_pattern)
                    if match_name_base_keys:
                        tgt_name_base = match_name_base_keys[0]
                        ext_search_dict = search_dict[tgt_name_base]
                        #
                        search_ext_keys = ext_search_dict.keys()
                        if i_ext_key_src in search_ext_keys:
                            search_ext_keys.remove(i_ext_key_src)
                            search_ext_keys.insert(0, i_ext_key_src)
                        #
                        matches = [i for search_ext in search_ext_keys for i in ext_search_dict.get(search_ext, [])]
                        if matches:
                            directory_path_tgt, tgt_name_base, ext_tgt = matches[0]
                            #
                            tgt_name_base = i_name_base_src
                            target_file_path = u'{}/{}{}'.format(directory_path_tgt, tgt_name_base, ext_tgt)
                            j_port = i_obj.get_port(j_port_path)
                            tgt_texture_file_obj = utl_dcc_objects.OsTexture(target_file_path)
                            #
                            repath_queue.append(
                                (j_port, tgt_texture_file_obj)
                            )
                            bsc_core.Log.trace_method_result(
                                'file-search',
                                u'file="{}" >> "{}"'.format(i_texture.path, tgt_texture_file_obj.path)
                            )
                    else:
                        bsc_core.Log.trace_method_warning(
                            'file-search',
                            u'file="{}" target is not found'.format(i_texture.path)
                        )
            #
            g_p.set_stop()
        #
        self._set_repath_queue_run_(repath_queue)

    def set_search_from_(self, directory_paths_tgt, below_enable=False):
        dcc_objs = self._objs

        repath_queue = []

        search_opt = bsc_core.StgFileSearchOpt(
            ignore_name_case=True,
            ignore_ext_case=True,
            ignore_ext=True
        )
        search_opt.set_search_directories(directory_paths_tgt, below_enable=below_enable)
        if dcc_objs:
            g_p = bsc_core.LogProcessContext(
                maximum=len(dcc_objs)
            )
            for i_dcc_obj in dcc_objs:
                g_p.do_update()
                for j_port_path, j_texture_path_tgt in i_dcc_obj.reference_raw.items():
                    j_texture_src = utl_dcc_objects.OsTexture(j_texture_path_tgt)
                    j_result = search_opt.get_result(j_texture_src.path)
                    if j_result:
                        j_port = i_dcc_obj.get_port(j_port_path)
                        tgt_texture_tgt = utl_dcc_objects.OsTexture(j_result)
                        #
                        repath_queue.append(
                            (j_port, tgt_texture_tgt)
                        )
                        bsc_core.Log.trace_method_result(
                            'file-search',
                            'file="{}" >> "{}"'.format(j_texture_src.path, tgt_texture_tgt.path)
                        )
                    else:
                        bsc_core.Log.trace_method_warning(
                            'file-search',
                            'file="{}" target is not found'.format(j_texture_src.path)
                        )

            #
            g_p.set_stop()

            self._set_repath_queue_run_(repath_queue)

    def set_copy_and_repath_to(self, directory_path_tgt):
        objs = self._objs
        #
        copy_queue = []
        repath_queue = []
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    j_port = i_obj.get_port(j_port_path)
                    src_texture_file_obj = utl_dcc_objects.OsTexture(j_file_path)
                    tgt_texture_file_obj = src_texture_file_obj.get_target_file(directory_path_tgt)
                    for src_texture_file_tile_obj in src_texture_file_obj.get_exists_units():
                        tgt_texture_file_tile_obj = src_texture_file_tile_obj.get_target_file(
                            directory_path_tgt
                        )
                        copy_queue.append(
                            (src_texture_file_tile_obj, tgt_texture_file_tile_obj)
                        )
                    #
                    repath_queue.append(
                        (j_port, tgt_texture_file_obj)
                    )
        #
        method_args = [
            (self._set_copy_queue_run_, (copy_queue,)),
            (self._set_repath_queue_run_, (repath_queue,))
        ]
        if method_args:
            g_p = bsc_core.LogProcessContext(
                maximum=len(method_args)
            )
            for method, args in method_args:
                g_p.do_update()
                method(*args)
            #
            g_p.set_stop()

    def get_reference_dic(self):
        dic = collections.OrderedDict()
        objs = self._objs
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    atr_path = '{}.{}'.format(i_obj.path, j_port_path)
                    dic[atr_path] = j_file_path
        return dic

    def set_reference_dict_save_as_yaml(self, file_path):
        raw = self.get_reference_dic()
        #
        yaml_file_obj = utl_dcc_objects.OsYamlFile(file_path)
        yaml_file_obj.set_write(raw)

    def set_load_by_reference_dict_file(self, file_path):
        yaml_file_obj = utl_dcc_objects.OsYamlFile(file_path)
        raw = yaml_file_obj.set_read()
        for i_atr_path, j_file_path in raw.items():
            self._texture_references._set_real_file_path_by_atr_path_(
                i_atr_path, j_file_path
            )

    def set_color_space_auto_switch(self):
        dcc_nodes = self._texture_references.get_objs()
        if dcc_nodes:
            with bsc_core.LogProcessContext.create(maximum=len(dcc_nodes), label='switch color-space auto') as g_p:
                for i_dcc_node in dcc_nodes:
                    g_p.do_update()
                    stg_files = i_dcc_node.get_file_objs()
                    if stg_files:
                        for stg_file in stg_files:
                            if stg_file.get_is_exists() is True:
                                color_space = stg_file.get_color_space_src()
                                i_dcc_node.set_color_space(color_space)

    def set_tx_repath_to_orig(self):
        objs = self._objs
        #
        repath_queue = []
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    j_port = i_obj.get_port(j_port_path)
                    stg_texture = utl_dcc_objects.OsTexture(j_file_path)
                    if stg_texture.get_ext_is_tx():
                        o = stg_texture.get_tx_orig()
                        if o is not None:
                            repath_queue.append(
                                (j_port, o)
                            )
        #
        self._set_repath_queue_run_(repath_queue)

    def set_repath_to_orig_as_tgt_ext(self, ext_tgt):
        objs = self._objs
        #
        repath_queue = []
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    j_port = i_obj.get_port(j_port_path)
                    i_texture = utl_dcc_objects.OsTexture(j_file_path)
                    if i_texture.get_ext_is(ext_tgt):
                        o = i_texture.get_orig_as_tgt_ext(ext_tgt)
                        if o is not None:
                            repath_queue.append(
                                (j_port, o)
                            )
        #
        self._set_repath_queue_run_(repath_queue)

    def map_to_current(self, target_platform=None):
        objs = self._objs
        #
        if objs:
            for i_obj in objs:
                for j_port_path, j_file_path in i_obj.reference_raw.items():
                    stg_texture = utl_dcc_objects.OsTexture(j_file_path)
                    if target_platform is None:
                        tgt_stg_texture_path = bsc_core.StgPathMapper.map_to_current(stg_texture.path)
                    elif target_platform == 'windows':
                        tgt_stg_texture_path = bsc_core.StgPathMapper.map_to_windows(stg_texture.path)
                    elif target_platform == 'linux':
                        tgt_stg_texture_path = bsc_core.StgPathMapper.map_to_linux(stg_texture.path)
                    else:
                        raise TypeError()
                    #
                    tgt_stg_texture = utl_dcc_objects.OsTexture(tgt_stg_texture_path)
                    j_port = i_obj.get_port(j_port_path)
                    #
                    self._set_port_repath_(j_port, tgt_stg_texture)
