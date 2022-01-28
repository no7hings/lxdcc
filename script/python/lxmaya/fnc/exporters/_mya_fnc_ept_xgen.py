# coding:utf-8
import os

from lxbasic import bsc_core

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya import ma_configure

import lxutil.objects as utl_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_xgn_operators as mya_dcc_xgn_operators

from lxmaya.fnc.exporters import _mya_fnc_ept_geometry


class XgenExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        project_directory='',
        grow_mesh_directory='',
        xgen_collection_directory='',
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
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_collection_paths = group.get_all_shape_paths(include_obj_type=[ma_configure.Util.XGEN_PALETTE])
        for i_xgen_collection_path in xgen_collection_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_collection_path
            )
            i_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_operators.Palette(i_name)
            i_file_name = i_xgen_palette_opt.get_file_name()
            #
            i_grow_meshes = i_xgen_palette_opt.get_grow_meshes()
            if i_grow_meshes:
                i_abc_file_path = '{}/{}.abc'.format(directory_path, os.path.splitext(i_file_name)[0])
                i_location = i_grow_meshes[0].transform.path
                _mya_fnc_ept_geometry.GeometryAbcExporter(
                    file_path=i_abc_file_path,
                    root=i_location,
                ).set_run()
    @classmethod
    def _set_xgen_collection_export_(cls, project_directory_path, xgen_collection_directory_path, location):
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_collection_paths = group.get_all_shape_paths(include_obj_type=[ma_configure.Util.XGEN_PALETTE])
        for i_xgen_collection_path in xgen_collection_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_collection_path
            )
            i_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_operators.Palette(i_name)
            i_xgen_directory_path_src = i_xgen_palette_opt.get_data_directory()
            # copy xgen-data
            i_xgen_directory_path_tgt = '{}/{}'.format(xgen_collection_directory_path, i_name)
            utl_dcc_objects.OsDirectory_(i_xgen_directory_path_src).set_copy_to_directory(
                i_xgen_directory_path_tgt
            )
            # repath directory in xgen-data
            i_file_path = i_xgen_palette_opt.get_file_path()
            i_dot_xgen_file = utl_objects.DotXgenFileReader(i_file_path)
            i_dot_xgen_file.set_project_path(project_directory_path)
            i_dot_xgen_file.set_xgen_collection_path(xgen_collection_directory_path)
            i_dot_xgen_file.set_save()

    def set_run(self):
        option = self.get_option()
        project_directory_path = option.get('project_directory')
        grow_mesh_directory_path = option.get('grow_mesh_directory')
        xgen_collection_directory_path = option.get('xgen_collection_directory')
        location = option.get('location')
        # #
        with_grow_mesh_abc = option.get('with_grow_mesh_abc')
        if with_grow_mesh_abc is True:
            self._set_grow_mesh_abc_export_(grow_mesh_directory_path, location)
        #
        with_xgen_collection = option.get('with_xgen_collection')
        if with_xgen_collection is True:
            self._set_xgen_collection_export_(project_directory_path, xgen_collection_directory_path, location)
