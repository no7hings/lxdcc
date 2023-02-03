# coding:utf-8
import copy

from lxbasic import bsc_core

from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxresolver.methods as rsv_methods


class RsvAssetWorkspaceTextureOpt(object):
    def __init__(self, rsv_task):
        self._resolver = rsv_commands.get_resolver()

        self._rsv_task = rsv_task

        self._variant = None

        self._version = None

        self._work_texture_version_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-version-dir'
        )
        self._work_texture_src_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-src-dir'
        )
        self._work_texture_tx_directory_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-texture-tx-dir'
        )

    def get_directory_path_at(self, variant, version):
        return self._work_texture_version_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(variant=variant)
        )

    def get_src_directory_path_at(self, variant, version):
        return self._work_texture_src_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(variant=variant)
        )

    def get_tx_directory_path_at(self, variant, version):
        return self._work_texture_tx_directory_rsv_unit.get_result(
            version=version,
            extend_variants=dict(variant=variant)
        )

    def get_all_variants(self):
        pass

    def set_version_create_at(self, variant, version):
        if version == 'new':
            version = self.get_new_version_at(variant)
        #
        bsc_core.StorageBaseMtd.set_directory_create(
            self.get_directory_path_at(variant, version)
        )
        bsc_core.StorageBaseMtd.set_directory_create(
            self.get_src_directory_path_at(variant, version)
        )
        bsc_core.StorageBaseMtd.set_directory_create(
            self.get_tx_directory_path_at(variant, version)
        )
        #
        utl_core.Log.set_module_result_trace(
            'version create',
            'variant="{}", version="{}"'.format(
                variant, version
            )
        )

    def set_version_lock_at(self, variant, version):
        directory_path = self.get_directory_path_at(variant, version)
        #
        self.set_directory_locked(directory_path)
        #
        utl_core.Log.set_module_result_trace(
            'version lock',
            'variant="{}", version="{}"'.format(
                variant, version
            )
        )
    @classmethod
    def set_directory_locked(cls, directory_path):
        rsv_methods.PathPermissionOpt(
            directory_path
        ).set_just_read_only_for(
            ['cg_group', 'coop_grp']
        )

    def set_current_variant(self, variant):
        self._variant = variant

    def set_current_version(self, version):
        self._version = version

    def get_current_variant(self):
        return self._variant

    def get_current_version(self):
        return self._version

    def get_latest_version_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_latest_version(
            extend_variants=dict(variant=variant)
        )

    def get_new_version_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_new_version(
            extend_variants=dict(variant=variant)
        )

    def get_all_versions_at(self, variant):
        return self._work_texture_version_directory_rsv_unit.get_all_exists_versions(
            extend_variants=dict(variant=variant)
        )

    def get_all_locked_versions_at(self, variant):
        matches = self._work_texture_version_directory_rsv_unit.get_all_exists_matches(
            extend_variants=dict(variant=variant)
        )
        list_ = []
        for i in matches:
            i_result, i_variants = i
            if bsc_core.StorageBaseMtd.get_is_writeable(i_result) is False:
                list_.append(i_variants['version'])
        return list_

    def get_all_unlocked_versions_at(self, variant):
        matches = self._work_texture_version_directory_rsv_unit.get_all_exists_matches(
            extend_variants=dict(variant=variant)
        )
        list_ = []
        for i in matches:
            i_result, i_variants = i
            if bsc_core.StorageBaseMtd.get_is_writeable(i_result) is True:
                list_.append(i_variants['version'])
        return list_

    def get_all_directories(self, dcc_objs):
        rsv_project = self._rsv_task.get_rsv_project()

        directory_keyword = 'asset-work-texture-version-dir'

        file_keywords = [
            'asset-work-texture-src-dir',
            'asset-work-texture-tx-dir'
        ]

        directory_pattern = rsv_project.get_pattern(directory_keyword)

        check_pattern_opts = []
        for i_k in file_keywords:
            i_p = rsv_project.get_pattern(
                i_k
            )
            i_check_p = i_p + '/{extra}'
            i_check_p_opt = bsc_core.PtnParseOpt(
                i_check_p
            )
            i_check_p_opt.set_update(
                **dict(root=rsv_project.get('root'))
            )
            check_pattern_opts.append(i_check_p_opt)

        set_ = set()

        file_paths = set([i_v for i in dcc_objs for i_k, i_v in i.reference_raw.items()])
        for i_file_path in file_paths:
            for i_check_p_opt in check_pattern_opts:
                i_variants = i_check_p_opt.get_variants(i_file_path)
                if i_variants is not None:
                    i_directory_path = directory_pattern.format(**i_variants)
                    set_.add(i_directory_path)
                    break

        return list(set_)

    def set_all_directories_locked(self, dcc_objs):
        directory_paths = self.get_all_directories(
            dcc_objs
        )
        unlocked_directory_paths = [i for i in directory_paths if bsc_core.StorageBaseMtd.get_is_writeable(i) is True]
        if unlocked_directory_paths:
            with utl_core.log_progress_bar(maximum=len(unlocked_directory_paths), label='workspace texture lock') as g_p:
                for _i in unlocked_directory_paths:
                    self.set_directory_locked(_i)
                    g_p.set_update()

    def set_all_directories_locked_with_dialog(self, dcc_objs):
        pass

    def get_kwargs_by_directory_path(self, directory_path):
        for i_rsv_unit in [
            self._work_texture_src_directory_rsv_unit,
            self._work_texture_tx_directory_rsv_unit
        ]:
            i_properties = i_rsv_unit.get_properties_by_result(directory_path)
            if i_properties:
                return i_properties.get_value()

    def get_search_directory_args(self, directory_path):
        kwargs = self.get_kwargs_by_directory_path(directory_path)
        if kwargs:
            kwargs_0, kwargs_1 = copy.copy(kwargs), copy.copy(kwargs)
            kwargs_0['keyword'], kwargs_1['keyword'] = 'asset-work-texture-src-dir', 'asset-work-texture-tx-dir'
            return self._resolver.get_result(**kwargs_0), self._resolver.get_result(**kwargs_1)
