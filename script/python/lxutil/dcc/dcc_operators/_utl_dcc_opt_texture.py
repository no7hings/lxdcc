# coding:utf-8
import glob

import os

import fnmatch

import collections

from lxbasic import bsc_core

from lxutil import utl_core

from lxbasic.objects import bsc_obj_abs

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
                for i_port_path, i_file_path in obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if i_texture.get_is_tx_ext() is True:
                        i_texture_orig = i_texture.get_tx_orig()
                        i_texture_tx = i_texture
                    else:
                        i_texture_tx = i_texture.get_tx()
                        #
                        i_port = obj.get_port(i_port_path)
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
                        tx_create_queue.append(i_texture_orig)
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'texture-tx create',
                            u'file="{}" orig is non-exists'.format(i_file_path)
                        )
        return tx_create_queue, tx_repath_queue
    #
    def set_tx_create(self, use_deferred=False, force=False):
        tx_create_queue, tx_repath_queue = self._get_tx_action_queue_(
            self._objs, force=force
        )
        #
        return self._get_tx_create_process_(tx_create_queue, use_deferred)
    #
    def set_tx_repath(self, check_exists=True):
        tx_create_queue, tx_repath_queue = self._get_tx_action_queue_(
            self._objs, check_exists=check_exists
        )
        return self._set_repath_queue_run_(tx_repath_queue)
    #
    def set_tx_create_and_repath_use_thread(self, use_deferred=False, force=False):
        objs = self._objs
        #
        tx_create_queue = []
        repath_queue = []
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if i_texture.get_is_tx_ext() is True:
                        i_texture_orig = i_texture.get_tx_orig()
                        i_texture_tx = i_texture
                    else:
                        i_texture_tx = i_texture.get_tx()
                        #
                        i_port = obj.get_port(i_port_path)
                        repath_queue.append(
                            (i_port, (i_texture, i_texture_tx))
                        )
                        i_texture_orig = i_texture
                    #
                    if force is True:
                        i_texture_tx.set_delete()
                    #
                    if i_texture_orig is not None:
                        tx_create_queue.append(i_texture_orig)
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'texture-tx create',
                            u'file="{}" orig is non-exists'.format(i_file_path)
                        )
        #
        method_args = [
            ('tx-create', self._get_tx_create_process_, (tx_create_queue, use_deferred)),
            ('repath', self._set_repath_queue_run_, (repath_queue, ))
        ]
        results_dict = {}
        if method_args:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(method_args)
            )
            for key, method, args in method_args:
                g_p.set_update()
                process = method(*args)
                results_dict[key] = process
            #
            g_p.set_stop()
        #
        return results_dict

    def set_tx_create_and_repath(self, force=False, check_exists=True):
        tx_create_queue, tx_repath_queue = self._get_tx_action_queue_(
            self._objs, force=force
        )
        self._set_tx_create_queue_run_(tx_create_queue)
        self._set_repath_queue_run_(tx_repath_queue)
    @classmethod
    def _set_tx_create_queue_run_(cls, queue):
        if queue:
            with utl_core.log_progress(maximum=len(queue), label='texture-tx create') as l_p:
                for i_texture in queue:
                    l_p.set_update()
                    if i_texture.get_tx_is_exists() is False:
                        i_texture_tiles = i_texture.get_exists_files()
                        if i_texture_tiles:
                            for j_texture_tile in i_texture_tiles:
                                utl_dcc_objects.OsTexture._set_unit_tx_create_(
                                    j_texture_tile.path, block=True
                                )
    @classmethod
    def _get_tx_create_process_(cls, queue, use_deferred):
        lis = []
        utl_core.Log.set_module_result_trace(
            'texture-tx process create',
            'start'
        )
        if queue:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(queue)
            )
            #
            for i_texture in queue:
                g_p.set_update()
                if i_texture.get_tx_is_exists() is False:
                    i_texture_tiles = i_texture.get_exists_files()
                    if i_texture_tiles:
                        for j_texture_tile in i_texture_tiles:
                            lis.append(j_texture_tile.path)
            #
            g_p.set_stop()
        #
        process = TextureTxMainProcess(lis)
        process.PROCESS_COUNT = 0
        process.set_name('texture-tx create')
        if use_deferred is True:
            pass
        else:
            process.set_start()
        #
        utl_core.Log.set_module_result_trace(
            'texture-tx process create',
            'complete'
        )
        return process
    @classmethod
    def _get_jpg_action_queue_(cls, objs, force=False, check_exists=True):
        jpg_create_queue = []
        jpg_repath_queue = []
        #
        tgt_ext = '.jpg'
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if i_texture.get_is_tgt_ext(tgt_ext) is True:
                        i_tgt_ext_texture_orig = i_texture.get_orig_as_tgt_ext(tgt_ext)
                        i_tgt_ext_texture = i_texture
                    else:
                        i_tgt_ext_texture = i_texture.get_as_tgt_ext(tgt_ext)
                        #
                        i_port = obj.get_port(i_port_path)
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
                        utl_core.Log.set_module_warning_trace(
                            'texture-tx create',
                            u'file="{}" orig is non-exists'.format(i_file_path)
                        )
        return jpg_create_queue, jpg_repath_queue

    def set_jpg_create(self, use_deferred=False, force=False):
        jpg_create_queue, jpg_repath_queue = self._get_jpg_action_queue_(
            self._objs, force=force
        )
        return self._get_jpg_create_process_(jpg_create_queue, use_deferred)

    def set_jpg_repath(self, check_exists=True):
        jpg_create_queue, jpg_repath_queue = self._get_jpg_action_queue_(
            self._objs, check_exists=check_exists
        )
        return self._set_repath_queue_run_(jpg_repath_queue)

    def set_jpg_create_and_repath_use_thread(self, use_deferred=False, force=False):
        objs = self._objs
        #
        jpg_create_queue = []
        repath_queue = []
        #
        tgt_ext = '.jpg'
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    i_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if i_texture.get_is_tgt_ext(tgt_ext) is True:
                        i_tgt_ext_texture_orig = i_texture.get_orig_as_tgt_ext(tgt_ext)
                        i_tgt_ext_texture = i_texture
                    else:
                        i_tgt_ext_texture = i_texture.get_as_tgt_ext(tgt_ext)
                        #
                        i_port = obj.get_port(i_port_path)
                        repath_queue.append(
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
                        utl_core.Log.set_module_warning_trace(
                            'texture-tx create',
                            u'file="{}" orig is non-exists'.format(i_file_path)
                        )
        #
        method_args = [
            ('jpg-create', self._get_jpg_create_process_, (jpg_create_queue, use_deferred)),
            ('repath', self._set_repath_queue_run_, (repath_queue,))
        ]
        results_dict = {}
        if method_args:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(method_args)
            )
            for key, method, args in method_args:
                g_p.set_update()
                process = method(*args)
                results_dict[key] = process
            #
            g_p.set_stop()
        #
        return results_dict

    def set_jpg_create_and_repath(self, force=False):
        jpg_create_queue, jpg_repath_queue = self._get_jpg_action_queue_(
            self._objs, force=force
        )
        self._set_jpg_create_queue_run_(jpg_create_queue)
        self._set_repath_queue_run_(jpg_repath_queue)
    @classmethod
    def _set_jpg_create_queue_run_(cls, queue):
        if queue:
            with utl_core.log_progress(maximum=len(queue), label='texture-jpg create') as l_p:
                for i_texture in queue:
                    l_p.set_update()
                    if i_texture.get_tx_is_exists() is False:
                        i_texture_tiles = i_texture.get_exists_files()
                        if i_texture_tiles:
                            for j_texture_tile in i_texture_tiles:
                                utl_dcc_objects.OsTexture._set_unit_jpg_create_(
                                    j_texture_tile.path, block=True
                                )
    @classmethod
    def _get_jpg_create_process_(cls, queue, use_deferred):
        lis = []
        utl_core.Log.set_module_result_trace(
            'texture-jpg-process create',
            'start'
        )
        if queue:
            tgt_ext = '.jpg'
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(queue)
            )
            #
            for i_texture in queue:
                g_p.set_update()
                if i_texture.get_is_exists_as_tgt_ext(tgt_ext) is False:
                    i_texture_tiles = i_texture.get_exists_files()
                    if i_texture_tiles:
                        for j_texture_tile in i_texture_tiles:
                            lis.append(j_texture_tile.path)
            #
            g_p.set_stop()
        #
        process = TextureJpgMainProcess(lis)
        process.PROCESS_COUNT = 0
        process.set_name('texture-jpg-create')
        if use_deferred is True:
            pass
        else:
            process.set_start()
        #
        utl_core.Log.set_module_result_trace(
            'texture-jpg-process create',
            'complete'
        )
        return process
    @classmethod
    def _set_copy_queue_run_(cls, queue):
        utl_core.Log.set_module_result_trace(
            'texture-copy',
            'start'
        )
        if queue:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(queue)
            )
            for src_stg_file, tgt_stg_file in queue:
                g_p.set_update()
                src_stg_file.set_copy_to_file(
                    tgt_stg_file.path
                )
            #
            g_p.set_stop()
        #
        utl_core.Log.set_module_result_trace(
            'texture-copy',
            'complete'
        )

    def _set_repath_queue_run_(self, queue, force=False):
        utl_core.Log.set_module_result_trace(
            'texture repath',
            'start'
        )
        if queue:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(queue)
            )
            for i_port, i_args in queue:
                g_p.set_update()
                #
                if isinstance(i_args, (tuple, list)):
                    check_file_obj, tgt_stg_file = i_args
                else:
                    check_file_obj = tgt_stg_file = i_args
                #
                if check_file_obj.get_exists_files() or force is True:
                    self._set_port_repath_(i_port, tgt_stg_file)
                    color_space = tgt_stg_file.get_used_color_space()
                    if tgt_stg_file.get_exists_files() is True:
                        i_port.obj.set_color_space(color_space)
                else:
                    utl_core.Log.set_module_warning_trace(
                        'texture repath',
                        u'file="{}" is non-exists'.format(tgt_stg_file.path)
                    )
            #
            g_p.set_stop()
            #
            self._set_repath_post_run_()
        #
        utl_core.Log.set_module_result_trace(
            'texture repath',
            'complete'
        )
    @utl_core._debug_
    def _set_repath_post_run_(self):
        if utl_core.Application.get_is_maya():
            import lxmaya.commands as mya_commands
            #
            mya_commands.set_texture_tiles_repair()

    def _set_port_repath_(self, port, stg_texture):
        self._texture_references._set_real_file_path_(
            port,
            stg_texture.path
        )
        utl_core.Log.set_module_result_trace(
            'texture repath',
            u'port="{}", file="{}"'.format(port.path, stg_texture.path)
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
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(objs)
            )
            for obj in objs:
                g_p.set_update()
                for i_port_path, i_file_path in obj.reference_raw.items():
                    src_texture_file = utl_dcc_objects.OsTexture(i_file_path)
                    #
                    src_name_base = src_texture_file.name_base
                    src_ext = src_texture_file.ext
                    #
                    src_ext_key = src_ext.lower()
                    #
                    search_name_bases = search_dict.keys()
                    name_base_fnmatch_pattern = bsc_core.MultiplyPatternMtd.to_fnmatch_style(src_name_base)
                    #
                    match_name_base_keys = fnmatch.filter(search_name_bases, name_base_fnmatch_pattern)
                    if match_name_base_keys:
                        tgt_name_base = match_name_base_keys[0]
                        ext_search_dict = search_dict[tgt_name_base]
                        #
                        search_ext_keys = ext_search_dict.keys()
                        if src_ext_key in search_ext_keys:
                            search_ext_keys.remove(src_ext_key)
                            search_ext_keys.insert(0, src_ext_key)
                        #
                        matches = [i for search_ext in search_ext_keys for i in ext_search_dict.get(search_ext, [])]
                        if matches:
                            tgt_directory_path, tgt_name_base, tgt_ext = matches[0]
                            tgt_name_base = src_name_base
                            target_file_path = u'{}/{}{}'.format(tgt_directory_path, tgt_name_base, tgt_ext)
                            port = obj.get_port(i_port_path)
                            tgt_texture_file_obj = utl_dcc_objects.OsTexture(target_file_path)
                            #
                            repath_queue.append(
                                (port, tgt_texture_file_obj)
                            )
                            utl_core.Log.set_module_result_trace(
                                'file-search',
                                u'file="{}" >> "{}"'.format(src_texture_file.path, tgt_texture_file_obj.path)
                            )
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'file-search',
                            u'file="{}" target is not found'.format(src_texture_file.path)
                        )
            #
            g_p.set_stop()
        #
        self._set_repath_queue_run_(repath_queue)

    def set_copy_and_repath_to(self, tgt_directory_path):
        objs = self._objs
        #
        copy_queue = []
        repath_queue = []
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    port = obj.get_port(i_port_path)
                    src_texture_file_obj = utl_dcc_objects.OsTexture(i_file_path)
                    tgt_texture_file_obj = src_texture_file_obj.get_target_file(tgt_directory_path)
                    for src_texture_file_tile_obj in src_texture_file_obj.get_exists_files():
                        tgt_texture_file_tile_obj = src_texture_file_tile_obj.get_target_file(
                            tgt_directory_path
                        )
                        copy_queue.append(
                            (src_texture_file_tile_obj, tgt_texture_file_tile_obj)
                        )
                    #
                    repath_queue.append(
                        (port, tgt_texture_file_obj)
                    )
        #
        method_args = [
            (self._set_copy_queue_run_, (copy_queue, )),
            (self._set_repath_queue_run_, (repath_queue, ))
        ]
        if method_args:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(method_args)
            )
            for method, args in method_args:
                g_p.set_update()
                method(*args)
            #
            g_p.set_stop()

    def get_reference_dic(self):
        dic = collections.OrderedDict()
        objs = self._objs
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    atr_path = '{}.{}'.format(obj.path, i_port_path)
                    dic[atr_path] = i_file_path
        return dic

    def set_reference_dict_save_as_yaml(self, file_path):
        raw = self.get_reference_dic()
        #
        yaml_file_obj = utl_dcc_objects.OsYamlFile(file_path)
        yaml_file_obj.set_write(raw)

    def set_load_by_reference_dict_file(self, file_path):
        yaml_file_obj = utl_dcc_objects.OsYamlFile(file_path)
        raw = yaml_file_obj.set_read()
        for i_atr_path, i_file_path in raw.items():
            self._texture_references._set_real_file_path_by_atr_path_(
                i_atr_path, i_file_path
            )

    def set_color_space_auto_switch(self):
        dcc_nodes = self._texture_references.get_objs()
        if dcc_nodes:
            g_p = utl_core.GuiProgressesRunner(
                maximum=len(dcc_nodes)
            )
            for dcc_node in dcc_nodes:
                g_p.set_update()
                stg_files = dcc_node.get_file_objs()
                if stg_files:
                    for stg_file in stg_files:
                        if stg_file.get_is_exists() is True:
                            color_space = stg_file.get_used_color_space()
                            dcc_node.set_color_space(color_space)
            #
            g_p.set_stop()

    def set_tx_repath_to_orig(self):
        objs = self._objs
        #
        repath_queue = []
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    port = obj.get_port(i_port_path)
                    stg_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if stg_texture.get_is_tx_ext():
                        o = stg_texture.get_tx_orig()
                        if o is not None:
                            repath_queue.append(
                                (port, o)
                            )
        #
        self._set_repath_queue_run_(repath_queue)

    def set_repath_to_orig_as_tgt_ext(self, tgt_ext):
        objs = self._objs
        #
        repath_queue = []
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    port = obj.get_port(i_port_path)
                    i_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if i_texture.get_is_tgt_ext(tgt_ext):
                        o = i_texture.get_orig_as_tgt_ext(tgt_ext)
                        if o is not None:
                            repath_queue.append(
                                (port, o)
                            )
        #
        self._set_repath_queue_run_(repath_queue)

    def set_map_to_platform(self, target_platform=None):
        objs = self._objs
        #
        if objs:
            for obj in objs:
                for i_port_path, i_file_path in obj.reference_raw.items():
                    stg_texture = utl_dcc_objects.OsTexture(i_file_path)
                    if target_platform is None:
                        tgt_stg_texture_path = bsc_core.StoragePathMtd.set_map_to_platform(stg_texture.path)
                    elif target_platform == 'windows':
                        tgt_stg_texture_path = bsc_core.StoragePathMtd.set_map_to_windows(stg_texture.path)
                    elif target_platform == 'linux':
                        tgt_stg_texture_path = bsc_core.StoragePathMtd.set_map_to_linux(stg_texture.path)
                    else:
                        raise TypeError()
                    #
                    tgt_stg_texture = utl_dcc_objects.OsTexture(tgt_stg_texture_path)
                    port = obj.get_port(i_port_path)
                    #
                    self._set_port_repath_(port, tgt_stg_texture)


class TextureTxSubProcess(bsc_obj_abs.AbsProcess):
    LOGGER = utl_core.Log
    #
    def __init__(self, file_path):
        super(TextureTxSubProcess, self).__init__()
        self._file_path = file_path
        self._f = utl_dcc_objects.OsTexture(self._file_path)

    def _set_sub_process_create_fnc_(self):
        pre_count = TextureTxMainProcess.PROCESS_COUNT
        maximum = TextureTxMainProcess.PROCESS_COUNT_MAXIMUM
        if pre_count < maximum:
            result = self._f._set_unit_tx_create_(self._file_path)
            TextureTxMainProcess.PROCESS_COUNT = pre_count + 1
        else:
            result = None
        return result

    def _set_finished_fnc_run_(self):
        pre_count = TextureTxMainProcess.PROCESS_COUNT
        TextureTxMainProcess.PROCESS_COUNT = pre_count - 1


class TextureTxMainProcess(bsc_obj_abs.AbsProcess):
    LOGGER = utl_core.Log
    #
    PROCESS_COUNT = 0
    PROCESS_COUNT_MAXIMUM = 2
    ELEMENT_PROCESS_CLS = TextureTxSubProcess
    def __init__(self, file_paths):
        super(TextureTxMainProcess, self).__init__()
        self._file_paths = list(set(file_paths))
        for i in self._file_paths:
            i_e = self.ELEMENT_PROCESS_CLS(i)
            i_e.set_name(i)
            self.set_element_add(i_e)

    def _set_sub_process_create_fnc_(self):
        return True

    def _set_finished_fnc_run_(self):
        return True


class TextureJpgSubProcess(bsc_obj_abs.AbsProcess):
    LOGGER = utl_core.Log
    #
    def __init__(self, file_path):
        super(TextureJpgSubProcess, self).__init__()
        self._file_path = file_path
        self._f = utl_dcc_objects.OsTexture(self._file_path)

    def _set_sub_process_create_fnc_(self):
        pre_count = TextureJpgMainProcess.PROCESS_COUNT
        maximum = TextureJpgMainProcess.PROCESS_COUNT_MAXIMUM
        if pre_count < maximum:
            result = self._f._set_unit_jpg_create_(self._file_path)
            TextureJpgMainProcess.PROCESS_COUNT = pre_count + 1
        else:
            result = None
        return result

    def _set_finished_fnc_run_(self):
        pre_count = TextureJpgMainProcess.PROCESS_COUNT
        TextureJpgMainProcess.PROCESS_COUNT = pre_count - 1


class TextureJpgMainProcess(bsc_obj_abs.AbsProcess):
    LOGGER = utl_core.Log
    #
    PROCESS_COUNT = 0
    PROCESS_COUNT_MAXIMUM = 2
    ELEMENT_PROCESS_CLS = TextureJpgSubProcess
    def __init__(self, file_paths):
        super(TextureJpgMainProcess, self).__init__()
        self._file_paths = list(set(file_paths))
        for i in self._file_paths:
            i_e = self.ELEMENT_PROCESS_CLS(i)
            i_e.set_name(i)
            self.set_element_add(i_e)

    def _set_sub_process_create_fnc_(self):
        return True

    def _set_finished_fnc_run_(self):
        return True
