# coding:utf-8
import collections

from lxbasic import bsc_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxusd.fnc.exporters as usd_fnc_exporters

from lxutil.fnc import utl_fnc_obj_abs

import lxresolver.commands as rsv_commands

from lxusd import usd_core


class RsvAssetSetUsdCreator(object):
    def __init__(self, rsv_asset):
        self._rsv_asset = rsv_asset
    @classmethod
    def _get_shot_asset_dict_(cls, rsv_asset, shot_set_usd_file_path):
        #
        dic = collections.OrderedDict()
        #
        paths = usd_core.UsdStageOpt(
            shot_set_usd_file_path
        ).set_obj_paths_find(
            '/assets/*/{}*'.format(
                rsv_asset.get('asset')
            )
        )
        if paths:
            paths = bsc_core.TextsOpt(paths).set_sort_to()
        #
        for i_location in paths:
            i_shot_asset = i_location.split('/')[-1]
            dic[i_shot_asset] = i_location
        return dic
    @classmethod
    def _get_rsv_asset_shots_(cls, rsv_asset):
        lis = []
        #
        resolver = rsv_commands.get_resolver()
        #
        rsv_shots = resolver.get_rsv_entities(
            project=rsv_asset.get('project'), branch='shot'
        )
        for i_rsv_shot in rsv_shots:
            i_rsv_shot_set_task = i_rsv_shot.get_rsv_task(
                workspace='publish', step='set', task='registry'
            )
            if i_rsv_shot_set_task is not None:
                i_rsv_shot_set_usd_file = i_rsv_shot_set_task.get_rsv_unit(
                    keyword='shot-set-usd-file'
                )
                i_shot_set_usd_file_path = i_rsv_shot_set_usd_file.get_result(
                    version='latest'
                )
                if i_shot_set_usd_file_path is not None:
                    shot_assets_dict = cls._get_shot_asset_dict_(
                        rsv_asset, i_shot_set_usd_file_path
                    )
                    if shot_assets_dict:
                        lis.append(i_rsv_shot)
        return lis
    @classmethod
    def get_shot_frame_range(cls, rsv_shot):
        rsv_shot_set_task = rsv_shot.get_rsv_task(
            workspace='publish', step='set', task='registry'
        )
        if rsv_shot_set_task is not None:
            rsv_shot_set_usd_file = rsv_shot_set_task.get_rsv_unit(
                keyword='shot-set-usd-file'
            )
            shot_set_usd_file_path = rsv_shot_set_usd_file.get_result(
                version='latest'
            )
            if shot_set_usd_file_path is not None:
                return usd_core.UsdStageOpt(
                    shot_set_usd_file_path
                ).get_frame_range()

    def get_rsv_asset_shots(self):
        return self._get_rsv_asset_shots_(
            self._rsv_asset
        )

    def set_run(self):
        pass


class RsvTaskOverrideUsdCreator(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        var_names=['hi'],
        root='/master'
    )
    VAR_NAMES = ['hi']
    def __init__(self, rsv_task, option=None):
        super(RsvTaskOverrideUsdCreator, self).__init__(option)
        if rsv_task is None:
            raise TypeError()
        #
        self._rsv_task = rsv_task

    def _set_geometry_uv_map_create_at_(self, var_name):
        root = self.get('root')
        work_asset_geometry_var_file_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-geometry-usd-var-file'
        )
        work_asset_geometry_uv_map_var_file_unit = self._rsv_task.get_rsv_unit(
            keyword='asset-work-geometry-uv_map-usd-var-file'
        )
        work_asset_geometry_hi_file_paths = work_asset_geometry_var_file_unit.get_result(
            version='all', extend_variants=dict(var=var_name)
        )
        for i_work_asset_geometry_var_file_path in work_asset_geometry_hi_file_paths:
            i_properties = work_asset_geometry_var_file_unit.get_properties(i_work_asset_geometry_var_file_path)
            i_version = i_properties.get('version')
            i_work_asset_geometry_uv_map_var_file_path = work_asset_geometry_uv_map_var_file_unit.get_result(
                version=i_version, extend_variants=dict(var=var_name)
            )
            if utl_dcc_objects.OsFile(i_work_asset_geometry_uv_map_var_file_path).get_is_exists() is False:
                usd_fnc_exporters.GeometryUvMapExporter(
                    file_path=i_work_asset_geometry_uv_map_var_file_path,
                    root=root,
                    option=dict(
                        file_0=i_work_asset_geometry_var_file_path,
                        file_1=i_work_asset_geometry_var_file_path
                    )
                ).set_run()

    def _set_geometry_uv_map_create_(self):
        for i_var_name in self.VAR_NAMES:
            self._set_geometry_uv_map_create_at_(i_var_name)

    def _set_geometry_display_color_create_at_(self):
        pass

    def set_run(self):
        pass
