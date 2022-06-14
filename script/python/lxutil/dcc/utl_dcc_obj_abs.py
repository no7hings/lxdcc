# coding:utf-8
import os

import re

import glob

import hashlib

import fnmatch

from lxbasic import bsc_core

from lxobj import obj_abstract

from lxutil import utl_core

import lxutil.configures as utl_configures


class AbsStorageGuiDef(object):
    def set_gui_attribute(self, *args, **kwargs):
        raise NotImplementedError()
    @property
    def name(self):
        raise NotImplementedError()
    @property
    def path(self):
        raise NotImplementedError()

    def set_copy_path_to_clipboard(self):
        from lxutil_gui.qt import utl_gui_qt_core
        utl_gui_qt_core.set_text_copy_to_clipboard(self.path)

    def set_copy_name_to_clipboard(self):
        from lxutil_gui.qt import utl_gui_qt_core
        utl_gui_qt_core.set_text_copy_to_clipboard(self.name)


class AbsOsDirectory(
    obj_abstract.AbsOsDirectory,
    obj_abstract.AbsObjGuiDef,
    AbsStorageGuiDef
):
    LOG = utl_core.Log
    def __init__(self, path):
        super(AbsOsDirectory, self).__init__(path)
        self._set_obj_gui_def_init_()
        self.set_gui_attribute(
            'gui_menu',
            [
                ('Open Folder', 'file/folder', self.set_open),
                (),
                ('Copy Path', None, self.set_copy_path_to_clipboard),
                ('Copy Name', None, self.set_copy_name_to_clipboard),
            ]
        )
    @property
    def icon(self):
        return utl_core.FileIcon.get_folder()

    def set_create(self):
        if self.get_is_exists() is False:
            os.makedirs(self.path)
            utl_core.Log.set_module_result_trace(
                'directory create',
                u'directory-path="{}"'.format(self.path)
            )

    def set_link_to(self, tgt_directory_path, force=False):
        tgt_directory = self.__class__(tgt_directory_path)
        if tgt_directory.get_is_exists():
            if force is False:
                utl_core.Log.set_module_warning_trace(
                    'link create',
                    u'path="{}" is exists'.format(tgt_directory.path)
                )
                return
            else:
                if os.path.islink(tgt_directory.path) is True:
                    os.remove(tgt_directory.path)
                    utl_core.Log.set_module_result_trace(
                        'path-link-remove',
                        u'path="{}"'.format(tgt_directory.path)
                    )
        #
        if tgt_directory.get_is_exists() is False:
            self._set_symlink_create_(self.path, tgt_directory.path)
            #
            utl_core.Log.set_module_result_trace(
                'link create',
                u'connection="{}" >> "{}"'.format(self.path, tgt_directory.path)
            )

    def get_directory_paths(self):
        lis = []
        _ = glob.glob(u'{}/*'.format(self.path)) or []
        for i in _:
            if os.path.isdir(i):
                lis.append(i)
        lis.sort()
        return lis

    def get_all_files(self):
        return


class AbsOsFile(
    obj_abstract.AbsOsFile,
    obj_abstract.AbsObjGuiDef,
    AbsStorageGuiDef,
    obj_abstract.AbsOsFilePackageDef
):
    ICON_DICT = {
        '.ma': 'ma',
        '.mb': 'ma',
        '.hip': 'hip',
        '.katana': 'katana',
        '.exr': 'image',
        '.py': 'python'
    }
    OS_DIRECTORY_CLASS = None
    # ignore case
    # multiply
    # udim
    RE_UDIM_KEYS = [
        ('<udim>', 4),
    ]
    # sequence
    RE_SEQUENCE_KEYS = [
        ('#', -1),
        (r'\$F04', 4),
        (r'\$F', 4),
        (r'(\()[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](\))(%04d)', 4),
        (r'%04d', 4),
    ]
    RE_MULTIPLY_KEYS = RE_UDIM_KEYS + RE_SEQUENCE_KEYS
    #
    RE_SEQUENCE_PATTERN = None
    #
    LOG = utl_core.Log
    def __init__(self, path):
        super(AbsOsFile, self).__init__(
            bsc_core.StoragePathOpt(path).__str__()
        )
        self._set_obj_gui_def_init_()
        #
        self.set_gui_attribute(
            'gui_menu',
            [
                ('Open Folder', 'file/folder', self.set_directory_open),
                (),
                ('Copy Path', None, self.set_copy_path_to_clipboard),
                ('Copy Name', None, self.set_copy_name_to_clipboard),
            ]
        )
        # file reference node
        self._obj = None
        self._dcc_attribute_name = None
    @property
    def icon(self):
        if self.ext:
            return utl_core.FileIcon.get_by_file_ext(self.ext)
        return utl_core.FileIcon.get_default()
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
        return self.get_exists_file_paths() != []

    def get_is_udim(self):
        return self._get_is_udim_(self.path)
    @classmethod
    def _get_is_udim_(cls, file_path):
        path_base = os.path.basename(file_path)
        for k, c in cls.RE_UDIM_KEYS:
            r = re.finditer(k, path_base, re.IGNORECASE) or []
            if r:
                return True
        return False

    def get_is_sequence(self):
        return self._get_is_sequence_(self.path)
    @classmethod
    def _get_is_sequence_(cls, file_path):
        path_base = os.path.basename(file_path)
        for k, c in cls.RE_SEQUENCE_KEYS:
            r = re.finditer(k, path_base, re.IGNORECASE) or []
            if r:
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
            utl_core.Log.set_warning_trace('file: "{}" is Non-exists.'.format(self.path))
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
            r = re.finditer(k, path_base, re.IGNORECASE) or []
            if r:
                return True
        return False
    @classmethod
    def _set_file_path_ext_replace_to_(cls, file_path, ext):
        return os.path.splitext(file_path)[0] + ext

    def get_ext_replace(self, ext):
        file_path = self._set_file_path_ext_replace_to_(self.path, ext)
        return self.__class__(file_path)

    def get_has_elements(self):
        return self._get_has_elements_(self.path)
    @classmethod
    def _get_exists_file_paths_(cls, file_path, include_exts=None):
        def get_ext_replace_fnc_(file_path_, ext_):
            return os.path.splitext(file_path_)[0] + ext_
        #
        def get_add_fnc_(include_exts_, ext_):
            if isinstance(include_exts_, (tuple, list)):
                for _ext in include_exts_:
                    if ext_ == _ext:
                        continue
                    for _i in list_:
                        _add = get_ext_replace_fnc_(_i, _ext)
                        if os.path.isfile(_add) is True:
                            add_list_.append(_add)
        #
        re_keys = cls.RE_MULTIPLY_KEYS
        pathsep = cls.PATHSEP
        #
        directory = os.path.dirname(file_path)
        path_base = os.path.basename(file_path)
        base_new = path_base
        ext = os.path.splitext(path_base)[-1]
        for k, c in re_keys:
            r = re.finditer(k, path_base, re.IGNORECASE) or []
            for i in r:
                start, end = i.span()
                if c == -1:
                    s = '[0-9]'
                    base_new = base_new.replace(path_base[start:end], s, 1)
                else:
                    s = '[0-9]'*c
                    base_new = base_new.replace(path_base[start:end], s, 1)
        #
        glob_pattern = pathsep.join([directory, base_new])
        #
        list_ = glob.glob(glob_pattern)
        if list_:
            list_.sort()
        #
        add_list_ = []
        get_add_fnc_(include_exts, ext)
        _ = list_ + add_list_
        return [i for i in _ if os.path.isfile(i)]

    def get_exists_file_paths(self, *args, **kwargs):
        return self._get_exists_file_paths_(self.path, **kwargs)

    def get_exists_files(self, *args, **kwargs):
        return [self.__class__(i) for i in self.get_exists_file_paths(*args, **kwargs)]

    def get_permissions(self, *args, **kwargs):
        return [bsc_core.StoragePathMtd.get_permission(i) for i in self.get_exists_file_paths()]

    def get_modify_timestamp(self, *args, **kwargs):
        exists_file_paths = self.get_exists_file_paths(*args, **kwargs)
        timestamps = [os.stat(i).st_mtime for i in exists_file_paths]
        if timestamps:
            return sum(timestamps)/len(timestamps)

    def get_time(self):
        if self.get_is_exists() is True:
            timestamp = self.get_modify_timestamp()
            return bsc_core.TimestampOpt(timestamp).get()

    def get_time_tag(self):
        timestamp = self.get_modify_timestamp()
        return bsc_core.TimestampOpt(timestamp).get_as_tag()

    def get_is_same_timestamp_to(self, file_obj):
        return str(self.get_modify_timestamp()) == str(file_obj.get_modify_timestamp())

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

    def set_copy_as_src(self, target_tgt_dir_path, target_src_dir_path, fix_name_blank=False, force=False):
        if self.get_is_exists_file():
            timestamp = self.get_modify_timestamp()
            size = self.get_size()
            name = self.name
            if fix_name_blank is True:
                if ' ' in name:
                    name = name.replace(' ', '_')
            #
            time_tag = bsc_core.IntegerOpt(int(timestamp)).set_encode_to_36()
            size_tag = bsc_core.IntegerOpt(int(size)).set_encode_to_36()
            target_tgt_file_path = u'{}/{}'.format(target_tgt_dir_path, name)
            target_src_file_path = u'{}/{}/V-{}-{}.{}'.format(target_src_dir_path, name, time_tag, size_tag, name)
            # copy to src
            self.set_copy_to_file(target_src_file_path)
            target_tgt_file = self.__class__(target_tgt_file_path)
            if target_tgt_file.get_is_exists() is True:
                if force is False:
                    utl_core.Log.set_module_warning_trace(
                        'link create',
                        u'file="{}" is exists'.format(target_tgt_file.path)
                    )
                    return
                else:
                    if os.path.islink(target_tgt_file.path) is True:
                        utl_core.Log.set_module_result_trace(
                            'link remove',
                            u'file="{}"'.format(target_tgt_file.path)
                        )
                        os.remove(target_tgt_file.path)
            #
            if target_tgt_file.get_is_exists() is False:
                target_tgt_file.set_directory_create()
                # link src to target
                self._set_symlink_create_(target_src_file_path, target_tgt_file.path)
                utl_core.Log.set_module_result_trace(
                    'link create',
                    u'connection="{} >> {}"'.format(target_src_file_path, target_tgt_file.path)
                )
        else:
            utl_core.Log.set_warning_trace(
                'file-src-copy',
                'file-path"{}" Non-available'.format(self.path)
            )
    # file reference node ******************************************************************************************** #
    def set_node(self, node):
        self._obj = node

    def get_obj(self):
        return self._obj

    def set_dcc_attribute_name(self, port_path):
        self._dcc_attribute_name = port_path

    def get_dcc_attribute_name(self):
        return self._dcc_attribute_name

    def set_rename(self, new_name):
        new_path = '{}{}{}'.format(self.directory.path, self.PATHSEP, new_name)
        if os.path.exists(self.path) is True and os.path.exists(new_path) is False:
            os.rename(
                self.path, new_path
            )
            utl_core.Log.set_result_trace(
                u'rename file: "{}" > "{}"'.format(self.path, new_path)
            )

    def get_ext_variants(self, include_exts=None):
        path_base, ext = os.path.splitext(self.path)
        glob_pattern = u'{}.*'.format(path_base)
        _ = glob.glob(glob_pattern)
        lis = []
        if _:
            for i in _:
                if i == self.path:
                    continue
                if include_exts is not None:
                    i_base, i_ext = os.path.splitext(i)
                    if i_ext not in include_exts:
                        continue
                lis.append(i)
        return [self.__class__(i) for i in lis]

    def set_ext_replace(self, ext):
        path_base, _ext = os.path.splitext(self.path)
        return self.__class__(path_base+ext)

    def set_delete(self):
        exists_file_paths = self._get_exists_file_paths_(self._path)
        if exists_file_paths:
            for i in exists_file_paths:
                os.remove(i)
                utl_core.Log.set_module_result_trace(
                    'file-delete',
                    u'"{}"'.format(i)
                )

    def get_is_link_source_to(self, file_path):
        pass

    def set_link_to(self, tgt_file_path, force=False):
        tgt_file = self.__class__(tgt_file_path)
        if self.get_is_exists() is True:
            if tgt_file.get_is_exists():
                if force is False:
                    utl_core.Log.set_module_warning_trace(
                        'link create',
                        u'path="{}" is exists'.format(tgt_file.path)
                    )
                    return
                else:
                    if os.path.islink(tgt_file.path) is True:
                        os.remove(tgt_file.path)
                        utl_core.Log.set_module_result_trace(
                            'path-link-remove',
                            u'path="{}"'.format(tgt_file.path)
                        )
            #
            if tgt_file.get_is_exists() is False:
                tgt_file.set_directory_create()
                #
                bsc_core.StorageLinkMtd.set_link_to(
                    self.path, tgt_file.path
                )
                #
                utl_core.Log.set_module_result_trace(
                    'link create',
                    u'link="{} >> {}"'.format(self.path, tgt_file.path)
                )


class AbsOsTexture(AbsOsFile):
    TEXTURE_CFG = utl_configures.get_texture_tx_configure()
    COLOR_SPACE_CFG = utl_configures.get_aces_color_space_configure()
    #
    OS_FILE_CLASS = None
    # sequence
    RE_SEQUENCE_PATTERN = None
    # udim
    RE_UDIM_PATTERN = r'.*?(<udim>).*?'
    #
    TX_EXT = '.tx'
    EXR_EXT = '.exr'
    JPG_EXT = '.jpg'
    def __init__(self, path):
        super(AbsOsTexture, self).__init__(path)
    @property
    def icon(self):
        return utl_core.FileIcon.get_image()
    # udim
    def get_exists_udim_file_paths(self, with_tx=True):
        list_ = []
        path = self.path
        re_pattern = re.compile(self.RE_UDIM_PATTERN, re.IGNORECASE)
        results = re.findall(re_pattern, path)
        if results:
            glob_pattern = path.replace(results[0], '*')
            list_ = glob.glob(glob_pattern)
            if list_:
                if with_tx is True:
                    tx_list = []
                    for i in list_:
                        tx_file_path = self._get_tgt_ext_path_(i, tgt_ext=self.TX_EXT)
                        if os.path.isfile(tx_file_path):
                            tx_list.append(tx_file_path)
                        else:
                            utl_core.Log.set_warning_trace('texture-tx: "{}" is Non-exists.'.format(tx_file_path))
                    if tx_list:
                        list_.extend(tx_list)
            else:
                utl_core.Log.set_warning_trace(u'Udim-texture: "{}" is Non-exists.'.format(self.path))
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

    def get_exists_file_paths(self, with_tx=True):
        if with_tx is True:
            return self._get_exists_file_paths_(self.path, include_exts=[self.TX_EXT])
        return self._get_exists_file_paths_(self.path)

    def get_exists_files(self, with_tx=True):
        return [self.__class__(i) for i in self.get_exists_file_paths(with_tx)]
    @classmethod
    def _get_exists_files_(cls, file_path):
        return [cls(i) for i in cls._get_exists_file_paths_(file_path)]

    def get_permissions(self, with_tx=True):
        return [bsc_core.StoragePathMtd.get_permission(i) for i in self.get_exists_file_paths(with_tx)]
    # tx
    @classmethod
    def _get_unit_tgt_ext_is_exists_(cls, any_file_path, tgt_ext):
        tgt_ext_orig_path = cls._get_unit_tgt_ext_orig_path_(any_file_path, tgt_ext)
        tgt_ext_path = cls._get_tgt_ext_path_(any_file_path, tgt_ext)
        tgt_ext_orig_timestamp = cls(tgt_ext_orig_path).get_modify_timestamp() or 0
        tgt_ext_timestamp = cls(tgt_ext_path).get_modify_timestamp() or 0
        return int(tgt_ext_orig_timestamp) == int(tgt_ext_timestamp)
    @classmethod
    def _get_tgt_ext_path_(cls, file_path, tgt_ext):
        path_base, ext = os.path.splitext(file_path)
        if ext != tgt_ext:
            return u'{}{}'.format(path_base, tgt_ext)
        return file_path
    @classmethod
    def _get_unit_tx_(cls, file_path):
        return cls(cls._get_tgt_ext_path_(file_path, tgt_ext=cls.TX_EXT))
    @classmethod
    def _get_unit_tgt_ext_orig_ext_(cls, file_path, tgt_ext):
        path_base, ext = os.path.splitext(file_path)
        if ext == tgt_ext:
            glob_pattern = u'{}.*'.format(path_base)
            #
            ext_ = cls._get_unit_name_base_same_ext_(
                file_path, utl_core.Path._get_stg_paths_by_parse_pattern_(glob_pattern)
            )
            if ext_ is not None:
                return ext_
        return ext
    @classmethod
    def _get_unit_tgt_ext_orig_path_(cls, file_path, tgt_ext):
        path_base, ext = os.path.splitext(file_path)
        # etc ext=".tx"
        if ext == tgt_ext:
            ext_ = cls._get_unit_tgt_ext_orig_ext_(file_path, tgt_ext)
            if ext_ is not None:
                return '{}{}'.format(path_base, ext_)
        return file_path
    @classmethod
    def _get_unit_name_base_same_ext_(cls, file_path, target_file_paths):
        name_base, ext = os.path.splitext(os.path.basename(file_path))
        for i_file_path in target_file_paths:
            i_name_base, i_ext = os.path.splitext(os.path.basename(i_file_path))
            if i_name_base == name_base:
                if i_ext != ext:
                    return i_ext

    def get_tx_file_path(self):
        return self._get_tgt_ext_path_(self.path, tgt_ext=self.TX_EXT)

    def get_tx(self):
        return self.__class__(
            self.get_tx_file_path()
        )

    def get_tx_is_exists(self):
        return self.get_is_exists_as_tgt_ext(self.TX_EXT)

    def _get_tgt_ext_is_exists_(self, tgt_ext):
        # TODO: if ext is ".tx", "*.1001.exr" is exists and "*.1001.tx" is lost
        _ = self._get_exists_files_(self.path)
        if _:
            # find orig ext
            orig_ext = None
            for i in _:
                if orig_ext is None:
                    i_orig_ext = self._get_unit_tgt_ext_orig_ext_(i.path, tgt_ext)
                    if i_orig_ext != tgt_ext:
                        orig_ext = i_orig_ext
                #
                orig_file_path = self._get_tgt_ext_path_(i.path, orig_ext)
                if os.path.isfile(orig_file_path):
                    if i._get_unit_tgt_ext_is_exists_(orig_file_path, tgt_ext) is False:
                        return False
            return True

    def _get_tgt_ext_orig_path_(self, tgt_ext):
        ext = self.ext
        if ext == tgt_ext:
            _ = self._get_exists_files_(self.path)
            for i in _:
                print self._get_unit_tgt_ext_orig_ext_(i.path, tgt_ext), 'AAA'
        return tgt_ext

    def get_tx_orig_path(self):
        _ = self._get_exists_file_paths_(self.path)
        if _:
            path_base, ext = os.path.splitext(self.path)
            ext_ = self._get_unit_tgt_ext_orig_ext_(_[0], self.TX_EXT)
            if ext_ is not None:
                return '{}{}'.format(path_base, ext_)

    def get_tx_orig(self):
        _ = self.get_tx_orig_path()
        if _ is not None:
            return self.__class__(_)

    def get_tgt_ext_orig_path(self, tgt_ext):
        _ = self._get_exists_file_paths_(self.path)
        if _:
            path_base, ext = os.path.splitext(self.path)
            ext_ = self._get_unit_tgt_ext_orig_ext_(_[0], tgt_ext)
            if ext_ is not None:
                return '{}{}'.format(path_base, ext_)

    def get_path_as_tgt_ext(self, tgt_ext):
        return self._get_tgt_ext_path_(self.path, tgt_ext)

    def get_as_tgt_ext(self, tgt_ext):
        return self.__class__(
            self.get_path_as_tgt_ext(tgt_ext)
        )

    def get_orig_as_tgt_ext(self, tgt_ext):
        _ = self.get_tgt_ext_orig_path(tgt_ext)
        if _ is not None:
            return self.__class__(_)

    def get_tx_has_orig(self):
        return self.get_tx_orig_path() is not None

    def get_is_tx_ext(self):
        return self.ext == self.TX_EXT

    def get_is_jpg_ext(self):
        return self.ext == self.JPG_EXT

    def get_is_tgt_ext(self, ext):
        return self.ext == ext

    def get_is_exists_as_tgt_ext(self, tgt_ext):
        return self._get_tgt_ext_is_exists_(tgt_ext)

    def get_is_exr(self):
        return self.ext == self.EXR_EXT

    def get_color_space(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            return self.COLOR_SPACE_CFG.get_aces_color_space(
                self.TEXTURE_CFG.get_color_space(file_path)
            )

    def get_used_color_space(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            if self.get_is_tx_ext():
                return self.COLOR_SPACE_CFG.get_aces_render_color_space()
            elif self.get_is_exr():
                return self.COLOR_SPACE_CFG.get_aces_render_color_space()
            return self.COLOR_SPACE_CFG.get_aces_color_space(
                self.TEXTURE_CFG.get_used_color_space(file_path)
            )
    @classmethod
    def _get_unit_used_color_space_(cls, file_path):
        path_base, ext = os.path.splitext(file_path)
        if ext.lower() == '.tx':
            return cls.COLOR_SPACE_CFG.get_aces_render_color_space()
        elif ext.lower() == '.exr':
            file_opt = bsc_core.StorageFileOpt(file_path)
            if file_opt.get_is_match_name_pattern('*.z_disp.*.exr'):
                return cls.COLOR_SPACE_CFG.get_aces_color_space(
                    cls.TEXTURE_CFG.get_used_color_space(file_path)
                )
            return cls.COLOR_SPACE_CFG.get_aces_render_color_space()
        return cls.COLOR_SPACE_CFG.get_aces_color_space(
            cls.TEXTURE_CFG.get_used_color_space(file_path)
        )

    def get_purpose(self):
        return self.TEXTURE_CFG.get_purpose(self.path)

    def set_tx_create(self, force=False):
        lis = []
        if self.get_is_tx_ext() is False:
            from lxarnold import and_core
            #
            color_space = self.get_used_color_space()
            #
            use_aces = self.COLOR_SPACE_CFG.get_is_use_aces()
            aces_color_spaces = self.COLOR_SPACE_CFG.get_aces_color_spaces()
            aces_render_color_space = self.COLOR_SPACE_CFG.get_aces_render_color_space()
            aces_file = self.COLOR_SPACE_CFG.get_aces_file()
            exists_files = self.get_exists_files()
            if exists_files:
                for i_tile in exists_files:
                    if i_tile.get_tx_is_exists() is False or force is True:
                        and_core.AndTextureOpt_(i_tile.path).set_tx_create(
                            color_space, use_aces, aces_file, aces_color_spaces, aces_render_color_space
                        )
                        lis.append(i_tile.path)
        return lis
    @classmethod
    def _get_unit_jpg_is_exists_(cls, file_path):
        pass
    @classmethod
    def _set_unit_tx_create_(cls, file_path, block=False):
        path_base, ext = os.path.splitext(file_path)
        if ext != cls.TX_EXT:
            from lxarnold import and_core
            #
            color_space = cls._get_unit_used_color_space_(file_path)
            #
            use_aces = cls.COLOR_SPACE_CFG.get_is_use_aces()
            aces_color_spaces = cls.COLOR_SPACE_CFG.get_aces_color_spaces()
            aces_render_color_space = cls.COLOR_SPACE_CFG.get_aces_render_color_space()
            aces_file = cls.COLOR_SPACE_CFG.get_aces_file()
            if cls._get_unit_tgt_ext_is_exists_(file_path, tgt_ext=cls.TX_EXT) is False:
                return and_core.AndTextureOpt_(file_path)._set_unit_tx_create_(
                    color_space, use_aces, aces_file, aces_color_spaces, aces_render_color_space, block
                )
        return True
    @classmethod
    def _set_unit_jpg_create_(cls, file_path, block=False):
        path_base, ext = os.path.splitext(file_path)
        if ext != cls.JPG_EXT:
            if cls._get_unit_tgt_ext_is_exists_(file_path, tgt_ext=cls.JPG_EXT) is False:
                return bsc_core.ImageOpt(file_path).get_jpg(width=2048, block=block)
        return True
    #
    def get_thumbnail_file_path(self):
        _ = self._get_exists_file_paths_(self._path)
        if _:
            file_path = _[0]
            return bsc_core.ImageOpt(
                file_path
            ).get_thumbnail()


class AbsObjScene(obj_abstract.AbsObjScene):
    def __init__(self, *args, **kwargs):
        super(AbsObjScene, self).__init__(*args, **kwargs)

    def set_load_by_root(self, *args, **kwargs):
        self._set_load_by_root_(*args, **kwargs)

    def _set_load_by_root_(self, *args, **kwargs):
        raise NotImplementedError()


class AbsDccFileReferences(object):
    def __init__(self, *args, **kwargs):
        pass
