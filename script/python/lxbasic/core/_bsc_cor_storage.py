# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw, _bsc_cor_pattern, _bsc_cor_dict, _bsc_cor_environ, _bsc_cor_process, _bsc_cor_thread


class StgUserMtd(object):
    @classmethod
    def get_user_temporary_directory(cls, create=False):
        date_tag = TimeMtd.get_date_tag()
        if SystemMtd.get_is_windows():
            _ = '{}/temporary/{}'.format(
                bsc_configure.UserDirectory.WINDOWS, date_tag
            )
        elif SystemMtd.get_is_linux():
            _ = '{}/temporary/{}'.format(
                bsc_configure.UserDirectory.LINUX, date_tag
            )
        else:
            raise SystemError()
        if create:
            StorageMtd.set_directory_create(_)
        return _
    @classmethod
    def get_user_debug_directory(cls, tag=None, create=False):
        date_tag = TimeMtd.get_date_tag()
        if SystemMtd.get_is_windows():
            root = bsc_configure.UserDirectory.WINDOWS
            _ = '{}/debug/{}'.format(root, date_tag)
        elif SystemMtd.get_is_linux():
            _ = '{}/debug/{}'.format(bsc_configure.UserDirectory.LINUX, date_tag)
        else:
            raise SystemError()
        if tag is not None:
            _ = '{}/{}'.format(_, tag)
        if create:
            StorageMtd.set_directory_create(_)
        return _
    @classmethod
    def get_user_session_directory(cls, create=False):
        date_tag = TimeMtd.get_date_tag()
        if SystemMtd.get_is_windows():
            _ = '{}/.session/{}'.format(bsc_configure.UserDirectory.WINDOWS, date_tag)
        elif SystemMtd.get_is_linux():
            _ = '{}/.session/{}'.format(bsc_configure.UserDirectory.LINUX, date_tag)
        else:
            raise SystemError()
        if create:
            StorageMtd.set_directory_create(_)
        return _
    @classmethod
    def get_user_session_file(cls, unique_id=None):
        directory_path = cls.get_user_session_directory()
        if unique_id is None:
            unique_id = UuidMtd.get_new()
        return '{}/{}.yml'.format(directory_path, unique_id)


class StgExtraMtd(object):
    @classmethod
    def set_directory_open(cls, path):
        if SystemMtd.get_is_windows():
            cmd = u'explorer "{}"'.format(path.replace('/', '\\'))
            # subprocess.Popen(cmd, shell=True)
        elif SystemMtd.get_is_linux():
            cmd = u'nautilus "{}"'.format(path)
            # subprocess.Popen(cmd, shell=True)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(
                _bsc_cor_process.SubProcessMtd.set_run_with_result, cmd
            )
        )
        t_0.start()
        # t_0.join()
    @classmethod
    def set_file_open(cls, path):
        if SystemMtd.get_is_windows():
            cmd = u'explorer /select,"{}"'.format(path.replace('/', '\\'))
            # subprocess.Popen(cmd, shell=True)

        elif SystemMtd.get_is_linux():
            cmd = u'nautilus "{}" --select'.format(path)
            # subprocess.Popen(cmd, shell=True)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(
                _bsc_cor_process.SubProcessMtd.set_run_with_result, cmd
            )
        )
        t_0.start()
        # t_0.join()
    @classmethod
    def get_paths_by_fnmatch_pattern(cls, pattern, sort_by='number'):
        _ = glob.glob(pattern) or []
        if _:
            # fix windows path
            if platform.system() == 'Windows':
                _ = [i.replace('\\', '/') for i in _]
            if len(_) > 1:
                # sort by number
                if sort_by == 'number':
                    _.sort(key=lambda x: _bsc_cor_raw.RawTextMtd.to_number_embedded_args(x))
        return _


class StgPathLinkMtd(object):
    @classmethod
    def set_link_to(cls, path_src, path_tgt):
        if os.path.exists(path_tgt) is False:
            tgt_dir_path = os.path.dirname(path_tgt)
            src_rel_path = os.path.relpath(path_src, tgt_dir_path)
            os.symlink(src_rel_path, path_tgt)
    @classmethod
    def get_is_link_source_to(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        src_rel_path = os.path.relpath(path_src, tgt_dir_path)
        if os.path.islink(path_tgt):
            orig_src_rel_path = os.readlink(path_tgt)
            return src_rel_path == orig_src_rel_path
        return False
    @classmethod
    def get_rel_path(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        return os.path.relpath(path_src, tgt_dir_path)
    @classmethod
    def get_is_link(cls, path):
        return os.path.islink(path)
    @classmethod
    def get_link_source(cls, path_tgt):
        cur_path = path_tgt
        while True:
            if os.path.exists(cur_path):
                if os.path.islink(cur_path) is True:
                    cur_directory_path = os.path.dirname(cur_path)
                    os.chdir(cur_directory_path)
                    cur_path = os.path.abspath(os.readlink(cur_path))
                else:
                    break
            else:
                break
        return cur_path
    @classmethod
    def set_file_link_to(cls, path_src, path_tgt):
        if os.path.isfile(path_src):
            if os.path.islink(path_src):
                path_src = cls.get_link_source(path_src)
            #
            if os.path.exists(path_tgt) is False:
                tgt_dir_path = os.path.dirname(path_tgt)
                src_rel_path = os.path.relpath(path_src, tgt_dir_path)
                os.symlink(src_rel_path, path_tgt)


class StgDirectoryMtd(object):
    @classmethod
    def get_file_paths(cls, directory_path, include_exts=None):
        list_ = []
        if os.path.isdir(directory_path):
            results = os.listdir(directory_path) or []
            # results.sort()
            for i_name in results:
                i_path = '{}/{}'.format(directory_path, i_name)
                if os.path.isfile(i_path):
                    if isinstance(include_exts, (tuple, list)):
                        i_name_base, i_ext = os.path.splitext(i_name)
                        if i_ext not in include_exts:
                            continue
                    #
                    list_.append(i_path)
        return list_
    @classmethod
    def _get_file_paths(cls, directory_path, include_exts=None):
        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            for i in scandir.scandir(directory_path):
                if i.is_file():
                    i_path = i.path
                    if isinstance(include_exts, (tuple, list)):
                        i_base, i_ext = os.path.splitext(i_path)
                        if i_ext not in include_exts:
                            continue
                    #
                    list_.append(i_path)
        return list_
    @classmethod
    def get_file_paths__(cls, directory_path, include_exts=None):
        if SystemMtd.get_is_linux():
            return cls._get_file_paths(directory_path, include_exts)
        else:
            return cls.get_file_paths(directory_path, include_exts)
    @classmethod
    def get_all_file_paths(cls, directory_path, include_exts=None):
        def rcs_fnc_(path_):
            _results = os.listdir(path_) or []
            # _results.sort()
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isfile(_i_path):
                    if isinstance(include_exts, (tuple, list)):
                        _i_name_base, _i_ext = os.path.splitext(_i_name)
                        if _i_ext not in include_exts:
                            continue
                    #
                    list_.append(_i_path)
                elif os.path.isdir(_i_path):
                    rcs_fnc_(_i_path)

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        return list_
    @classmethod
    def _get_all_file_paths(cls, directory_path, include_exts=None):
        def rcs_fnc_(path_):
            for _i in scandir.scandir(path_):
                _i_path = _i.path
                if _i.is_file():
                    if isinstance(include_exts, (tuple, list)):
                        _i_base, _i_ext = os.path.splitext(_i_path)
                        if _i_ext not in include_exts:
                            continue
                    #
                    list_.append(_i_path)
                elif _i.is_dir():
                    rcs_fnc_(_i_path)

        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        return list_
    @classmethod
    def get_all_file_paths__(cls, directory_path, include_exts=None):
        if SystemMtd.get_is_linux():
            return cls._get_all_file_paths(directory_path, include_exts)
        else:
            return cls.get_all_file_paths(directory_path, include_exts)
    @classmethod
    def get_directory_paths(cls, directory_path):
        list_ = []
        if os.path.isdir(directory_path):
            results = os.listdir(directory_path) or []
            # results.sort()
            for i_name in results:
                i_path = '{}/{}'.format(directory_path, i_name)
                if os.path.isdir(i_path):
                    list_.append(i_path)
        return list_
    @classmethod
    def _get_directory_paths(cls, directory_path):
        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            for i in scandir.scandir(directory_path):
                if i.is_dir():
                    list_.append(i.path)
        return list_
    @classmethod
    def get_directory_paths__(cls, directory_path):
        if SystemMtd.get_is_linux():
            return cls._get_directory_paths(directory_path)
        else:
            return cls.get_directory_paths(directory_path)
    @classmethod
    def get_all_directory_paths(cls, directory_path):
        def rcs_fnc_(path_):
            _results = os.listdir(path_) or []
            # _results.sort()
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isdir(_i_path):
                    list_.append(_i_path)
                    rcs_fnc_(_i_path)

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        return list_
    @classmethod
    def _get_all_directory_paths(cls, directory_path):
        def rcs_fnc_(d_):
            for _i in scandir.scandir(d_):
                if _i.is_dir():
                    _i_path = _i.path
                    list_.append(_i_path)
                    rcs_fnc_(_i_path)
        # noinspection PyUnresolvedReferences
        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        return list_
    @classmethod
    def get_all_directory_paths__(cls, directory_path):
        if SystemMtd.get_is_linux():
            return cls._get_all_directory_paths(directory_path)
        else:
            return cls.get_all_directory_paths(directory_path)
    @classmethod
    def get_file_relative_path(cls, directory_path, file_path):
        return os.path.relpath(file_path, directory_path)
    @classmethod
    def set_copy_to(cls, src_directory_path, tgt_directory_path):
        def copy_fnc_(src_file_path_, tgt_file_path_):
            shutil.copy2(src_file_path_, tgt_file_path_)
        #
        src_directory_path = src_directory_path
        file_paths = cls.get_all_file_paths__(src_directory_path)
        #
        threads = []
        for i_src_file_path in file_paths:
            i_local_file_path = i_src_file_path[len(src_directory_path):]
            #
            i_tgt_file_path = tgt_directory_path + i_local_file_path
            if os.path.exists(i_tgt_file_path) is False:
                i_tgt_dir_path = os.path.dirname(i_tgt_file_path)
                if os.path.exists(i_tgt_dir_path) is False:
                    os.makedirs(i_tgt_dir_path)
                #
                i_thread = PyThread(
                    copy_fnc_, i_src_file_path, i_tgt_file_path
                )
                threads.append(i_thread)
                i_thread.start()
                # i_thread.join()
        #
        [i.join() for i in threads]
    @classmethod
    def get_file_paths_by_pattern__(cls, directory_path, name_pattern):
        path_pattern = '{}/{}'.format(directory_path, name_pattern)
        return fnmatch.filter(
            cls.get_file_paths__(directory_path), path_pattern
        )
    @classmethod
    def get_file_paths_by_glob_pattern__(cls, glob_pattern):
        return fnmatch.filter(
            cls.get_file_paths__(os.path.dirname(glob_pattern)), glob_pattern
        )


class StgFileMultiplyMtd(object):
    """
    methods using for multiply file
    etc. "/tmp/image.1001.exr" convert to "/tmp/image.####.exr"
    """
    @classmethod
    def get_match_args(cls, file_name, name_pattern):
        new_file_name = file_name
        args = _bsc_cor_pattern.PtnMultiplyFileMtd.get_args(
            name_pattern
        )
        re_pattern = _bsc_cor_pattern.PtnMultiplyFileMtd.to_re_style(name_pattern)
        numbers = re.findall(re_pattern, file_name)
        if numbers:
            if len(args) > 1:
                numbers = numbers[0]
            #
            for i, (i_key, i_count) in enumerate(args):
                new_file_name = new_file_name.replace(
                    numbers[i], i_key, 1
                )
            return new_file_name, map(int, numbers)
    @classmethod
    def set_merge_to(cls, file_paths, name_patterns):
        list_ = []
        for i_file_path in file_paths:
            i_file_path = cls.set_convert_to(i_file_path, name_patterns)
            if i_file_path not in list_:
                list_.append(i_file_path)
        return list_
    @classmethod
    def set_convert_to(cls, file_path, name_patterns):
        """
        use for convert "/tmp/image.1001.exr" to "/tmp/image.####.exr"
        :param file_path:
        :param name_patterns: list[str, ...]
        etc. *.####.{ext}, ext like "exr", "jpg"
        :return:
        """
        file_opt = StgFileOpt(file_path)
        for i_name_pattern in name_patterns:
            i_name_pattern = i_name_pattern.format(
                **dict(ext=file_opt.ext[1:])
            )
            if _bsc_cor_pattern.PtnMultiplyFileMtd.get_is_valid(i_name_pattern):
                match_args = StgFileMultiplyMtd.get_match_args(
                    file_opt.name, i_name_pattern
                )
                if match_args:
                    file_name_, numbers = match_args
                    #
                    file_path_ = '{}/{}'.format(file_opt.directory_path, file_name_)
                    return file_path_
        return file_path
    @classmethod
    def get_exists_tiles(cls, file_path):
        P = '[0-9]'
        re_keys = _bsc_cor_pattern.PtnMultiplyFileMtd.RE_MULTIPLY_KEYS
        pathsep = _bsc_cor_pattern.PtnMultiplyFileMtd.PATHSEP
        #
        directory_path = os.path.dirname(file_path)
        #
        name_base = os.path.basename(file_path)
        name_base_new = name_base
        for i_keyword, i_re_format, i_count in re_keys:
            i_results = re.finditer(i_re_format.format(i_keyword), name_base, re.IGNORECASE) or []
            for j_result in i_results:
                j_start, j_end = j_result.span()
                if i_count == -1:
                    s = P
                else:
                    s = P*i_count
                #
                name_base_new = name_base_new.replace(name_base[j_start:j_end], s, 1)
        #
        if name_base != name_base_new:
            glob_pattern = pathsep.join([directory_path, name_base_new])
            #
            list_ = StgDirectoryMtd.get_file_paths_by_glob_pattern__(glob_pattern)
            if list_:
                list_.sort()
        else:
            if os.path.isfile(file_path):
                list_ = [file_path]
            else:
                list_ = []
        return list_


class StgDirectoryMultiplyMtd(object):
    @classmethod
    def get_all_multiply_file_dict(cls, directory_path, name_pattern):
        dic = collections.OrderedDict()
        _ = StgDirectoryMtd.get_all_file_paths__(directory_path)
        for i_file_path in _:
            i_opt = StgFileOpt(i_file_path)
            i_match_args = StgFileMultiplyMtd.get_match_args(
                i_opt.name, name_pattern
            )
            if i_match_args:
                i_pattern, i_numbers = i_match_args
                if len(i_numbers) == 1:
                    i_relative_path_dir_path = StgDirectoryMtd.get_file_relative_path(
                        directory_path, i_opt.directory_path
                    )
                    i_key = '{}/{}'.format(
                        i_relative_path_dir_path, i_pattern
                    )
                    dic.setdefault(
                        i_key, []
                    ).append(i_numbers[0])
        return dic


class StgPathOpt(object):
    PATHSEP = '/'
    def __init__(self, path, cleanup=True):
        if cleanup is True:
            self._path = StorageMtd.set_pathsep_cleanup(path)
        else:
            self._path = path
        #
        if self.get_is_windows():
            self._root = self._path.split(self.PATHSEP)[0]
        elif self.get_is_linux():
            self._root = self.PATHSEP
        else:
            self._root = '/'

    def get_path(self):
        return self._path
    path = property(get_path)

    def get_root(self):
        return self._root
    root = property(get_root)
    @property
    def normcase_root(self):
        return os.path.normcase(self._root)
    @property
    def normcase_path(self):
        return os.path.normcase(self._path)

    def get_is_windows(self):
        return StorageMtd.get_path_is_windows(self.get_path())

    def get_is_linux(self):
        return StorageMtd.get_path_is_linux(self.get_path())

    def get_is_exists(self):
        return os.path.exists(self.get_path())

    def get_is_directory(self):
        return os.path.isdir(self.get_path())

    def get_is_file(self):
        return os.path.isfile(self.get_path())

    def set_open_in_system(self):
        if self.get_is_exists():
            if self.get_is_directory():
                StgExtraMtd.set_directory_open(self.get_path())
            elif self.get_is_file():
                StgExtraMtd.set_file_open(self.get_path())

    def get_modify_timestamp(self):
        return os.stat(self._path).st_mtime

    def get_user(self):
        return StorageMtd.get_user(self.get_path())

    def get_access_timestamp(self):
        return os.stat(self._path).st_atime

    def get_timestamp_is_same_to(self, file_path):
        if file_path is not None:
            if self.get_is_exists() is True and self.__class__(file_path).get_is_exists() is True:
                return str(self.get_modify_timestamp()) == str(self.__class__(file_path).get_modify_timestamp())
            return False
        return False

    def get_is_readable(self):
        return os.access(self._path, os.R_OK)

    def get_is_writeable(self):
        return os.access(self._path, os.W_OK)

    def set_map_to_platform(self):
        self._path = StorageMtd.set_map_to_platform(self._path)

    def __str__(self):
        return self._path


class StgFileSearchOpt(object):
    def __init__(self, ignore_name_case=False, ignore_ext_case=False, ignore_ext=False):
        self._ignore_name_case = ignore_name_case
        self._ignore_ext_case = ignore_ext_case
        self._ignore_ext = ignore_ext
        self._search_dict = collections.OrderedDict()

    def set_search_directories(self, directory_paths):
        self._search_dict = collections.OrderedDict()
        for i in directory_paths:
            for j in StgDirectoryMtd.get_all_file_paths__(i):
                j_directory_path, j_name_base, j_ext = StorageMtd.get_file_args(j)
                if self._ignore_name_case is True:
                    j_name_base = j_name_base.lower()
                if self._ignore_ext_case is True:
                    j_ext = j_ext.lower()

                self._search_dict[u'{}/{}{}'.format(j_directory_path, j_name_base, j_ext)] = j
        #
        self._set_key_sort_()

    def set_search_directory_append(self, directory_path, below_enable=False):
        if below_enable is True:
            _ = StgDirectoryMtd.get_all_file_paths__(directory_path)
        else:
            _ = StgDirectoryMtd.get_file_paths__(directory_path)

        for i in _:
            i_directory_path, i_name_base, i_ext = StorageMtd.get_file_args(i)
            if self._ignore_name_case is True:
                i_name_base = i_name_base.lower()
            if self._ignore_ext_case is True:
                i_ext = i_ext.lower()
            self._search_dict[u'{}/{}{}'.format(i_directory_path, i_name_base, i_ext)] = i
        # sort
        self._set_key_sort_()

    def _set_key_sort_(self):
        self._search_dict = _bsc_cor_dict.DictMtd.set_string_key_sort_to(self._search_dict)

    def get_result(self, file_path_src):
        name_src = os.path.basename(file_path_src)
        name_base_src, ext_src = os.path.splitext(name_src)
        name_base_pattern = _bsc_cor_pattern.PtnMultiplyFileMtd.to_fnmatch_style(name_base_src)

        if self._ignore_name_case is True:
            name_base_pattern = name_base_pattern.lower()

        if self._ignore_ext_case is True:
            ext_src = ext_src.lower()

        file_path_keys = self._search_dict.keys()

        match_pattern_0 = u'*/{}{}'.format(name_base_pattern, ext_src)
        matches_0 = fnmatch.filter(
            file_path_keys, match_pattern_0
        )
        if matches_0:
            file_path_tgt = self._search_dict[matches_0[-1]]
            directory_path_tgt, name_base_tgt, ext_tgt = StorageMtd.get_file_args(file_path_tgt)
            return u'{}/{}{}'.format(directory_path_tgt, name_base_src, ext_tgt)
        #
        if self._ignore_ext is True:
            match_pattern_1 = u'*/{}.*'.format(name_base_pattern)
            matches_1 = fnmatch.filter(
                file_path_keys, match_pattern_1
            )
            if matches_1:
                file_path_tgt = self._search_dict[matches_1[-1]]
                directory_path_tgt, name_base_tgt, ext_tgt = StorageMtd.get_file_args(file_path_tgt)
                return u'{}/{}{}'.format(directory_path_tgt, name_base_src, ext_tgt)


class StgDirectoryOpt(StgPathOpt):
    def __init__(self, path):
        super(StgDirectoryOpt, self).__init__(path)

    def set_create(self):
        StorageMtd.set_directory_create(
            self.path
        )

    def get_all_file_paths(self, include_exts=None):
        return StgDirectoryMtd.get_all_file_paths__(
            self.path, include_exts
        )

    def get_all_directory_paths(self):
        return StgDirectoryMtd.get_all_directory_paths__(
            self._path
        )

    def set_copy_to_directory(self, directory_path_tgt, replace=False):
        directory_path_src = self.path
        file_paths_src = self.get_all_file_paths()
        #
        for index, i_file_path_src in enumerate(file_paths_src):
            i_relative_file_path = i_file_path_src[len(directory_path_src):]
            i_file_path_tgt = directory_path_tgt + i_relative_file_path
            #
            i_file_opt_src = StgFileOpt(i_file_path_src)
            i_file_opt_tgt = StgFileOpt(i_file_path_tgt)
            if i_file_opt_tgt.get_is_exists() is False:
                # create target directory first
                i_file_opt_tgt.set_directory_create()
                #
                _bsc_cor_thread.TrdMethod.set_wait()
                _bsc_cor_thread.TrdMethod.set_start(
                    i_file_opt_src.set_copy_to_file, index,
                    i_file_path_tgt, replace=replace
                )


class StgDirectoryOpt_(object):
    def __init__(self, directory_path):
        self._path = directory_path

    def get_path(self):
        return self._path
    path = property(get_path)

    def set_open(self):
        if os.path.exists(self.path):
            if SystemMtd.get_is_windows():
                os.startfile(
                    self.path.replace(u'/', os.sep)
                )
            elif SystemMtd.get_is_linux():
                subprocess.Popen(
                    u'nautilus "{}" --select'.format(self.path),
                    shell=True
                )

    def get_is_exists(self):
        return os.path.exists(self.path)

    def get_all_file_path(self, include_exts=None):
        return StgDirectoryMtd.get_all_file_paths__(
            self.path, include_exts
        )

    def set_create(self):
        StorageMtd.set_directory_create(
            self._path
        )


class StgFileMtd(object):
    @classmethod
    def get_directory(cls, file_path):
        return os.path.dirname(file_path)


class StgFileOpt(StgPathOpt):
    def __init__(self, file_path, file_type=None):
        super(StgFileOpt, self).__init__(file_path)
        self._file_type = file_type

    def get_directory_path(self):
        return os.path.dirname(self.path)
    directory_path = property(get_directory_path)

    def get_type(self):
        return self.ext
    type = property(get_type)

    def get_path_base(self):
        return os.path.splitext(self.path)[0]
    @property
    def path_base(self):
        return os.path.splitext(self.path)[0]

    def get_name(self):
        return os.path.basename(self.path)
    name = property(get_name)
    @property
    def name_base(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    def get_ext(self):
        if self._file_type is not None:
            return self._file_type
        return os.path.splitext(self.path)[-1]
    ext = property(get_ext)

    def get_is_match_name_pattern(self, name_pattern):
        _ = fnmatch.filter([self.name], name_pattern)
        if _:
            return True
        return False

    def set_read(self):
        if os.path.exists(self.path):
            if self.get_ext() in ['.json']:
                with open(self.path) as j:
                    raw = json.load(j, object_pairs_hook=collections.OrderedDict)
                    j.close()
                    return raw
            elif self.get_ext() in ['.yml']:
                with open(self.path) as y:
                    raw = _bsc_cor_dict.OrderedYamlMtd.set_load(y)
                    y.close()
                    return raw
            else:
                with open(self.path) as f:
                    raw = f.read()
                    f.close()
                    return raw

    def set_write(self, raw):
        directory = os.path.dirname(self.path)
        if os.path.isdir(directory) is False:
            # noinspection PyBroadException
            try:
                os.makedirs(directory)
            except:
                pass
        if self.ext in ['.json']:
            with open(self.path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif self.ext in ['.yml']:
            with open(self.path, 'w') as y:
                _bsc_cor_dict.OrderedYamlMtd.set_dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                )
        else:
            with open(self.path, 'w') as f:
                f.write(raw)

    def set_append(self, raw):
        with open(self.path, 'w') as f:
            f.write(raw)

    def set_directory_create(self):
        StorageMtd.set_directory_create(
            self.get_directory_path()
        )

    def set_directory_repath_to(self, directory_path_tgt):
        return self.__class__(
            u'{}/{}'.format(
                directory_path_tgt, self.get_name()
            )
        )

    def set_directory_repath_to_join_uuid(self, directory_path_tgt):
        directory_path_src = self.get_directory_path()
        uuid_key = UuidMtd.get_by_string(directory_path_src)
        return self.__class__(
            u'{}/{}/{}'.format(
                directory_path_tgt, uuid_key, self.get_name()
            )
        )

    def set_ext_repath_to(self, ext_tgt):
        return self.__class__(
            u'{}{}'.format(
                self.get_path_base(), ext_tgt
            )
        )

    def set_copy_to_file(self, file_path_tgt, replace=False):
        if replace is True:
            if os.path.exists(file_path_tgt):
                os.remove(file_path_tgt)
        #
        file_path_src = self.path
        #
        if os.path.exists(file_path_tgt) is False:
            directory_path_tgt = os.path.dirname(file_path_tgt)
            if os.path.exists(directory_path_tgt) is False:
                os.makedirs(directory_path_tgt)
            # noinspection PyBroadException
            try:
                shutil.copy2(file_path_src, file_path_tgt)
            except:
                ExceptionMtd.set_print()

    def set_copy_to_directory(self, directory_path_tgt, replace=False):
        file_path_tgt = u'{}/{}'.format(
            directory_path_tgt, self.name
        )
        self.set_copy_to_file(
            file_path_tgt, replace=replace
        )


class StgGzipFileOpt(StgFileOpt):
    def __init__(self, *args, **kwargs):
        super(StgGzipFileOpt, self).__init__(*args, **kwargs)

    def set_read(self):
        if self.get_is_file() is True:
            with gzip.GzipFile(
                    mode='rb',
                    fileobj=open(self.path, 'rb')
            ) as g:
                if self.get_ext() in ['.yml']:
                    raw = _bsc_cor_dict.OrderedYamlMtd.set_load(g)
                    g.close()
                    return raw

    def set_write(self, raw):
        if os.path.isdir(self.directory_path) is False:
            os.makedirs(self.directory_path)
        # noinspection PyArgumentEqualDefault
        with gzip.GzipFile(
            filename=self.name + self.ext,
            mode='wb',
            compresslevel=9,
            fileobj=open(self.path, 'wb')
        ) as g:
            if self.get_ext() in ['.yml']:
                _bsc_cor_dict.OrderedYamlMtd.set_dump(
                    raw,
                    g,
                    indent=4,
                    default_flow_style=False,
                )


class StgZipFileOpt(StgFileOpt):
    def __init__(self, file_path):
        self._file_path = file_path

    def get_path(self):
        return self._file_path
    path = property(get_path)

    def get_element_names(self):
        file_path = self.get_path()
        if self.get_is_exists() is True:
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as z:
                    return z.namelist()
        # else:
        #     from unrar import rarfile
        #     if rarfile.is_rarfile(file_path):
        #         with rarfile.RarFile(file_path) as r:
        #             return r.namelist()
        return []

    def set_element_extract_to(self, element_name, element_file_path):
        if self.get_is_exists() is True:
            if zipfile.is_zipfile(self.path):
                with zipfile.ZipFile(self.path) as z:
                    directory_path = os.path.dirname(element_file_path)
                    f = z.extract(element_name, directory_path)
                    os.rename(f, element_file_path)
        # else:
        #     from unrar import rarfile
        #     if rarfile.is_rarfile(self.path):
        #         with rarfile.RarFile(self.path) as r:
        #             directory_path = os.path.dirname(element_file_path)
        #             f = r.extract(element_name, directory_path)
        #             os.rename(f, element_file_path)


# temp
class StgTmpBaseMtd(object):
    ROOT = '/l/temp'
    @classmethod
    def get_user_directory(cls, tag):
        return StorageMtd.set_map_to_platform(
            u'{root}/temporary/{tag}/{date_tag}-{user}'.format(
                **dict(
                    root=cls.ROOT,
                    date_tag=TimeMtd.get_date_tag(),
                    user=SystemMtd.get_user_name(),
                    tag=tag
                )
            )
        )
    @classmethod
    def get_save_region(cls, unique_id):
        number = abs(uuid.UUID(unique_id).int)
        return _bsc_cor_raw.RawIntegerOpt(number % 4096).set_encode_to_36()


class StgTmpThumbnailMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return UuidMtd.get_by_file(file_path)
    @classmethod
    def get_file_path(cls, file_path, ext='.jpg'):
        directory_path = _bsc_cor_environ.EnvironMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.thumbnail/{}/{}{}'.format(
            directory_path, region, key, ext
        )
    @classmethod
    def get_file_path_(cls, file_path, width=128, ext='.jpg'):
        directory_path = _bsc_cor_environ.EnvironMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.thumbnail/{}/{}/{}{}'.format(
            directory_path, region, key, width, ext
        )


class StgTmpYamlMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return UuidMtd.get_by_file(file_path)
    @classmethod
    def get_file_path(cls, file_path, tag):
        directory_path = _bsc_cor_environ.EnvironMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.yml/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.yml'
        )


class StgTmpTextMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return UuidMtd.get_by_file(file_path)
    @classmethod
    def get_file_path(cls, file_path, tag):
        directory_path = _bsc_cor_environ.EnvironMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.txt/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.txt'
        )
