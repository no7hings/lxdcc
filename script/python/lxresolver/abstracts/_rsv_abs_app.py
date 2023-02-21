# coding:utf-8
import copy

import fnmatch

import threading

import os

import subprocess

import functools

from lxbasic import bsc_core

from lxresolver import rsv_configure

import lxbasic.objects as bsc_objects


class AbsRsvAppDef(object):
    Applications = rsv_configure.Applications
    CACHE = dict()
    BIN = None
    def __init__(self, rsv_project, application, configure):
        self._rsv_project = rsv_project
        #
        self._project = rsv_project.get_name()
        self._platform = bsc_core.SystemMtd.get_platform()
        #
        if application == 'python':
            self._application = 'maya'
        elif application == 'shotgun':
            self._application = 'maya'
        elif application == 'usd':
            self._application = 'maya'
        elif application == 'gui':
            self._application = 'maya'
        elif application == 'rv':
            self._application = 'maya'
        elif application == 'rv-movie-convert':
            self._application = 'maya'
        else:
            self._application = application
        #
        self._configure = configure
        #
        self._variants = dict(
            home=bsc_core.SystemMtd.get_home_directory(),
            project=self._project,
            platfrom=self._platform,
            application=self._application
        )

    def get_key(self):
        return '{}.{}'.format(
            self._project,
            self._application
        )

    def get_project(self):
        return self._project
    project = property(get_project)

    def get_application(self):
        return self._application
    application = property(get_application)

    def get_configure(self):
        return self._configure
    configure = property(get_configure)

    def _get_package_roots(self):
        list_ = []
        platform = bsc_core.SystemMtd.get_platform()
        variants = dict(
            home=bsc_core.SystemMtd.get_home_directory(),
            project=self._project,
            application=self._application
        )
        for i_p in self._configure.get('package-root-patterns.{}'.format(platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_package_user_roots(self):
        list_ = []
        for i_p in self._configure.get('package-user-root-patterns.{}'.format(self._platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_package_pre_release_roots(self):
        list_ = []
        for i_p in self._configure.get('package-pre_release-root-patterns.{}'.format(self._platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_package_release_roots(self):
        list_ = []
        for i_p in self._configure.get('package-release-root-patterns.{}'.format(self._platform)) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def _get_package_file_patterns(self):
        return self._configure.get('package-file-patterns') or []

    def _get_configure_root_patterns(self):
        platform = bsc_core.SystemMtd.get_platform()
        return self._configure.get('configure-root-patterns.{}'.format(platform)) or []

    def _get_configure_file_patterns(self):
        return self._configure.get('configure-file-patterns') or []

    def _get_configure_directory(self):
        for i_p in self._get_configure_root_patterns():
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                i_results = bsc_core.RawTextsMtd.set_sort_to(i_results)
                return i_results[-1]

    def _get_configure_file(self):
        d = self._get_configure_directory()
        variants = dict(
            root=d,
            project=self._project,
            application=self._application
        )
        for i_p in self._get_configure_file_patterns():
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                i_results = bsc_core.RawTextsMtd.set_sort_to(i_results)
                return i_results[-1]

    def get_package(self, package_name):
        pass

    def get_args(self, packages_extend=None):
        raise NotImplementedError()

    def get_packages(self):
        pass

    def get_command(self, args_execute=None, packages_extend=None):
        raise NotImplementedError()

    def execute_command(self, args_execute=None, packages_extend=None):
        cmd = self.get_command(args_execute, packages_extend)
        if cmd:
            bsc_core.LogMtd.trace_method_result(
                'execute app command',
                'command=`{}` is started'.format(cmd)
            )
            bsc_core.SubProcessMtd.set_run_with_result(cmd)
    @classmethod
    def execute_with_result(cls, command, **sub_progress_kwargs):
        bsc_core.LogMtd.trace_method_result(
            'execute app command',
            'command=`{}` is started'.format(command)
        )
        bsc_core.SubProcessMtd.set_run_with_result(command, **sub_progress_kwargs)
    @classmethod
    def execute_with_result_use_thread(cls, command, **sub_progress_kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=command,
                **sub_progress_kwargs
            )
        )
        t_0.start()
        # t_0.join()

    def _test_(self):
        print self.get_package('pglauncher')

    def __str__(self):
        return str(self._configure)


class PackageContextDefault(object):
    pass


class AbsRsvAppDefault(AbsRsvAppDef):
    BIN = 'rez-env'
    def __init__(self, *args, **kwargs):
        super(AbsRsvAppDefault, self).__init__(*args, **kwargs)
    
    def get_args(self, packages_extend=None):
        if self._application == self.Applications.Lynxi:
            return ['lxdcc']

        key = self.get_key()
        if key in self.__class__.CACHE:
            return self.__class__.CACHE[key]
        #
        list_ = []
        configure_file_path = self._get_configure_file()
        if configure_file_path:
            bsc_core.LogMtd.trace_method_result(
                'app resolved',
                'app="{project}.{application}"'.format(
                    **dict(project=self._project, application=self._application)
                )
            )
            configure = bsc_objects.Configure(value=configure_file_path)
            keys = configure.get_leaf_keys()
            for i_key in keys:
                i_args = configure.get(i_key)
                list_.extend(i_args)
        if list_:
            self.__class__.CACHE[key] = list_
            #
            _ = copy.copy(list_)
            if isinstance(packages_extend, (set, tuple, list)):
                _.extend(list(packages_extend))
            return _
        return []

    def get_command(self, args_execute=None, packages_extend=None):
        args = self.get_args(packages_extend)
        if args:
            if isinstance(args_execute, (set, tuple, list)):
                args.extend(args_execute)
            return ' '.join([self.BIN] + list(args))

    def _test_(self):
        pass


class PackageContextNew(object):
    CACHE = dict()
    def __init__(self, app, cmd, packages_extend):
        self._app = app
        self._cmd = cmd

        self._packages_extend = packages_extend

        self._exclude_packages = []

    def get_resolved_packages_data(self):
        results = bsc_core.SubProcessMtd.set_run_as_block('{} {} -v'.format(self._app.BIN_SOURCE, self._cmd))
        package_start_index = None
        package_end_index = None
        index_maximum = len(results)-1
        index = 0
        while True:
            index += 1
            result = results[index]
            if result == 'It simplifies to:':
                package_start_index = index+1
            elif result == 'Which resolves to:':
                package_end_index = index-1
            if index >= index_maximum:
                break
        #
        if package_start_index is not None and package_end_index is not None:
            args = map(lambda x: x.strip(), results[package_start_index:package_end_index])
            return args
        return []

    def _get_user_package_args(self, package_name):
        package_file_patterns = self._app._get_package_file_patterns()
        user_root = self._app._get_package_roots()[0]
        if bsc_core.StorageMtd.get_is_exists(user_root):
            for i_p in package_file_patterns:
                i_variants = dict(
                    root=user_root,
                    package_name=package_name
                )
                i_p_opt = bsc_core.PtnParseOpt(i_p)
                i_p_opt.set_update(**i_variants)
                i_results = i_p_opt.get_exists_results()
                if i_results:
                    i_results = bsc_core.RawTextsMtd.set_sort_to(i_results)
                    i_package_file_path = i_results[-1]
                    i_package_directory_path = bsc_core.StgFileMtd.get_directory(i_package_file_path)
                    i_package_variants = i_p_opt.get_variants(i_package_file_path)
                    i_package = '{}@{}'.format(package_name, i_package_directory_path)
                    return i_package, i_package_variants
    @classmethod
    def _get_virtual_version(cls, version):
        """
        etc. convert master-1 to 0.0.1
        :param version:
        :return:
        """
        if fnmatch.filter([version], 'master-[0-9]*'):
            _ = version.split('-')
            return '0.{}'.format(float(_[-1]))
        return version

    def _get_replace_package(self, package):
        package_name, package_version = package.split('@')
        package_virtual_version = self._get_virtual_version(package_version)
        package_data = {}
        package_user_roots = self._app.get_package_user_roots()
        package_pre_release_roots = self._app.get_package_pre_release_roots()
        package_roots = package_user_roots + package_pre_release_roots
        package_file_patterns = self._app._get_package_file_patterns()
        #
        for i_index, i_package_root in enumerate(package_roots):
            if bsc_core.StorageMtd.get_is_exists(i_package_root):
                i_variants = dict(
                    root=i_package_root,
                    package_name=package_name
                )
                for j_p in package_file_patterns:
                    j_p_opt = bsc_core.PtnParseOpt(j_p)
                    j_p_opt.set_update(**i_variants)
                    j_results = j_p_opt.get_exists_results()
                    if j_results:
                        for k_package_file in j_results:
                            k_package_directory = bsc_core.StgFileMtd.get_directory(k_package_file)
                            k_package_variants = j_p_opt.get_variants(k_package_file)
                            k_package_version = k_package_variants['version']
                            k_package_virtual_version = self._get_virtual_version(k_package_version)
                            k_key = '{}.{}'.format(k_package_virtual_version, i_index)
                            k_package = '{}@{}'.format(package_name, k_package_directory)
                            package_data[k_key] = k_package
        #
        if package_data:
            package_data[package_virtual_version] = package
            keys = package_data.keys()
            keys = bsc_core.RawTextsMtd.set_sort_to(keys)
            package_latest = package_data[keys[-1]]
            return package_latest

    def _get_package(self, package):
        if '@' not in package:
            package_name = package
            package_data = {}
            package_user_roots = self._app.get_package_user_roots()
            package_pre_release_roots = self._app.get_package_pre_release_roots()
            package_release_roots = self._app.get_package_release_roots()
            package_roots = package_user_roots + package_pre_release_roots + package_release_roots
            package_file_patterns = self._app._get_package_file_patterns()
            #
            for i_index, i_package_root in enumerate(package_roots):
                if bsc_core.StorageMtd.get_is_exists(i_package_root):
                    i_variants = dict(
                        root=i_package_root,
                        package_name=package_name
                    )
                    for j_p in package_file_patterns:
                        j_p_opt = bsc_core.PtnParseOpt(j_p)
                        j_p_opt.set_update(**i_variants)
                        j_results = j_p_opt.get_exists_results()
                        if j_results:
                            for k_package_file in j_results:
                                k_package_directory = bsc_core.StgFileMtd.get_directory(k_package_file)
                                k_package_variants = j_p_opt.get_variants(k_package_file)
                                k_package_version = k_package_variants['version']
                                k_package_virtual_version = self._get_virtual_version(k_package_version)
                                k_key = '{}.{}'.format(k_package_virtual_version, i_index)
                                if i_package_root in package_release_roots:
                                    k_package = '{}@{}'.format(package_name, k_package_version)
                                else:
                                    k_package = '{}@{}'.format(package_name, k_package_directory)
                                package_data[k_key] = k_package
            #
            if package_data:
                keys = package_data.keys()
                keys = bsc_core.RawTextsMtd.set_sort_to(keys)
                package_latest = package_data[keys[-1]]
                return package_latest
        return package

    def _get_packages(self):
        list_ = []
        resolved_packages = self.get_resolved_packages_data()
        #
        for i_p in resolved_packages:
            i_replace_package = self._get_replace_package(i_p)
            if i_replace_package is not None:
                bsc_core.LogMtd.trace_method_result(
                    'package replaced',
                    'package="{}"'.format(i_replace_package)
                )
                list_.append(i_replace_package)
            else:
                list_.append(i_p)

        if isinstance(self._packages_extend, (set, tuple, list)):
            for i_p in self._packages_extend:
                i_package = self._get_package(i_p)
                if i_package is not None:
                    bsc_core.LogMtd.trace_method_result(
                        'package resolved',
                        'package="{}"'.format(i_package)
                    )
                    list_.append(i_package)
        return list_

    def get_args(self):
        return self._get_packages()


class AbsRsvAppNew(AbsRsvAppDef):
    BIN_SOURCE = '/job/PLE/support/wrappers/paper-bin'
    BIN = '/job/PLE/support/wrappers/paper-bin'
    def __init__(self, *args, **kwargs):
        super(AbsRsvAppNew, self).__init__(*args, **kwargs)

    def get_args(self, packages_extend=None):
        if self._application == self.Applications.Lynxi:
            return ['lxdcc', 'lxdcc_lib', 'lxdcc_gui', 'lxdcc_rsc']
        #
        key = self.get_key()
        if key in self.__class__.CACHE:
            return self.__class__.CACHE[key]
        #
        list_ = []
        configure_file_path = self._get_configure_file()
        if configure_file_path:
            bsc_core.LogMtd.trace_method_result(
                'app resolved',
                'app="{project}.{application}"'.format(
                    **dict(project=self._project, application=self._application)
                )
            )
            configure = bsc_objects.Configure(value=configure_file_path)
            s = configure.get('{}.pipeline'.format(self._application))
            p_c = PackageContextNew(
                self, s, packages_extend
            )
            args = p_c.get_args()
            list_.extend(args)
        if list_:
            self.__class__.CACHE[key] = list_
            #
            _ = copy.copy(list_)
            return _
        return []

    def get_command(self, args_execute=None, packages_extend=None):
        if isinstance(args_execute, (set, tuple, list)):
            args_execute = [
                '--join-cmd' if x_seq == 0 and y_seq == 0 and y in ['--', '-c'] else y
                for x_seq, x in enumerate(args_execute)
                for y_seq, y in enumerate(x.split(' '))
            ]
        #
        args = self.get_args(packages_extend)
        if args:
            if isinstance(args_execute, (set, tuple, list)):
                args.extend(args_execute)
            return ' '.join([self.BIN] + list(args))

    def _test_(self):
        pass
