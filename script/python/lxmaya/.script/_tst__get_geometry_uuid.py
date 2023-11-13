# coding:utf-8
from lxbasic import bsc_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators


def get_meshes_uuid(location):
    lis = []
    group = mya_dcc_objects.Group(location)
    if group.get_is_exists() is True:
        paths = group.get_all_shape_paths(include_obj_type='mesh')
        for i_path in paths:
            i_uuid = mya_dcc_operators.MeshOpt(mya_dcc_objects.Shape(i_path)).get_face_vertices_as_uuid()
            lis.append(i_uuid)
    lis.sort()
    return bsc_core.HashMtd.get_hash_value(lis, as_unique_id=True)


def get_curves_uuid(location):
    lis = []
    group = mya_dcc_objects.Group(location)
    if group.get_is_exists() is True:
        paths = group.get_all_shape_paths(include_obj_type='nurbsCurve')
        for i_path in paths:
            i_uuid = mya_dcc_operators.NurbsCurveOpt(mya_dcc_objects.Shape(i_path)).get_knots_as_uuid()
            lis.append(i_uuid)

    lis.sort()
    return bsc_core.HashMtd.get_hash_value(lis, as_unique_id=True)


if __name__ == '__main__':
    get_meshes_uuid('master')
    get_curves_uuid('master')
