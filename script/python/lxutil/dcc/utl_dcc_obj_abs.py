# coding:utf-8
import os

import re

import glob

import hashlib

import lxbasic.core as bsc_core

import lxuniverse.abstracts as unr_abstracts


class AbsObjStgGuiExtraDef(object):
    def set_gui_attribute(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def path(self):
        raise NotImplementedError()

    def copy_path_to_clipboard(self):
        import lxgui.qt.core as gui_qt_core

        gui_qt_core.GuiQtUtil.copy_text_to_clipboard(self.path)

    def copy_name_to_clipboard(self):
        import lxgui.qt.core as gui_qt_core

        gui_qt_core.GuiQtUtil.copy_text_to_clipboard(self.name)


class AbsStgDirectory(
    unr_abstracts.AbsStgDirectory,
    unr_abstracts.AbsGuiExtraDef,
    AbsObjStgGuiExtraDef
):

    def __init__(self, path):
        super(AbsStgDirectory, self).__init__(path)
        self._init_gui_extra_def_()
        self.set_gui_attribute(
            'gui_menu',
            [
                ('open folder', 'file/open-folder', self.set_open),
                (),
                ('copy path', 'copy', self.copy_path_to_clipboard),
                ('copy name', 'copy', self.copy_name_to_clipboard),
            ]
        )

    def get_icon(self):
        return bsc_core.ResourceIcon.get('file/folder')

    icon = property(get_icon)

    def set_create(self):
        if self.get_is_exists() is False:
            bsc_core.StorageMtd.create_directory(self.path)
            bsc_core.Log.trace_method_result(
                'directory create',
                u'directory-path="{}"'.format(self.path)
            )

    def link_to(self, directory_path_tgt, replace=False):
        directory_tgt = self.__class__(directory_path_tgt)
        if directory_tgt.get_is_exists():
            if replace is False:
                bsc_core.Log.trace_method_warning(
                    'link create',
                    u'path="{}" is exists'.format(directory_tgt.path)
                )
                return
            else:
                if os.path.islink(directory_tgt.path) is True:
                    bsc_core.StgPathPermissionMtd.unlock(directory_tgt.path)
                    os.remove(directory_tgt.path)
                    bsc_core.Log.trace_method_result(
                        'path-link-remove',
                        u'path="{}"'.format(directory_tgt.path)
                    )
        #
        if directory_tgt.get_is_exists() is False:
            self.create_symlink_fnc(self.path, directory_tgt.path)
            #
            bsc_core.Log.trace_method_result(
                'link create',
                u'connection="{}" >> "{}"'.format(self.path, directory_tgt.path)
            )

    def get_directory_paths(self):
        return bsc_core.StgDirectoryMtd.get_directory_paths(
            self.path
        )

    def get_all_files(self):
        return


class AbsStgFile(
    unr_abstracts.AbsStgFile,
    unr_abstracts.AbsGuiExtraDef,
    AbsObjStgGuiExtraDef
):
    ICON_DICT = {
        '.ma': 'ma',
        '.mb': 'ma',
        '.hip': 'hip',
        '.katana': 'katana',
        '.exr': 'image',
        '.py': 'python'
    }
    OS_DIRECTORY_CLS = None
    # ignore case
    # multiply
    # udim
    RE_UDIM_KEYS = [
        ('<udim>', 4),
    ]
    # sequence
    RE_SEQUENCE_KEYS = [
        ('#', -1),
        (r'<f>', 4),
        (r'\$F04', 4),
        (r'\$F', 4),
        (r'(\()[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](\))(%04d)', 4),
        (r'%04d', 4),
    ]
    RE_MULTIPLY_KEYS = RE_UDIM_KEYS+RE_SEQUENCE_KEYS
    #
    RE_SEQUENCE_PATTERN = None
    #
    LOG = bsc_core.Log

    def __init__(self, path):
        super(AbsStgFile, self).__init__(
            bsc_core.StgPathOpt(path).__str__()
        )
        self._init_gui_extra_def_()
        #
        self.set_gui_attribute(
            'gui_menu',
            [
                ('open folder', 'file/open-folder', self.open_directory_in_system),
                (),
                ('copy path', None, self.copy_path_to_clipboard),
                ('copy name', None, self.copy_name_to_clipboard),
            ]
        )
        # file reference node
        self._obj = None
        self._relevant_dcc_port_path = None

    def get_icon(self):
        if self.ext:
            _ = bsc_core.ResourceIcon.get('file/{}'.format(self.ext[1:]))
            if _:
                return _
        return bsc_core.ResourceIcon.get('file/file')

    icon = property(get_icon)

    @property
    def file_path(self):
        return self._path

    def get_size(self):
        if os.path.isfile(self.path):
            return os.path.getsize(self.path)
        return 0

    def get_hash(self):
        if os.path.isfile(self.path):
            with open(self.path, u'rb') as f:
                # noinspection PyDeprecation
                md5 = hashlib.md5()
                while True:
                    d = f.read(8096)
                    if not d:
                        break
                    md5.update(d)
                f.close()
                return str(md5.hexdigest()).upper()
        return u'D41D8CD98F00B204E9800998ECF8427E'

    def get_is_exists(self):
        return self.get_exists_unit_paths() != []

    def get_is_udim(self):
        return self._get_is_udim_(self.path)

    @classmethod
    def _get_is_udim_(cls, file_path):
        path_base = os.path.basename(file_path)
        for k, c in cls.RE_UDIM_KEYS:
            i_r = re.finditer(k, path_base, re.IGNORECASE) or []
            if i_r:
                return True
        return False

    def get_is_sequence(self):
        return self._get_is_sequence_(self.path)

    @classmethod
    def _get_is_sequence_(cls, file_path):
        path_base = os.path.basename(file_path)
        for k, c in cls.RE_SEQUENCE_KEYS:
            i_r = re.finditer(k, path_base, re.IGNORECASE) or []
            if i_r:
                return True
        return False

    def get_exists_sequence_file_paths(self):
        list_ = []
        path = self.path
        re_pattern = re.compile(self.RE_SEQUENCE_PATTERN, re.IGNORECASE)
        results = re.findall(re_pattern, path)
        if results:
            glob_pattern = path.replace(results[0], '*')
            list_ = glob.glob(glob_pattern)
        if list_:
            list_.sort()
        else:
            bsc_core.Log.trace_warning('file: "{}" is Non-exists.'.format(self.path))
        return list_

    def get_exists_sequence_files(self):
        return [self.__class__(i) for i in self.get_exists_sequence_file_paths()]

    def get_exists_sequence_frames(self, frame_range):
        pass

    def get_is_sequence_exists(self, frame_range):
        pass

    # multiply
    @classmethod
    def _get_has_elements_(cls, file_path):
        path_base = os.path.basename(file_path)
        for k, c in cls.RE_MULTIPLY_KEYS:
            i_r = re.finditer(k, path_base, re.IGNORECASE) or []
            if i_r:
                return True
        return False

    @classmethod
    def _set_file_path_ext_replace_to_(cls, file_path, ext):
        return os.path.splitext(file_path)[0]+ext

    def get_as_new_ext(self, ext):
        return self.__class__(
            '{}{}'.format(self.path_base, ext)
        )

    def get_has_elements(self):
        return self._get_has_elements_(self.path)

    @classmethod
    def _get_exists_file_paths_(cls, file_path, ext_includes=None):
        def get_ext_replace_fnc_(file_path_, ext_):
            return os.path.splitext(file_path_)[0]+ext_

        #
        def get_add_fnc_(include_exts_, ext_):
            if isinstance(include_exts_, (tuple, list)):
                for _i_ext in include_exts_:
                    if ext_ == _i_ext:
                        continue
                    for _i in list_:
                        _i_add = get_ext_replace_fnc_(_i, _i_ext)
                        if os.path.isfile(_i_add) is True:
                            add_list_.append(_i_add)

        #
        re_keys = cls.RE_MULTIPLY_KEYS
        pathsep = cls.PATHSEP
        #
        directory = os.path.dirname(file_path)
        name_base = os.path.basename(file_path)
        name_base_new = name_base
        ext = os.path.splitext(name_base)[-1]
        for k, c in re_keys:
            i_r = re.finditer(k, name_base, re.IGNORECASE) or []
            for j in i_r:
                start, end = j.span()
                if c == -1:
                    s = '[0-9]'
                    name_base_new = name_base_new.replace(name_base[start:end], s, 1)
                else:
                    s = '[0-9]'*c
                    name_base_new = name_base_new.replace(name_base[start:end], s, 1)
        #
        if name_base != name_base_new:
            glob_pattern = pathsep.join([directory, name_base_new])
            list_ = glob.glob(glob_pattern)
            if list_:
                list_.sort()
        else:
            if os.path.isfile(file_path):
                list_ = [file_path]
            else:
                list_ = []
        #
        add_list_ = []
        get_add_fnc_(ext_includes, ext)
        _ = list_+add_list_
        return [i for i in _ if os.path.isfile(i)]

    @classmethod
    def _get_exists_file_paths__(cls, file_path, ext_includes=None):
        def get_ext_replace_fnc_(file_path_, ext_):
            return os.path.splitext(file_path_)[0]+ext_

        #
        def get_add_fnc_(include_exts_, ext_):
            if isinstance(include_exts_, (tuple, list)):
                for _i_ext in include_exts_:
                    if ext_ == _i_ext:
                        continue
                    for _i in list_:
                        _i_add = get_ext_replace_fnc_(_i, _i_ext)
                        if os.path.isfile(_i_add) is True:
                            add_list_.append(_i_add)

        #
        re_keys = cls.RE_MULTIPLY_KEYS
        pathsep = cls.PATHSEP
        #
        directory = os.path.dirname(file_path)
        name_base = os.path.basename(file_path)
        name_base_new = name_base
        ext = os.path.splitext(name_base)[-1]
        for k, c in re_keys:
            i_r = re.finditer(k, name_base, re.IGNORECASE) or []
            for i in i_r:
                start, end = i.span()
                if c == -1:
                    s = '[0-9]'
                    name_base_new = name_base_new.replace(name_base[start:end], s, 1)
                else:
                    s = '[0-9]'*c
                    name_base_new = name_base_new.replace(name_base[start:end], s, 1)
        #
        if name_base != name_base_new:
            glob_pattern = pathsep.join([directory, name_base_new])
            list_ = bsc_core.StgDirectoryMtd.find_file_paths(glob_pattern)
            if list_:
                list_.sort()
        else:
            if os.path.isfile(file_path):
                list_ = [file_path]
            else:
                list_ = []
        #
        add_list_ = []
        get_add_fnc_(ext_includes, ext)
        _ = list_+add_list_
        return _

    def get_exists_file_paths(self, *args, **kwargs):
        return self._get_exists_file_paths__(self.path, **kwargs)

    def get_exists_files(self, *args, **kwargs):
        return [self.__class__(i) for i in self.get_exists_unit_paths(*args, **kwargs)]

    @classmethod
    def get_exists_unit_paths_fnc(cls, file_path):
        return bsc_core.StgFileMultiplyMtd.get_exists_unit_paths(file_path)

    def get_exists_unit_paths(self):
        return self.get_exists_unit_paths_fnc(self.path)

    def get_exists_units(self):
        return [self.__class__(i) for i in self.get_exists_unit_paths()]

    def get_permissions(self, *args, **kwargs):
        return [bsc_core.StorageMtd.get_permission(i) for i in self.get_exists_unit_paths()]

    def get_modify_timestamp(self, *args, **kwargs):
        exists_file_paths = self.get_exists_unit_paths(*args, **kwargs)
        timestamps = [int(os.stat(i).st_mtime) for i in exists_file_paths]
        if timestamps:
            return sum(timestamps)/len(timestamps)

    def get_time(self):
        if self.get_is_exists() is True:
            timestamp = self.get_modify_timestamp()
            return bsc_core.TimestampOpt(timestamp).get()

    def get_time_tag(self):
        timestamp = self.get_modify_timestamp()
        return bsc_core.TimestampOpt(timestamp).get_as_tag()

    def get_timestamp_is_same_to(self, file_tgt):
        for i_src in self.get_exists_units():
            i_tgt = self.__class__(
                '{}/{}{}'.format(file_tgt.directory.path, i_src.name_base, file_tgt.ext)
            )
            if str(i_src.get_modify_timestamp()) != str(i_tgt.get_modify_timestamp()):
                return False
        return True

    def get_group(self):
        # noinspection PyBroadException
        try:
            import grp

            if self.get_is_exists() is True:
                stat_info = os.stat(self.path)
                gid = stat_info.st_gid
                group = grp.getgrgid(gid)[0]
                return group
        except:
            pass
        return None

    def get_user(self):
        # noinspection PyBroadException
        try:
            import pwd

            if self.get_is_exists() is True:
                stat_info = os.stat(self.path)
                uid = stat_info.st_uid
                user = pwd.getpwuid(uid)[0]
                return user
        except:
            pass
        return None

    def copy_unit_to(self, directory_path_dst, fix_name_blank=False, replace=True):
        name = self.name
        if fix_name_blank is True:
            if ' ' in name:
                name = name.replace(' ', '_')
        #
        file_path_tgt = '{}/{}'.format(directory_path_dst, name)
        file_tgt = self.__class__(file_path_tgt)
        if file_tgt.get_is_exists_file() is True:
            if replace is True:
                os.remove(file_tgt.path)
        #
        if file_tgt.get_is_exists() is False:
            file_tgt.create_directory()
            self.set_copy_to_file(file_path_tgt)

    def copy_unit_as_base_link(self, directory_path_bsc, directory_path_dst, fix_name_blank=False, replace=True):
        if self.get_is_exists_file():
            timestamp = self.get_modify_timestamp()
            size = self.get_size()
            name = self.name
            if fix_name_blank is True:
                if ' ' in name:
                    name = name.replace(' ', '_')
            #
            time_tag = bsc_core.RawIntegerOpt(int(timestamp)).set_encode_to_36()
            size_tag = bsc_core.RawIntegerOpt(int(size)).set_encode_to_36()
            file_path_tgt = u'{}/{}'.format(directory_path_dst, name)
            file_path_dir_src = u'{}/{}'.format(directory_path_bsc, name)
            file_path_name_src = u'V-{}-{}.{}'.format(time_tag, size_tag, name)
            file_path_src = u'{}/{}'.format(file_path_dir_src, file_path_name_src)
            file_path_copy_log_src = u'{}/.copy.log'.format(file_path_dir_src)
            file_path_link_log_src = u'{}/.link.log'.format(file_path_dir_src)
            # copy to src
            result, copy_log = self.set_copy_to_file(file_path_src)
            # write log
            if copy_log is not None:
                bsc_core.StgFileOpt(file_path_copy_log_src).append(copy_log)
            #
            file_tgt = self.__class__(file_path_tgt)
            if file_tgt.get_is_exists_file() is True:
                if replace is True:
                    if bsc_core.StgPathLinkMtd.get_is_link_source_to(
                            file_path_src, file_path_tgt,
                    ) is False:
                        os.remove(file_tgt.path)
                        #
                        bsc_core.StgPathLinkMtd.link_to(file_path_src, file_tgt.path)
                        link_log = bsc_core.Log.trace_method_result(
                            'link replace',
                            u'connection="{} >> {}"'.format(file_path_src, file_path_tgt)
                        )
                        bsc_core.StgFileOpt(file_path_link_log_src).append(link_log)
                        return True, link_log
                else:
                    return False, bsc_core.Log.trace_method_warning(
                        'link create',
                        u'file="{}" is exists'.format(file_path_tgt)
                    )
            #
            if file_tgt.get_is_exists() is False:
                file_tgt.create_directory()
                # link src to target
                bsc_core.StgPathLinkMtd.link_to(file_path_src, file_path_tgt)
                link_log = bsc_core.Log.trace_method_result(
                    'link create',
                    u'connection="{} >> {}"'.format(file_path_src, file_path_tgt)
                )
                bsc_core.StgFileOpt(file_path_link_log_src).append(link_log)
                return True, link_log
        else:
            bsc_core.Log.trace_method_warning(
                'file base link',
                'file="{}" not available'.format(self.path)
            )
        return False, None

    def copy_as_base_link(self, directory_path_bsc, directory_path_dst, fix_name_blank=False, replace=True):
        files = self.get_exists_units()
        for i_file in files:
            i_file.copy_unit_as_base_link(
                directory_path_bsc=directory_path_bsc,
                directory_path_dst=directory_path_dst,
                fix_name_blank=fix_name_blank,
                replace=replace
            )

    # file reference node ******************************************************************************************** #
    def set_node(self, node):
        self._obj = node

    def get_obj(self):
        return self._obj

    def set_relevant_dcc_port_path(self, port_path):
        self._relevant_dcc_port_path = port_path

    def get_relevant_dcc_port_path(self):
        return self._relevant_dcc_port_path

    def set_rename(self, new_name):
        new_path = '{}{}{}'.format(self.directory.path, self.PATHSEP, new_name)
        if os.path.exists(self.path) is True and os.path.exists(new_path) is False:
            os.rename(
                self.path, new_path
            )
            bsc_core.Log.trace_result(
                u'rename file: "{}" > "{}"'.format(self.path, new_path)
            )

    def get_ext_variants(self, ext_includes=None):
        path_base, ext = os.path.splitext(self.path)
        glob_pattern = u'{}.*'.format(path_base)
        _ = glob.glob(glob_pattern)
        lis = []
        if _:
            for i in _:
                if i == self.path:
                    continue
                if ext_includes is not None:
                    i_base, i_ext = os.path.splitext(i)
                    if i_ext not in ext_includes:
                        continue
                lis.append(i)
        return [self.__class__(i) for i in lis]

    def set_ext_replace(self, ext):
        path_base, _ext = os.path.splitext(self.path)
        return self.__class__(path_base+ext)

    def set_delete(self):
        exists_file_paths = self._get_exists_file_paths__(self._path)
        if exists_file_paths:
            for i in exists_file_paths:
                os.remove(i)
                self.LOG.trace_method_result(
                    'file-delete',
                    u'"{}"'.format(i)
                )

    def get_is_link_source_to(self, file_path_tgt):
        return bsc_core.StgPathLinkMtd.get_is_link_source_to(
            self.path, file_path_tgt,
        )

    def link_to(self, tgt_file_path, replace=False):
        file_tgt = self.__class__(tgt_file_path)
        file_path_src = self.path
        file_path_tgt = file_tgt.path
        if self.get_is_exists() is True:
            if file_tgt.get_is_exists():
                if replace is True:
                    if bsc_core.StorageMtd.get_is_writable(file_path_tgt) is True:
                        if bsc_core.StgPathLinkMtd.get_is_link(file_path_tgt) is True:
                            if bsc_core.StgPathLinkMtd.get_is_link_source_to(
                                    file_path_src, file_path_tgt,
                            ) is True:
                                bsc_core.Log.trace_method_warning(
                                    'file link replace',
                                    u'relation="{} >> {}" is non-changed'.format(file_path_src, file_path_tgt)
                                )
                                return
                            #
                            os.remove(file_path_tgt)
                            bsc_core.StgPathLinkMtd.link_file_to(file_path_src, file_path_tgt)
                            bsc_core.Log.trace_method_result(
                                'file link replace',
                                u'relation="{} >> {}"'.format(file_path_src, file_path_tgt)
                            )
                            return
                        #
                        os.remove(file_path_tgt)
                        bsc_core.StgPathLinkMtd.link_file_to(file_path_src, file_path_tgt)
                        bsc_core.Log.trace_method_result(
                            'file link replace',
                            u'relation="{} >> {}"'.format(file_path_src, file_path_tgt)
                        )
                        return
                    self.LOG.trace_method_error(
                        'file link replace',
                        u'file="{}" is locked'.format(file_tgt.path)
                    )
                    return

                else:
                    bsc_core.Log.trace_method_warning(
                        'file link',
                        u'file="{}" is exists'.format(file_path_tgt)
                    )
                    return
            #
            if file_tgt.get_is_exists() is False:
                file_tgt.create_directory()
                #
                bsc_core.StgPathLinkMtd.link_file_to(
                    self.path, file_tgt.path
                )
                #
                bsc_core.Log.trace_method_result(
                    'file link',
                    u'relation="{} >> {}"'.format(self.path, file_tgt.path)
                )

    def set_link_to_file(self, file_path_tgt, replace=False):
        self.link_to(
            file_path_tgt, replace
        )

    def set_link_to_directory(self, directory_path_tgt, replace=False):
        file_path_tgt = u'{}/{}'.format(
            directory_path_tgt, self.name
        )
        self.link_to(
            file_path_tgt, replace
        )

    def get_is_writable(self):
        for i in self.get_exists_unit_paths():
            if bsc_core.StorageMtd.get_is_writable(i) is False:
                return False
        return True

    def get_is_readable(self):
        for i in self.get_exists_unit_paths():
            if bsc_core.StorageMtd.get_is_readable(i) is False:
                return False
        return True


class AbsOsTextureSeparateDef(object):
    @classmethod
    def get_directory_args_dpt_as_default_fnc(cls, texture_any, target_extension):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = texture_any.directory.path
            directory_path_tgt = texture_any.directory.get_as_new_name(target_format).path
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = (texture_any.directory.get_as_new_name('src')).path
            directory_path_tgt = texture_any.directory.path
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = texture_any.directory.path
        directory_path_tgt = texture_any.directory.path
        return directory_path_src, directory_path_tgt

    @classmethod
    def get_directory_args_dst_as_default_fnc(cls, texture_any, target_extension, target_directory):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = target_directory
        directory_path_tgt = target_directory
        return directory_path_src, directory_path_tgt

    @classmethod
    def get_directory_args_dpt_as_separate_fnc(cls, texture_any, target_extension):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = texture_any.directory.path
            directory_path_tgt = texture_any.directory.get_as_new_name(target_format).path
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = (texture_any.directory.get_as_new_name('src')).path
            directory_path_tgt = texture_any.directory.path
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = '{}/src'.format(texture_any.directory.path)
        directory_path_tgt = '{}/{}'.format(texture_any.directory.path, target_format)
        return directory_path_src, directory_path_tgt

    @classmethod
    def get_directory_args_dst_as_separate_fnc(cls, texture_any, target_extension, target_directory):
        target_format = target_extension[1:]
        # source
        if texture_any.directory.get_path_is_matched('*/src') is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        # target
        elif texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
            directory_path_src = '{}/src'.format(target_directory)
            directory_path_tgt = '{}/{}'.format(target_directory, target_format)
            return directory_path_src, directory_path_tgt
        #
        directory_path_src = '{}/src'.format(target_directory)
        directory_path_tgt = '{}/{}'.format(target_directory, target_format)
        return directory_path_src, directory_path_tgt

    @classmethod
    def get_directory_args_dpt_fnc(cls, texture_any, target_extension):
        target_format = target_extension[1:]
        if texture_any.get_extension() == target_extension:
            if texture_any.directory.get_path_is_matched('*/{}'.format(target_format)) is True:
                return cls.get_directory_args_dpt_as_separate_fnc(texture_any, target_extension)
            return cls.get_directory_args_dpt_as_default_fnc(texture_any, target_extension)
        if texture_any.directory.get_path_is_matched('*/src') is True:
            return cls.get_directory_args_dpt_as_separate_fnc(texture_any, target_extension)
        return cls.get_directory_args_dpt_as_default_fnc(texture_any, target_extension)


class AbsOsTexture(
    AbsStgFile,
    AbsOsTextureSeparateDef
):
    TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT = None
    TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES = None
    #
    OS_FILE_CLS = None
    # sequence
    RE_SEQUENCE_PATTERN = None
    # udim
    RE_UDIM_PATTERN = r'.*?(<udim>).*?'
    #
    TX_EXT = '.tx'
    EXR_EXT = '.exr'
    JPG_EXT = '.jpg'

    @classmethod
    def generate_color_space_configure_for_convert(cls):
        if cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT is not None:
            return cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT
        import lxarnold.core as and_core
        cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT = and_core.TextureColorSpaceConfigureForConvert()
        return cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT

    @classmethod
    def generate_color_space_configure_for_aces(cls):
        if cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES is not None:
            return cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES
        import lxarnold.core as and_core
        cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES = and_core.TextureColorSpaceConfigureForAces()
        return cls.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES

    def get_target_file_path_as_src(
        self, directory_path_dst, scheme='separate', target_extension='.tx', fix_name_blank=False
    ):
        if self.get_exists_unit_paths():
            directory_args_dpt = self.get_directory_args_dpt_fnc(
                self, target_extension
            )
            if scheme == 'default':
                directory_args_dst = self.get_directory_args_dst_as_default_fnc(
                    self, target_extension, directory_path_dst
                )
            elif scheme == 'separate':
                directory_args_dst = self.get_directory_args_dst_as_separate_fnc(
                    self, target_extension, directory_path_dst
                )
            else:
                raise RuntimeError()
            #
            if directory_args_dpt and directory_args_dst:
                texture_src, texture_tgt = self.get_args_as_ext_tgt_by_directory_args(
                    target_extension, directory_args_dpt
                )
                directory_src_dst, directory_tgt_dst = directory_args_dst
                #
                texture_name_src = texture_src.name
                if fix_name_blank is True:
                    if ' ' in texture_name_src:
                        texture_name_src = texture_name_src.replace(' ', '_')
                texture_path_dst_src = '{}/{}'.format(directory_src_dst, texture_name_src)
                #
                texture_name_tgt = texture_tgt.name
                if fix_name_blank is True:
                    if ' ' in texture_name_tgt:
                        texture_name_tgt = texture_name_tgt.replace(' ', '_')
                texture_path_dst_tgt = '{}/{}'.format(directory_tgt_dst, texture_name_tgt)
                return texture_path_dst_src, texture_path_dst_tgt

    def copy_unit_with_src(
        self, directory_path_dst, scheme='separate', target_extension='.tx', fix_name_blank=False, replace=True
    ):
        if self.get_is_exists_file():
            directory_args_dpt = self.get_directory_args_dpt_fnc(
                self, target_extension
            )
            if scheme == 'default':
                directory_args_dst = self.get_directory_args_dst_as_default_fnc(
                    self, target_extension, directory_path_dst
                )
            elif scheme == 'separate':
                directory_args_dst = self.get_directory_args_dst_as_separate_fnc(
                    self, target_extension, directory_path_dst
                )
            else:
                raise RuntimeError()
            #
            if directory_args_dpt and directory_args_dst:
                texture_src, texture_tgt = self.get_args_as_ext_tgt_by_directory_args(
                    target_extension, directory_args_dpt
                )
                directory_src_dst, directory_tgt_dst = directory_args_dst
                #
                if texture_src.get_is_exists() is True:
                    texture_src.copy_unit_to(
                        directory_src_dst,
                        fix_name_blank=fix_name_blank, replace=replace
                    )
                #
                if texture_tgt.get_is_exists() is True:
                    texture_tgt.copy_unit_to(
                        directory_tgt_dst,
                        fix_name_blank=fix_name_blank, replace=replace
                    )

    def copy_unit_as_base_link_with_src(
        self, directory_path_bsc, directory_path_dst, scheme='separate', target_extension='.tx',
        fix_name_blank=False, replace=True
    ):
        if self.get_is_exists_file():
            directory_args_dpt = self.get_directory_args_dpt_fnc(
                self, target_extension
            )
            if scheme == 'default':
                directory_args_dst = self.get_directory_args_dst_as_default_fnc(
                    self, target_extension, directory_path_dst
                    )
            elif scheme == 'separate':
                directory_args_dst = self.get_directory_args_dst_as_separate_fnc(
                    self, target_extension, directory_path_dst
                    )
            else:
                raise RuntimeError()
            #
            if directory_args_dpt and directory_args_dst:
                texture_src, texture_tgt = self.get_args_as_ext_tgt_by_directory_args(
                    target_extension, directory_args_dpt
                )
                directory_src_dst, directory_tgt_dst = directory_args_dst
                #
                if texture_src.get_is_exists() is True:
                    texture_src.copy_unit_as_base_link(
                        directory_path_bsc, directory_src_dst,
                        fix_name_blank=fix_name_blank, replace=replace
                    )
                if texture_tgt.get_is_exists() is True:
                    texture_tgt.copy_unit_as_base_link(
                        directory_path_bsc, directory_tgt_dst,
                        fix_name_blank=fix_name_blank, replace=replace
                    )

    @classmethod
    def _get_unit_is_exists_as_ext_tgt_(cls, file_path_any, ext_tgt):
        tgt_ext_orig_path = cls._get_unit_path_src_as_ext_tgt_(file_path_any, ext_tgt)
        tgt_ext_path = cls._get_path_tgt_as_ext_tgt_(file_path_any, ext_tgt)
        # if is non-exists use 0
        tgt_ext_orig_timestamp = cls(tgt_ext_orig_path).get_modify_timestamp() or 0
        tgt_ext_timestamp = cls(tgt_ext_path).get_modify_timestamp() or 0
        return int(tgt_ext_orig_timestamp) == int(tgt_ext_timestamp)

    # find ext source use unit path
    @classmethod
    def _get_unit_ext_src_as_ext_tgt_(cls, file_path_any, ext_tgt, search_directory_path=None):
        path_base, ext_any = os.path.splitext(file_path_any)
        if ext_any == ext_tgt:
            if search_directory_path:
                name_base = os.path.basename(path_base)
                path_base = '{}/{}'.format(search_directory_path, name_base)

            glob_pattern = '{}.*'.format(path_base)

            ext_src = cls._get_unit_name_base_same_ext_(
                file_path_any, bsc_core.StgExtraMtd.get_paths_by_fnmatch_pattern(glob_pattern)
            )
            if ext_src is not None:
                return ext_src
        return ext_any

    # find path source use unit path
    @classmethod
    def _get_unit_path_src_as_ext_tgt_(cls, file_path_any, ext_tgt):
        path_base, ext_any = os.path.splitext(file_path_any)
        if ext_any == ext_tgt:
            ext_src = cls._get_unit_ext_src_as_ext_tgt_(file_path_any, ext_tgt)
            if ext_src is not None:
                return u'{}{}'.format(path_base, ext_src)
        return file_path_any

    #
    @classmethod
    def _get_unit_name_base_same_ext_(cls, file_path_any, file_paths_any):
        name_base, ext_any = os.path.splitext(os.path.basename(file_path_any))
        for i_file_path in file_paths_any:
            i_name_base, i_ext = os.path.splitext(os.path.basename(i_file_path))
            if i_name_base == name_base:
                if i_ext != ext_any:
                    return i_ext

    @classmethod
    def _get_unit_format_convert_used_color_space_src_(cls, file_path_src):
        return cls.generate_color_space_configure_for_aces().to_aces_color_space(
            cls.generate_color_space_configure_for_convert().get_color_space_src(file_path_src)
        )

    @classmethod
    def _get_unit_tx_create_used_color_space_src_(cls, file_path_src):
        path_base, ext_any = os.path.splitext(file_path_src)
        #
        if ext_any.lower() == '.tx':
            return cls.generate_color_space_configure_for_aces().get_default_color_space()
        elif ext_any.lower() == '.exr':
            file_opt = bsc_core.StgFileOpt(file_path_src)
            if file_opt.get_is_match_name_pattern('*.z_disp.*.exr'):
                return cls.generate_color_space_configure_for_aces().to_aces_color_space(
                    cls.generate_color_space_configure_for_convert().get_color_space_src(file_path_src)
                )
            return cls.generate_color_space_configure_for_aces().get_default_color_space()
        # not "exr"
        return cls.generate_color_space_configure_for_aces().to_aces_color_space(
            cls.generate_color_space_configure_for_convert().get_color_space_src(file_path_src)
        )

    @classmethod
    def _get_unit_is_exists_as_tgt_ext_by_src_(cls, file_path_src, ext_tgt, search_directory_path=None):
        file_path_src = bsc_core.auto_encode(file_path_src)
        name = os.path.basename(file_path_src)
        name_base, ext_any = os.path.splitext(name)
        directory_path = os.path.dirname(file_path_src)
        if search_directory_path:
            tgt_ext_path = '{}/{}{}'.format(search_directory_path, name_base, ext_tgt)
        else:
            tgt_ext_path = '{}/{}{}'.format(directory_path, name_base, ext_tgt)
        #
        tgt_ext_orig_path = file_path_src
        tgt_ext_orig_timestamp = cls(tgt_ext_orig_path).get_modify_timestamp() or 0
        tgt_ext_timestamp = cls(tgt_ext_path).get_modify_timestamp() or 0
        return int(tgt_ext_orig_timestamp) == int(tgt_ext_timestamp)

    @classmethod
    def _set_unit_tx_create_by_src_(cls, file_path_src, search_directory_path=None, block=False):
        path_base, ext_any = os.path.splitext(file_path_src)
        if ext_any != cls.TX_EXT:
            import lxarnold.core as and_core

            color_space_src = cls._get_unit_tx_create_used_color_space_src_(file_path_src)
            #
            use_aces = cls.generate_color_space_configure_for_aces().get_is_enable()
            aces_color_spaces = cls.generate_color_space_configure_for_aces().get_all_color_spaces()
            aces_render_color_space = cls.generate_color_space_configure_for_aces().get_default_color_space()
            aces_file = cls.generate_color_space_configure_for_aces().get_ocio_file()
            if cls._get_unit_is_exists_as_tgt_ext_by_src_(
                    file_path_src,
                    ext_tgt=cls.TX_EXT,
                    search_directory_path=search_directory_path,
            ) is False:
                return and_core.AndTextureOpt(file_path_src).set_unit_tx_create(
                    color_space=color_space_src,
                    use_aces=use_aces,
                    aces_file=aces_file,
                    aces_color_spaces=aces_color_spaces,
                    aces_render_color_space=aces_render_color_space,
                    search_directory_path=search_directory_path,
                    block=block
                )
        return True

    @classmethod
    def _get_unit_tx_create_cmd_by_src_(cls, file_path_src, search_directory_path=None):
        path_base, ext_any = os.path.splitext(file_path_src)
        if ext_any != cls.TX_EXT:
            import lxarnold.core as and_core

            color_space_src = cls._get_unit_tx_create_used_color_space_src_(file_path_src)
            #
            use_aces = cls.generate_color_space_configure_for_aces().get_is_enable()
            aces_color_spaces = cls.generate_color_space_configure_for_aces().get_all_color_spaces()
            aces_render_color_space = cls.generate_color_space_configure_for_aces().get_default_color_space()
            aces_file = cls.generate_color_space_configure_for_aces().get_ocio_file()
            if cls._get_unit_is_exists_as_tgt_ext_by_src_(
                    file_path_src,
                    ext_tgt=cls.TX_EXT,
                    search_directory_path=search_directory_path,
            ) is False:
                return and_core.AndTextureOpt(file_path_src).get_unit_tx_create_cmd(
                    color_space_src=color_space_src,
                    use_aces=use_aces,
                    aces_file=aces_file,
                    aces_color_spaces=aces_color_spaces,
                    aces_render_color_space=aces_render_color_space,
                    search_directory_path=search_directory_path,
                )

    @classmethod
    def _get_unit_tx_create_cmd_by_src_force_(cls, file_path_src, search_directory_path=None):
        path_base, ext_any = os.path.splitext(file_path_src)
        if ext_any != cls.TX_EXT:
            import lxarnold.core as and_core

            color_space_src = cls._get_unit_tx_create_used_color_space_src_(file_path_src)
            #
            use_aces = cls.generate_color_space_configure_for_aces().get_is_enable()
            aces_color_spaces = cls.generate_color_space_configure_for_aces().get_all_color_spaces()
            aces_render_color_space = cls.generate_color_space_configure_for_aces().get_default_color_space()
            aces_file = cls.generate_color_space_configure_for_aces().get_ocio_file()
            return and_core.AndTextureOpt(file_path_src).get_unit_tx_create_cmd(
                color_space_src=color_space_src,
                use_aces=use_aces,
                aces_file=aces_file,
                aces_color_spaces=aces_color_spaces,
                aces_render_color_space=aces_render_color_space,
                search_directory_path=search_directory_path,
            )

    # tx create command
    @classmethod
    def _get_unit_create_cmd_as_ext_tgt_by_src_force_(
            cls, file_path_src, ext_tgt, search_directory_path=None, width=None
            ):
        path_base, ext_any = os.path.splitext(file_path_src)
        if ext_any != ext_tgt:
            # tx use arnold
            if ext_tgt == cls.TX_EXT:
                return cls._get_unit_tx_create_cmd_by_src_force_(
                    file_path_src, search_directory_path
                )
            # other use oiio
            else:
                return bsc_core.ImgFileOpt(
                    file_path_src
                ).get_create_cmd_as_ext_tgt(
                    ext_tgt,
                    search_directory_path,
                    width
                )

    @classmethod
    def _set_unit_jpg_create_(cls, file_path, block=False):
        path_base, ext_any = os.path.splitext(file_path)
        if ext_any != cls.JPG_EXT:
            if cls._get_unit_is_exists_as_ext_tgt_(file_path, ext_tgt=cls.JPG_EXT) is False:
                return bsc_core.ImgFileOpt(file_path).get_jpg(width=2048, block=block)
        return True

    @classmethod
    def _create_unit_exr_as_acescg_(cls, file_path_src, file_path_tgt, use_update_mode=True):
        import lxarnold.core as and_core

        color_space_src = cls._get_unit_format_convert_used_color_space_src_(file_path_src)
        color_space_tgt = 'ACES - ACEScg'
        #
        cmd = and_core.AndTextureOpt.get_create_exr_as_acescg_command(
            file_path_src=file_path_src, file_path_tgt=file_path_tgt,
            color_space_src=color_space_src, color_space_tgt=color_space_tgt,
            use_update_mode=use_update_mode
        )
        bsc_core.SubProcessMtd.execute_with_result(
            cmd
        )

    @classmethod
    def _get_unit_exr_create_cmd_as_acescg_(cls, file_path_src, file_path_tgt, use_update_mode=True):
        import lxarnold.core as and_core

        color_space_src = cls._get_unit_format_convert_used_color_space_src_(file_path_src)
        color_space_tgt = 'ACES - ACEScg'
        #
        cmd = and_core.AndTextureOpt.get_create_exr_as_acescg_command(
            file_path_src=file_path_src, file_path_tgt=file_path_tgt,
            color_space_src=color_space_src, color_space_tgt=color_space_tgt,
            use_update_mode=use_update_mode
        )
        return cmd

    @classmethod
    def _create_unit_tx_as_acescg_(cls, file_path_src, file_path_tgt, use_update_mode=True):
        import lxarnold.core as and_core

        color_space_src = cls._get_unit_tx_create_used_color_space_src_(file_path_src)
        color_space_tgt = 'ACES - ACEScg'
        cmd = and_core.AndTextureOpt.get_create_tx_as_acescg_command(
            file_path_src=file_path_src, file_path_tgt=file_path_tgt,
            color_space_src=color_space_src, color_space_tgt=color_space_tgt,
            use_update_mode=use_update_mode
        )
        bsc_core.SubProcessMtd.execute_with_result(cmd)

    @classmethod
    def _get_unit_tx_create_cmd_as_acescg_(cls, file_path_src, file_path_tgt, use_update_mode=True):
        import lxarnold.core as and_core

        color_space_src = cls._get_unit_tx_create_used_color_space_src_(file_path_src)
        color_space_tgt = 'ACES - ACEScg'
        cmd = and_core.AndTextureOpt.get_create_tx_as_acescg_command(
            file_path_src=file_path_src, file_path_tgt=file_path_tgt,
            color_space_src=color_space_src, color_space_tgt=color_space_tgt,
            use_update_mode=use_update_mode
        )
        return cmd

    @classmethod
    def _convert_unit_format_(cls, file_path_src, file_path_tgt, color_space_src, color_space_tgt):
        import lxarnold.core as and_core

        cmd = and_core.AndTextureOpt.get_create_exr_as_acescg_command(
            file_path_src=file_path_src, file_path_tgt=file_path_tgt,
            color_space_src=color_space_src, color_space_tgt=color_space_tgt
        )
        bsc_core.SubProcessMtd.execute_with_result(cmd)

    # find path source use multipy path
    @classmethod
    def _get_path_src_as_ext_tgt_(cls, file_path_any, ext_tgt, search_directory_path=None):
        path_base, ext_any = os.path.splitext(file_path_any)
        if ext_any == ext_tgt:
            _ = cls.get_exists_unit_paths_fnc(file_path_any)
            if _:
                ext_src = cls._get_unit_ext_src_as_ext_tgt_(_[0], ext_tgt, search_directory_path)
                if ext_src is not None:
                    if search_directory_path:
                        name_base = os.path.basename(path_base)
                        path_base = u'{}/{}'.format(search_directory_path, name_base)
                    return u'{}{}'.format(path_base, ext_src)
        return file_path_any

    @classmethod
    def _get_path_tgt_as_ext_tgt_(cls, file_path_any, ext_tgt, search_directory_path=None):
        path_base, ext_any = os.path.splitext(file_path_any)
        if ext_any != ext_tgt:
            if search_directory_path:
                name_base = os.path.basename(path_base)
                path_base = u'{}/{}'.format(search_directory_path, name_base)
            return u'{}{}'.format(path_base, ext_tgt)
        return file_path_any

    @classmethod
    def _get_path_args_as_ext_tgt_(cls, file_path_any, ext_tgt):
        return cls._get_path_src_as_ext_tgt_(file_path_any, ext_tgt), cls._get_path_tgt_as_ext_tgt_(
            file_path_any, ext_tgt
            )

    @classmethod
    def _get_path_args_as_ext_tgt_by_directory_args_(cls, file_path_any, ext_tgt, directory_path_args):
        directory_path_src, directory_path_tgt = directory_path_args
        return (
            cls._get_path_src_as_ext_tgt_(file_path_any, ext_tgt, directory_path_src),
            cls._get_path_tgt_as_ext_tgt_(file_path_any, ext_tgt, directory_path_tgt)
        )

    @classmethod
    def _get_is_exists_as_tgt_ext_by_src_(cls, file_path_src, ext_tgt, search_directory_path=None):
        file_paths_src = cls._get_exists_file_paths_(file_path_src)
        for i_file_path_src in file_paths_src:
            if cls._get_unit_is_exists_as_tgt_ext_by_src_(
                    i_file_path_src,
                    ext_tgt,
                    search_directory_path,
            ) is False:
                return False
        return True

    @classmethod
    def _get_is_exists_as_tgt_ext_(cls, file_path_any, ext_tgt, search_directory_path=None):
        file_path_src = cls._get_path_src_as_ext_tgt_(file_path_any, ext_tgt)
        return cls._get_is_exists_as_tgt_ext_by_src_(
            file_path_src, ext_tgt, search_directory_path
        )

    def __init__(self, path):
        super(AbsOsTexture, self).__init__(path)

        self.generate_color_space_configure_for_convert()
        self.generate_color_space_configure_for_aces()

    @property
    def icon(self):
        return bsc_core.ResourceIcon.get('file/image')

    def get_args_as_ext_tgt(self, ext_tgt):
        path_src, path_tgt = self._get_path_args_as_ext_tgt_(self.path, ext_tgt)
        src, tgt = self.__class__(path_src), self.__class__(path_tgt)
        # if src.ext == ext_tgt:
        #     src = None
        # if not self.get_exists_unit_paths_fnc(path_tgt):
        #     tgt = None
        return src, tgt

    def get_args_as_tx(self):
        return self.get_args_as_ext_tgt(self.TX_EXT)

    def get_args_as_ext_tgt_by_directory_args(self, ext_tgt, directory_path_args):
        path_src, path_tgt = self._get_path_args_as_ext_tgt_by_directory_args_(self.path, ext_tgt, directory_path_args)
        src, tgt = self.__class__(path_src), self.__class__(path_tgt)
        # if src.ext == ext_tgt:
        #     src = None
        # if not self.get_exists_unit_paths_fnc(path_tgt):
        #     tgt = None
        return src, tgt

    def get_args_as_tx_by_directory_args(self, directory_path_args):
        return self.get_args_as_ext_tgt_by_directory_args(
            self.TX_EXT, directory_path_args
        )

    # udim
    def get_exists_udim_file_paths(self, with_tx=True):
        list_ = []
        path = self.path
        re_pattern = re.compile(self.RE_UDIM_PATTERN, re.IGNORECASE)
        results = re.findall(re_pattern, path)
        if results:
            glob_pattern = path.replace(results[0], '*')
            #
            list_ = glob.glob(glob_pattern)
            if list_:
                if with_tx is True:
                    tx_list = []
                    for i in list_:
                        i_tx_file_path = self._get_path_tgt_as_ext_tgt_(i, ext_tgt=self.TX_EXT)
                        if os.path.isfile(i_tx_file_path):
                            tx_list.append(i_tx_file_path)
                        else:
                            bsc_core.Log.trace_warning(
                                u'texture-tx: "{}" is non-exists.'.format(i_tx_file_path)
                            )
                    #
                    if tx_list:
                        list_.extend(tx_list)
            else:
                bsc_core.Log.trace_warning(
                    u'texture-udim: "{}" is non-exists.'.format(self.path)
                )
        #
        if list_:
            list_.sort()
        return list_

    def get_exists_udim_files(self, with_tx=True):
        return [self.__class__(i) for i in self.get_exists_udim_file_paths(with_tx)]

    def get_udim_numbers(self):
        list_ = []
        if self.get_is_udim():
            p = r'<udim>'
            r = re.finditer(p, self.path, re.IGNORECASE) or []
            start, end = list(r)[0].span()
            file_paths = self.get_exists_udim_file_paths(with_tx=False)
            for file_path in file_paths:
                list_.append(int(file_path[start:start+4]))
        if list_:
            list_.sort()
        return list_

    def _get_tgt_ext_is_exists_(self, ext_tgt):
        # TODO: if ext is ".tx", "*.1001.exr" is exists and "*.1001.tx" is lost
        _ = self.get_exists_units()
        if _:
            # find orig ext
            orig_ext = None
            for i in _:
                if orig_ext is None:
                    i_orig_ext = self._get_unit_ext_src_as_ext_tgt_(i.path, ext_tgt)
                    if i_orig_ext != ext_tgt:
                        orig_ext = i_orig_ext
                #
                orig_file_path = self._get_path_tgt_as_ext_tgt_(i.path, orig_ext)
                if os.path.isfile(orig_file_path):
                    if i._get_unit_is_exists_as_ext_tgt_(orig_file_path, ext_tgt) is False:
                        return False
            return True

    def _get_tgt_ext_orig_path_(self, ext_tgt):
        ext = self.ext
        if ext == ext_tgt:
            _ = self.get_exists_units()
            for i in _:
                print self._get_unit_ext_src_as_ext_tgt_(i.path, ext_tgt), 'AAA'
        return ext_tgt

    def get_tx_orig_path(self):
        _ = self._get_exists_file_paths_(self.path)
        if _:
            path_base, ext = os.path.splitext(self.path)
            ext_src = self._get_unit_ext_src_as_ext_tgt_(_[0], self.TX_EXT)
            if ext_src is not None:
                return u'{}{}'.format(path_base, ext_src)

    def get_tx_orig(self):
        _ = self.get_tx_orig_path()
        if _ is not None:
            return self.__class__(_)

    def get_orig_path_as_ext_tgt(self, ext_tgt):
        return self._get_path_src_as_ext_tgt_(
            self.path,
            ext_tgt
        )

    def get_path_as_tgt_ext(self, ext_tgt, search_directory_path=None):
        return self._get_path_tgt_as_ext_tgt_(
            self.path,
            ext_tgt,
            search_directory_path
        )

    def get_as_tgt_ext(self, ext_tgt, search_directory_path=None):
        return self.__class__(
            self.get_path_as_tgt_ext(ext_tgt, search_directory_path)
        )

    def set_directory_repath_to(self, directory_path_tgt):
        return self.__class__(
            u'{}/{}'.format(
                directory_path_tgt, self.get_name()
            )
        )

    def set_ext_rename_to(self, ext_tgt):
        return self.__class__(
            u'{}{}'.format(
                self.get_path_base(), ext_tgt
            )
        )

    # tx
    def get_path_as_tx(self, search_directory_path=None):
        return self.get_path_as_tgt_ext(
            self.TX_EXT, search_directory_path
        )

    def get_as_tx(self, search_directory_path=None):
        return self.get_as_tgt_ext(
            self.TX_EXT, search_directory_path
        )

    def get_is_exists_as_tgt_ext(self, ext_tgt, search_directory_path=None):
        return self._get_is_exists_as_tgt_ext_(
            self.path,
            ext_tgt,
            search_directory_path
        )

    def get_is_exists_as_tx(self, search_directory_path=None):
        return self.get_is_exists_as_tgt_ext(
            self.TX_EXT, search_directory_path
        )

    def get_orig_as_tgt_ext(self, ext_tgt):
        _ = self.get_orig_path_as_ext_tgt(ext_tgt)
        if _ is not None:
            return self.__class__(_)

    def get_tx_has_orig(self):
        return self.get_tx_orig_path() is not None

    def get_ext_is_tx(self):
        return self.ext == self.TX_EXT

    def get_ext_is_jpg(self):
        return self.ext == self.JPG_EXT

    def get_ext_is_exr(self):
        return self.ext == self.EXR_EXT

    def get_color_space(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            return self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES.to_aces_color_space(
                self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT.get_color_space(file_path)
            )

    def get_color_space_src(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            if self.get_ext_is_tx():
                return self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES.get_default_color_space()
            elif self.get_ext_is_exr():
                return self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES.get_default_color_space()
            return self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES.to_aces_color_space(
                self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT.get_color_space_src(file_path)
            )

    def get_best_color_space(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            return self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_ACES.to_aces_color_space(
                self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT.get_color_space_src(file_path)
            )

    def get_purpose(self):
        return self.TEXTURE_COLOR_SPACE_CONFIGURE_FOR_CONVERT.get_purpose(self.path)

    #
    def get_thumbnail_file_path(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            return bsc_core.ImgFileOpt(
                file_path
            ).get_thumbnail()

    def get_thumbnail_create_args(self):
        pass

    def convert_to_acescg(self, file_path_tgt):
        pass

    def get_info(self):
        return bsc_core.ImgFileOiioOpt(self.path).info


class AbsObjScene(unr_abstracts.AbsObjScene):
    def __init__(self, *args, **kwargs):
        super(AbsObjScene, self).__init__(*args, **kwargs)

    def load_from_location(self, *args, **kwargs):
        self.load_from_location_fnc(*args, **kwargs)

    def load_from_location_fnc(self, *args, **kwargs):
        raise NotImplementedError()


class AbsDccFileReferences(object):
    def __init__(self, *args, **kwargs):
        pass
