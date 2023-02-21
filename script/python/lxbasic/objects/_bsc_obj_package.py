# coding:utf-8
import fnmatch

from lxbasic import bsc_core


class PackageContextNew(object):
    BIN_SOURCE = '/job/PLE/support/wrappers/paper-bin'
    USER_ROOT_PATTERNS = dict(
        windows=['{home}/packages'],
        linux=['{home}/packages']
    )
    PRE_RELEASE_PATTERNS = dict(
        windows=['x:/PLE/workspace/pre_release/packages'],
        linux=['/job/PLE/workspace/pre_release/packages']
    )
    RELEASE_PATTERNS = dict(
        windows=['x:/PLE/bundle/internal', 'x:/PLE/bundle/thirdparty'],
        linux=['/job/PLE/bundle/internal', '/job/PLE/bundle/thirdparty']
    )
    FILE_PATTERNS = dict(
        windows=['{root}/{package_name}/{version}/paper_configure_bundle.py'],
        linux=['{root}/{package_name}/{version}/paper_configure_bundle.py']
    )
    def __init__(self, args):
        self._args = args

        self._platform = bsc_core.PlatformMtd.get_current()

        self._variants = dict(
            home=bsc_core.SystemMtd.get_home_directory(),
            platfrom=self._platform,
        )

        self._exclude_packages = []

    def get_user_package_roots(self):
        list_ = []
        for i_p in self.USER_ROOT_PATTERNS.get(self._platform) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_pre_release_package_roots(self):
        list_ = []
        for i_p in self.PRE_RELEASE_PATTERNS.get(self._platform) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_release_package_roots(self):
        list_ = []
        for i_p in self.RELEASE_PATTERNS.get(self._platform) or []:
            i_p_opt = bsc_core.PtnParseOpt(
                i_p
            )
            i_p_opt.set_update(**self._variants)
            i_results = i_p_opt.get_exists_results()
            if i_results:
                list_.append(i_results[0])
        return list_

    def get_resolved_packages_data(self):
        if self._args:
            results = bsc_core.SubProcessMtd.set_run_as_block('{} {} -v'.format(self.BIN_SOURCE, self._args))
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

    def _get_package_file_patterns(self):
        return self.FILE_PATTERNS.get(self._platform) or []
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

    def _get_replace_package(self, package, beta_enable=False):
        package_name, package_version = package.split('@')
        package_virtual_version = self._get_virtual_version(package_version)
        package_data = {}
        user_package_roots = self.get_user_package_roots()
        pre_release_package_roots = self.get_pre_release_package_roots()
        package_roots = user_package_roots
        if beta_enable is True:
            package_roots += pre_release_package_roots
        package_file_patterns = self._get_package_file_patterns()
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

    def _get_valid_package(self, package, beta_enable=False):
        if '@' not in package:
            package_name = package
            package_data = {}
            user_package_roots = self.get_user_package_roots()
            pre_release_package_roots = self.get_pre_release_package_roots()
            package_roots = user_package_roots
            if beta_enable is True:
                package_roots += pre_release_package_roots
            #
            release_package_roots = self.get_release_package_roots()
            package_roots += pre_release_package_roots
            package_file_patterns = self._get_package_file_patterns()
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
                                if i_package_root in release_package_roots:
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

    def _get_packages(self, packages_extend=None, beta_enable=False):
        list_ = []
        resolved_packages = self.get_resolved_packages_data()
        #
        for i_p in resolved_packages:
            i_replace_package = self._get_replace_package(i_p, beta_enable=beta_enable)
            if i_replace_package is not None:
                bsc_core.LogMtd.trace_method_result(
                    'package replaced',
                    'package="{}"'.format(i_replace_package)
                )
                list_.append(i_replace_package)
            else:
                list_.append(i_p)

        for i_p in packages_extend or []:
            i_package = self._get_valid_package(i_p, beta_enable=beta_enable)
            if i_package is not None:
                bsc_core.LogMtd.trace_method_result(
                    'package resolved',
                    'package="{}"'.format(i_package)
                )
                list_.append(i_package)
        return list_

    def get_args(self, packages_extend=None, beta_enable=False):
        return self._get_packages(packages_extend, beta_enable)

    def get_command(self, args_execute=None, packages_extend=None, beta_enable=False):
        if isinstance(args_execute, (set, tuple, list)):
            # replace first argument to "--join-cmd", etc. "-- maya", "-c maya" to "--join-cmd maya"
            args_execute = [
                '--join-cmd' if x_seq == 0 and y_seq == 0 and y in ['--', '-c'] else y
                for x_seq, x in enumerate(args_execute)
                for y_seq, y in enumerate(x.split(' '))
            ]
        #
        args = self.get_args(packages_extend, beta_enable)
        if args:
            if isinstance(args_execute, (set, tuple, list)):
                args.extend(args_execute)
            return ' '.join([self.BIN_SOURCE] + list(args))


if __name__ == '__main__':
    print PackageContextNew(
        None
    ).get_command(args_execute=['-- lxdcc'], packages_extend=['lxdcc'])


