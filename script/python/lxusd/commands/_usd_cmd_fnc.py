# coding:utf-8
import collections

from lxutil.dcc import dcc_objects

import lxutil.objects as utl_objects

from lxusd import usd_configure

from lxresolver import rsv_configure

import lxresolver.commands as rsv_commands

import copy


def set_asset_work_set_usda_create(task_properties):
    resolver = rsv_commands.get_resolver()
    #
    branch = task_properties.get('branch')
    step = task_properties.get('step')
    set_usda_file_paths = []
    if branch == 'asset':
        if step in ['mod', 'srf']:
            asset = task_properties.get('asset')
            version = task_properties.get('version')
            #
            configure = utl_objects.Configure(value=usd_configure.Data.SET_USDA_ARGUMENT_CONFIGURE_PATH)
            set_usd_configure = utl_objects.Configure(value=rsv_configure.Data.GEOMETRY_USD_CONFIGURE_PATH)
            #
            configure.set('properties.asset', asset)
            #
            rsv_task = resolver.get_rsv_task(**task_properties.value)
            #
            for element_label in set_usd_configure.get_branch_keys('elements'):
                v = set_usd_configure.get('elements.{}'.format(element_label))
                _layer = v['layer']
                _keyword = v['keyword']
                #
                _kwargs = copy.copy(task_properties.value)
                _kwargs['workspace'] = v['workspace']
                _kwargs['step'] = v['step']
                _kwargs['task'] = v['task']
                #
                _rsv_task = resolver.get_rsv_task(**_kwargs)
                if _rsv_task is not None:
                    geometries = configure.get(
                        'usd.layers.{}'.format(_layer), default_value=collections.OrderedDict()
                    )
                    #
                    geometry_usd_file = _rsv_task.get_rsv_unit(
                        keyword=_keyword, workspace='publish'
                    )
                    if geometry_usd_file:
                        geometry_usd_file_path = geometry_usd_file.get_result(version='latest')
                        if geometry_usd_file_path:
                            geometries['geometry__{}'.format(element_label)] = geometry_usd_file_path
                    #
                    configure.set(
                        'usd.layers.{}'.format(_layer), geometries
                    )
            # geometry-surface
            surface_geometries = collections.OrderedDict()
            var_names = ['hi', 'temp']
            for var_name in var_names:
                work_geometry_usd_var_file = rsv_task.get_rsv_unit(
                    keyword='asset-work-geometry-usd-{}-file'.format(var_name), workspace='work'
                )
                if work_geometry_usd_var_file:
                    work_geometry_usd_var_file_path = work_geometry_usd_var_file.get_result(version='latest')
                    if work_geometry_usd_var_file_path:
                        surface_geometries['geometry__surface__{}'.format(var_name)] = work_geometry_usd_var_file_path
            #
            configure.set(
                'usd.layers.surface', surface_geometries
            )
            #
            for i in ['all', 'model', 'hair', 'effect', 'surface']:
                j2_template = usd_configure.JinJa2.ENVIRONMENT.get_template('{}-usda-template.j2'.format(i))
                raw = j2_template.render(**configure.value)
                #
                set_usd_file = rsv_task.get_rsv_unit(
                    keyword='asset-work-set-usd-{}-file'.format(i)
                )
                set_usd_file_path = set_usd_file.get_result(version=version)
                #
                dcc_objects.OsFile(set_usd_file_path).set_write(raw)
                set_usda_file_paths.append(set_usd_file_path)
    #
    return set_usda_file_paths
