# coding:utf-8
import os

from lxbasic import bsc_core

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya import ma_configure

import lxutil.objects as utl_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil.fnc.exporters as utl_fcn_exporters

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_xgn_operators as mya_dcc_xgn_operators

from lxmaya.fnc.exporters import _mya_fnc_ept_geometry


class XgenExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        xgen_project_directory='',
        xgen_collection_directory='',
        #
        grow_mesh_directory='',
        #
        location='',
        #
        with_grow_mesh_abc=True,
        with_xgen_collection=True,
    )
    def __init__(self, option=None):
        super(XgenExporter, self).__init__(option)
    @classmethod
    def _set_grow_mesh_abc_export_(cls, directory_path, location):
        mya_location = bsc_core.DccPathDagOpt(location).translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_collection_obj_paths = group.get_all_shape_paths(include_obj_type=[ma_configure.Util.XGEN_PALETTE])
        for i_xgen_collection_obj_path in xgen_collection_obj_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_collection_obj_path
            )
            i_xgen_collection_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_operators.Palette(i_xgen_collection_name)
            i_xgen_collection_file_name = i_xgen_palette_opt.get_file_name()
            #
            i_grow_meshes = i_xgen_palette_opt.get_grow_meshes()
            if i_grow_meshes:
                i_abc_file_path = '{}/{}.abc'.format(directory_path, os.path.splitext(i_xgen_collection_file_name)[0])
                # i_location = i_grow_meshes[0].transform.path
                _mya_fnc_ept_geometry.GeometryAbcExporter(
                    file_path=i_abc_file_path,
                    root=[i.transform.path for i in i_grow_meshes],
                    attribute_prefix=['xgen'],
                    option={}
                ).set_run()
    @classmethod
    def _set_xgen_collection_export_(cls, xgen_project_directory_path, xgen_collection_directory_path, location):
        mya_location = bsc_core.DccPathDagOpt(location).translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_collection_obj_paths = group.get_all_shape_paths(include_obj_type=[ma_configure.Util.XGEN_PALETTE])
        for i_xgen_collection_obj_path in xgen_collection_obj_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_collection_obj_path
            )
            i_xgen_collection_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_operators.Palette(i_xgen_collection_name)
            i_xgen_collection_data_directory_path_src = i_xgen_palette_opt.get_data_directory()
            # copy xgen-data
            i_xgen_collection_directory_path_tgt = '{}/{}'.format(xgen_collection_directory_path, i_xgen_collection_name)
            utl_dcc_objects.OsDirectory_(i_xgen_collection_data_directory_path_src).set_copy_to_directory(
                i_xgen_collection_directory_path_tgt
            )
            i_xgen_collection_file_path = i_xgen_palette_opt.get_file_path()
            utl_fcn_exporters.DotXgenExporter(
                option=dict(
                    xgen_collection_file=i_xgen_collection_file_path,
                    xgen_project_directory=xgen_project_directory_path,
                    xgen_collection_directory=xgen_collection_directory_path,
                    xgen_collection_name=i_xgen_collection_name,
                )
            ).set_run()

    def set_run(self):
        option_opt = self.get_option()
        xgen_project_directory_path = option_opt.get('xgen_project_directory')
        xgen_collection_directory_path = option_opt.get('xgen_collection_directory')
        #
        grow_mesh_directory_path = option_opt.get('grow_mesh_directory')
        location = option_opt.get('location')
        # #
        with_grow_mesh_abc = option_opt.get('with_grow_mesh_abc')
        if with_grow_mesh_abc is True:
            self._set_grow_mesh_abc_export_(grow_mesh_directory_path, location)
        #
        with_xgen_collection = option_opt.get('with_xgen_collection')
        if with_xgen_collection is True:
            self._set_xgen_collection_export_(
                xgen_project_directory_path,
                xgen_collection_directory_path,
                #
                location
            )


class XgenUsdExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        location='',
        xgen_collection_files=[]
    )
    def __init__(self, option=None):
        super(XgenUsdExporter, self).__init__(option)

    def set_run(self):
        option_opt = self.get_option()
        location = option_opt.get('location')
        location_dag_opt = bsc_core.DccPathDagOpt(location)
        mya_location_obj_path = location_dag_opt.translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        mya_location = mya_location_obj_path.path
        #
        group = mya_dcc_objects.Group(mya_location)
        if group.get_is_exists() is True:
            mya_objs = group.get_descendants()
            print mya_objs
