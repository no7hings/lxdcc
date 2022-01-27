# coding:utf-8
import os

from lxbasic import bsc_core

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya import ma_configure

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_xgn_operators as mya_dcc_xgn_operators

from lxmaya.fnc.exporters import _mya_fnc_ept_geometry


class XgenExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        grow_mesh_directory='',
        xgen_directory='',
        location='',
        #
        with_grow_mesh_abc=True,
        with_xgen=True,
    )
    def __init__(self, option=None):
        super(XgenExporter, self).__init__(option)
    @classmethod
    def _set_grow_mesh_abc_export_(cls, directory_path, location):
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_palette_paths = group.get_all_shape_paths(include_obj_type=[ma_configure.Util.XGEN_PALETTE])
        for i_xgen_palette_path in xgen_palette_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_palette_path
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
    def _set_xgen_export_(cls, directory_path, location):
        mya_location = bsc_core.DccPathDagOpt(location).set_translate_to('|').to_string()
        group = mya_dcc_objects.Group(mya_location)
        xgen_palette_paths = group.get_all_shape_paths(include_obj_type=[ma_configure.Util.XGEN_PALETTE])
        for i_xgen_palette_path in xgen_palette_paths:
            i_xgen_palette = mya_dcc_objects.XgenPalette(
                i_xgen_palette_path
            )
            i_name = i_xgen_palette.name
            i_xgen_palette_opt = mya_dcc_xgn_operators.Palette(i_name)
            i_xgen_directory_path_src = i_xgen_palette_opt.get_data_directory()
            #
            i_xgen_directory_path_tgt = '{}/{}'.format(directory_path, i_name)
            #
            utl_dcc_objects.OsDirectory_(i_xgen_directory_path_src).set_copy_to_directory(
                i_xgen_directory_path_tgt
            )

    def set_run(self):
        option = self.get_option()
        grow_mesh_directory_path = option.get('grow_mesh_directory')
        xgen_directory_path = option.get('xgen_directory')
        location = option.get('location')
        #
        # with_grow_mesh_abc = option.get('with_grow_mesh_abc')
        # if with_grow_mesh_abc is True:
        #     self._set_grow_mesh_abc_export_(grow_mesh_directory_path, location)
        #
        with_xgen = option.get('with_xgen')
        if with_xgen is True:
            self._set_xgen_export_(xgen_directory_path, location)
