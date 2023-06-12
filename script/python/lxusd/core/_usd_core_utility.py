# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import collections
#
import math
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, Gf, UsdGeom, UsdShade, UsdLux

import fnmatch

from lxbasic import bsc_core

from lxusd import usd_configure

from lxutil import utl_core

from lxuniverse import unr_configure

import os


class UsdBasic(object):
    @classmethod
    def _set_file_open_(cls, file_path):
        return Usd.Stage.Open(file_path, Usd.Stage.LoadAll)
    @classmethod
    def copy_with_references_fnc(cls, file_path_src, directory_tgt, replace=False):
        s = Usd.Stage.Open(file_path_src, Usd.Stage.LoadAll)
        layers = s.GetUsedLayers()
        directory_src = bsc_core.StgFileOpt(file_path_src).get_directory_path()
        for i in layers:
            i_file_path_src = i.realPath
            if i_file_path_src:
                i_name = i_file_path_src[len(directory_src)+1:]
                i_file_path_tgt = '{}/{}'.format(directory_tgt, i_name)
                bsc_core.StgFileOpt(i_file_path_src).set_copy_to_file(
                    i_file_path_tgt, replace=replace
                )


class UsdStageOpt(UsdBasic):
    def __init__(self, *args):
        if not args:
            stage = Usd.Stage.CreateInMemory()
        else:
            if isinstance(args[0], Usd.Stage):
                stage = args[0]
            elif isinstance(args[0], six.string_types):
                file_path = args[0]
                if os.path.isfile(file_path) is True:
                    bsc_core.LogMtd.trace_method_result(
                        'usd-file open is started', 'file="{}"'.format(
                            file_path
                        )
                    )
                    stage = self._set_file_open_(file_path)
                    bsc_core.LogMtd.trace_method_result(
                        'usd-file open is completed', 'file="{}"'.format(
                            file_path
                        )
                    )
                else:
                    raise OSError()
            else:
                raise TypeError()
        #
        self._usd_stage = stage
        self._usd_stage.SetMetadata("metersPerUnit", 0.01)
        #
        UsdGeom.SetStageUpAxis(
            self._usd_stage, UsdGeom.Tokens.y
        )
    @property
    def usd_instance(self):
        return self._usd_stage

    def set_sublayer_append(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.append(file_path)
            bsc_core.LogMtd.trace_method_result(
                'usd-layer-append',
                u'file="{}"'.format(file_path)
            )
        else:
            bsc_core.LogMtd.trace_method_warning(
                'usd-layer-append',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_flatten(self):
        self._usd_stage.Flatten()

    def set_sublayer_prepend(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.insert(0, file_path)
            bsc_core.LogMtd.trace_method_result(
                'usd-layer prepend',
                u'file="{}"'.format(file_path)
            )
        else:
            bsc_core.LogMtd.trace_method_warning(
                'usd-layer prepend',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_default_prim(self, obj_path):
        prim = self._usd_stage.GetPrimAtPath(obj_path)
        self._usd_stage.SetDefaultPrim(prim)
        #
        bsc_core.LogMtd.trace_method_result(
            'default-prim set',
            u'obj="{}"'.format(obj_path)
        )

    def set_export_to(self, file_path):
        self._usd_stage.Export(file_path)
        bsc_core.LogMtd.trace_method_result(
            'usd-export',
            u'file="{}"'.format(file_path)
        )
        #
        # import os
        # base, ext = os.path.splitext(file_path)
        # self._usd_stage.Export(base + '.usda')
        # #
        # bsc_core.LogMtd.trace_method_result(
        #     'usd-geometry-export',
        #     'file-path: "{}"'.format(file_path)
        # )

    def set_obj_create_as_override(self, obj_path):
        bsc_core.LogMtd.trace_method_result(
            'override-prim create',
            u'obj="{}"'.format(obj_path)
        )
        return self._usd_stage.OverridePrim(obj_path)

    def get_obj_is_exists(self, obj_path):
        return self._usd_stage.GetPrimAtPath(obj_path).IsValid()

    def get_obj(self, obj_path):
        return self._usd_stage.GetPrimAtPath(obj_path)

    def set_obj_create(self, obj_path):
        dag_path_opt = bsc_core.DccPathDagOpt(obj_path)
        paths = dag_path_opt.get_component_paths()
        paths.reverse()
        for i_path in paths:
            if i_path != '/':
                if self._usd_stage.GetPrimAtPath(obj_path).IsValid() is False:
                    self._usd_stage.DefinePrim(i_path, '')
        return self.get_obj(obj_path)

    def set_root_create(self, root, override=False):
        dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(
            root, pathsep=usd_configure.Obj.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i_path in dag_path_comps:
            if i_path != usd_configure.Obj.PATHSEP:
                if override is True:
                    self.set_obj_create_as_override(i_path)
                else:
                    self._usd_stage.DefinePrim(i_path, usd_configure.ObjType.Xform)
        #
        default_prim_path = self._usd_stage.GetPrimAtPath(dag_path_comps[-1])
        self._usd_stage.SetDefaultPrim(default_prim_path)

    def get_objs(self, regex):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            i_usd_prim_opt = UsdPrimOpt(i_usd_prim)
            list_.append(i_usd_prim_opt.get_path())
        #
        dag_path_opt = bsc_core.DccPathDagOpt(regex)
        #
        child_paths = bsc_core.DccPathDagMtd.get_dag_child_paths(
            dag_path_opt.get_parent_path(), list_
        )
        #
        return [
            self.get_obj(i) for i in fnmatch.filter(child_paths, regex)
        ]

    def get_obj_paths(self, regex):
        return [UsdPrimOpt(i).get_path() for i in self.get_objs(regex)]
    @classmethod
    def _set_metadata_copy_(cls, src_stage, tgt_stage):
        copy_list = [
            'metersPerUnit',
            'upAxis',
            #
            'startTimeCode',
            'endTimeCode',

        ]
        for i in copy_list:
            tgt_stage.SetMetadata(
                i, src_stage.GetMetadata(i)
            )

    def set_copy_to_new_stage(self, file_path):
        src_path = '/assets/chr/laohu_xiao'
        tgt_path = '/master/hi'
        #
        src_file_path = '/data/f/usd-cpy/test_src_1.usda'
        tgt_file_path = '/data/f/usd-cpy/test_tgt_3.usda'
        #
        src_stage_opt = self.__class__(src_file_path)
        src_stage = src_stage_opt.usd_instance
        src_layer = src_stage.GetRootLayer()
        src_obj = src_stage_opt.get_obj(src_path)
        #
        tgt_stage_opt = self.__class__()
        tgt_stage = tgt_stage_opt.usd_instance
        tgt_layer = tgt_stage.GetRootLayer()
        tgt_obj = tgt_stage_opt.set_obj_create(tgt_path)
        tgt_stage_opt.set_default_prim(
            '/master'
        )

        # Sdf.CopySpec(
        #     src_layer,
        #     src_obj.GetPath(),
        #     tgt_layer,
        #     tgt_obj.GetPath()
        # )

        self._set_metadata_copy_(src_stage, tgt_stage)

        tgt_stage_opt.set_export_to(
            tgt_file_path
        )

    def get_fps(self):
        return self._usd_stage.GetTimeCodesPerSecond()

    def set_frame(self, frame):
        self._usd_stage.Set()

    def set_frame_range(self, start_frame, end_frame):
        pass

    def get_frame_range(self):
        return (
            int(self._usd_stage.GetStartTimeCode()),
            int(self._usd_stage.GetEndTimeCode())
        )

    def get_all_objs(self):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            list_.append(i_usd_prim)
        return list_

    def get_all_obj_paths(self):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            if i_usd_prim.IsValid() is True:
                list_.append(i_usd_prim.GetPath().pathString)
        return list_

    def get_count(self):
        return len([i for i in self._usd_stage.TraverseAll()])

    def set_obj_paths_find(self, regex):
        def get_fnc_(path_, depth_):
            _depth = depth_+1
            if _depth <= depth_maximum:
                _prim = self._usd_stage.GetPrimAtPath(path_)
                _filter_name = filter_names[_depth]

                if path_ == '/':
                    _filter_path = '/*'
                else:
                    _filter_path = '{}/{}'.format(
                        path_, _filter_name
                    )
                _child_paths = UsdPrimOpt(_prim).get_child_paths()
                _filter_child_paths = fnmatch.filter(
                    _child_paths, _filter_path
                )
                if _filter_child_paths:
                    for _i_filter_child_path in _filter_child_paths:
                        if _depth == depth_maximum:
                            list_.append(_i_filter_child_path)
                        get_fnc_(_i_filter_child_path, _depth)
        #
        list_ = []
        #
        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1

        get_fnc_('/', 0)
        return list_

    def set_active_at(self, location, boolean):
        prim = self._usd_stage.GetPrimAtPath(location)
        if prim.IsValid():
            prim.SetActive(boolean)

    def get_bounding_box(self, location=None, active=False):
        b_box_cache = UsdGeom.BBoxCache(
            1,
            includedPurposes=[
                UsdGeom.Tokens.default_,
                UsdGeom.Tokens.render,
                UsdGeom.Tokens.proxy
            ],
            useExtentsHint=True,
            ignoreVisibility=True,
        )
        if location is not None:
            usd_prim = self._usd_stage.GetPrimAtPath(location)
        else:
            usd_prim = self._usd_stage.GetDefaultPrim()
        return b_box_cache.ComputeWorldBound(usd_prim)

    def get_geometry_args(self, location=None, use_int_size=False):
        if self.get_obj_is_exists(location) is True:
            b_box = self.get_bounding_box(location)
            r = b_box.GetRange()
            return bsc_core.RawBBoxMtd.get_geometry_args(
                r.GetMin(), r.GetMax(), use_int_size
            )

    def get_radius(self, pivot):
        b_box_cache = UsdGeom.BBoxCache(
            1,
            includedPurposes=[
                UsdGeom.Tokens.default_,
                UsdGeom.Tokens.render,
                UsdGeom.Tokens.proxy
            ],
            useExtentsHint=True,
            ignoreVisibility=True,
        )
        dict_ = {}
        for i_usd_prim in self._usd_stage.TraverseAll():
            if i_usd_prim.IsValid():
                i_b_box = b_box_cache.ComputeWorldBound(i_usd_prim)
                if i_usd_prim.GetTypeName() in [
                    usd_configure.ObjType.Mesh
                ]:
                    i_range = i_b_box.GetRange()
                    i_radius = bsc_core.RawBBoxMtd.get_radius(
                        i_range.GetMin(), i_range.GetMax(), pivot
                    )
                    dict_.setdefault(
                        i_radius, []
                    ).append(
                        i_usd_prim
                    )
        if dict_:
            usd_prim = dict_[max(dict_.keys())][0]
            return UsdMeshOpt(
                UsdGeom.Mesh(usd_prim)
            ).get_radius(pivot)

    def load_by_locations_fnc(self, file_path, locations, active_locations=None):
        stage_tmp = Usd.Stage.Open(file_path, Usd.Stage.LoadAll)
        if isinstance(active_locations, (tuple, list)):
            for i in active_locations:
                i_p = stage_tmp.GetPrimAtPath(i)
                if i_p.IsValid():
                    i_p.SetActive(True)
        #
        for i_location_arg in locations:
            if isinstance(i_location_arg, (tuple, list)):
                i_location_source, i_location_target = i_location_arg
            elif isinstance(i_location_arg, six.string_types):
                i_location_source, i_location_target = i_location_arg, i_location_arg
            else:
                raise RuntimeError()
            # when target is exists, use target
            # etc. we have source location "/master/hi", need map to "/master/mod/hi", "/master/hi" is already exists, use "/master/hi"
            i_p_tgt = stage_tmp.GetPrimAtPath(i_location_target)
            if i_p_tgt.IsValid():
                self.load_by_location_fnc(file_path, i_location_target, i_location_target)
            # when target is non exists, use source and reference source to target
            else:
                i_p_src = stage_tmp.GetPrimAtPath(i_location_source)
                if i_p_src.IsValid():
                    self.load_by_location_fnc(file_path, i_location_source, i_location_target)
        #
        self._usd_stage.Flatten()

    def load_by_location_fnc(self, file_path, location_source, location_target):
        usd_location = self._usd_stage.GetPseudoRoot()
        #
        dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(
            location_target, pathsep=usd_configure.Obj.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i in dag_path_comps:
            if i != usd_configure.Obj.PATHSEP:
                usd_location = self._usd_stage.DefinePrim(i, usd_configure.ObjType.Xform)
        #
        usd_location.GetReferences().AddReference(file_path, location_source)

    def get_all_mesh_prims(self):
        list_ = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            if i_usd_prim.GetTypeName() == 'Mesh':
                list_.append(i_usd_prim)
        return list_


class UsdFileWriteOpt(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._usd_stage = Usd.Stage.CreateInMemory()

    def set_location_add(self, location):
        dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(
            location, pathsep=usd_configure.Obj.PATHSEP
        )
        if dag_path_comps:
            dag_path_comps.reverse()
        #
        for i in dag_path_comps:
            if i != usd_configure.Obj.PATHSEP:
                self.set_obj_add(i)
        #
        default_prim_path = self._usd_stage.GetPrimAtPath(dag_path_comps[1])
        self._usd_stage.SetDefaultPrim(default_prim_path)

    def set_obj_add(self, path):
        self._usd_stage.DefinePrim(path, usd_configure.ObjType.Xform)

    def set_save(self):
        file_opt = bsc_core.StgFileOpt(self._file_path)
        file_opt.create_directory()
        self._usd_stage.Export(self._file_path)
        bsc_core.LogMtd.trace_method_result(
            'usd-export',
            u'file="{}"'.format(self._file_path)
        )


class UsdFileOpt(object):
    def __init__(self, file_path, location=None):
        if location is not None:
            usd_stage_mask = Usd.StagePopulationMask()
            usd_stage_mask.Add(
                Sdf.Path(location)
            )
            self._usd_stage = Usd.Stage.OpenMasked(
                file_path, usd_stage_mask
            )
        else:
            self._usd_stage = Usd.Stage.OpenMasked(
                file_path, Usd.Stage.LoadAll
            )

    def get_usd_instance(self):
        return self._usd_stage
    usd_instance = property(get_usd_instance)


class UsdStageDataOpt(object):
    def __init__(self, stage=None):
        self._usd_stage = stage
    @property
    def usd_instance(self):
        return self._usd_stage

    def set_create(self, type_, value):
        pass


class UsdPrimOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim

    def get_type_name(self):
        return self._usd_prim.GetTypeName()

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    def get_port(self, port_path):
        return self._usd_prim.GetAttribute(port_path)

    def get_customize_ports(self):
        return self._usd_prim.GetAuthoredAttributes() or []

    def get_customize_attributes(self, includes=None, use_full_path=False):
        dic = {}
        _ = self.get_customize_ports()
        for i in _:
            p = i.GetName().split(':')[-1]
            if isinstance(includes, (tuple, list)):
                if p not in includes:
                    continue
            dic[p] = i.Get()
        return dic

    def get_parent_path(self):
        # print self._usd_prim.GetParent()
        return self.__class__(self._usd_prim.GetParent()).get_path()

    def get_children(self):
        return self._usd_prim.GetChildren()

    def get_child_paths(self):
        return [i.GetPath().pathString for i in self._usd_prim.GetChildren()]

    def get_descendant_paths(self):
        def rcs_fnc_(list__, prim_):
            for _i_prim in prim_.GetChildren():
                list__.append(_i_prim.GetPath().pathString)
                rcs_fnc_(_i_prim)

        list_ = []
        rcs_fnc_(list_, self._usd_prim)
        return list_

    def get_variant_set(self, variant_set_name):
        return self._usd_prim.GetVariantSet(variant_set_name)

    def get_variant_sets(self):
        list_ = []
        usd_variant_sets = self._usd_prim.GetVariantSets()
        for i in usd_variant_sets.GetNames():
            i_variant_set = self._usd_prim.GetVariantSet(i)
            list_.append(
                i_variant_set
            )
        return list_

    def get_variant_names(self, variant_set_name):
        return UsdVariantSetOpt(self.get_variant_set(variant_set_name)).get_variant_names()

    def get_variant_dict(self):
        dic = collections.OrderedDict()
        for i in self.get_variant_sets():
            i_variant_set_opt = UsdVariantSetOpt(i)
            dic[i_variant_set_opt.get_name()] = i_variant_set_opt.get_current_variant_name(), i_variant_set_opt.get_variant_names()
        return dic
    @classmethod
    def _add_customize_attribute_(cls, usd_obj, key, value):
        if isinstance(value, bool):
            dcc_type_name = unr_configure.Type.CONSTANT_BOOLEAN
        elif isinstance(value, int):
            dcc_type_name = unr_configure.Type.CONSTANT_INTEGER
        elif isinstance(value, float):
            dcc_type_name = unr_configure.Type.CONSTANT_FLOAT
        elif isinstance(value, six.string_types):
            dcc_type_name = unr_configure.Type.CONSTANT_STRING
        else:
            raise TypeError()
        #
        usd_type = UsdDataMapper.MAPPER[dcc_type_name]
        p = usd_obj.CreatePrimvar(
            key,
            usd_type
        )
        p.Set(value)

    def __str__(self):
        return '{}(path={})'.format(
            self.get_type_name(),
            self.get_path()
        )


class UsdVariantSetOpt(object):
    def __init__(self, usd_usd_variant):
        self._usd_usd_variant = usd_usd_variant
    @property
    def usd_instance(self):
        return self._usd_usd_variant

    def get_name(self):
        return self._usd_usd_variant.GetName()

    def get_variant_names(self):
        return self._usd_usd_variant.GetVariantNames()

    def get_current_variant_name(self):
        return self._usd_usd_variant.GetVariantSelection()


class UsdDataMapper(object):
    MAPPER = {
        unr_configure.Type.CONSTANT_BOOLEAN: Sdf.ValueTypeNames.Bool,
        unr_configure.Type.CONSTANT_INTEGER: Sdf.ValueTypeNames.Int,
        unr_configure.Type.CONSTANT_FLOAT: Sdf.ValueTypeNames.Float,
        unr_configure.Type.CONSTANT_STRING: Sdf.ValueTypeNames.String,
        #
        unr_configure.Type.COLOR_COLOR3: Sdf.ValueTypeNames.Color3f,
        unr_configure.Type.ARRAY_COLOR3: Sdf.ValueTypeNames.Color3fArray,
        #
        unr_configure.Type.ARRAY_STRING: Sdf.ValueTypeNames.StringArray,
    }
    def __init__(self, dcc_type, dcc_value):
        self._dcc_type = dcc_type
        self._dcc_value = dcc_value

    def get_usd_args(self):
        key = self._dcc_type.category.name, self._dcc_type.name
        if key in self.MAPPER:
            usd_type = self.MAPPER[key]
            return usd_type, None
        return None, None


class UsdTransformOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_transform = UsdGeom.Imageable(self._usd_prim)

    def set_visible(self, boolean):
        p = self._usd_transform.GetVisibilityAttr()
        if p:
            pass
        else:
            p = self._usd_transform.CreateVisibilityAttr(
                UsdGeom.Tokens.inherited,
                True
            )
        #
        p.Set(
            UsdGeom.Tokens.inherited if boolean is True else UsdGeom.Tokens.invisible
        )


class _Basic(object):
    @classmethod
    def _get_int_array_(cls, usd_int_array):
        return list(usd_int_array)
    @classmethod
    def _get_point_array_(cls, usd_point_array):
        return [tuple(i) for i in usd_point_array]
    @classmethod
    def _get_coord_array_(cls, usd_coord_array):
        return [tuple(i) for i in usd_coord_array]
    @classmethod
    def _get_matrix_(cls, usd_matrix):
        list_ = []
        for row in usd_matrix:
            for column in row:
                list_.append(column)
        return list_
    @classmethod
    def _get_usd_matrix_(cls, matrix):
        list_ = []
        for i in range(4):
            rows = []
            for j in range(4):
                rows.append(matrix[i * 4 + j])
            list_.append(rows)
        #
        return Gf.Matrix4d(list_)


class UsdGeometryOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_geometry = UsdGeom.Imageable(self._usd_prim)

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    def set_customize_port_create(self, port_path, dcc_type, dcc_value):
        usd_type, usd_value = UsdDataMapper(dcc_type, dcc_value).get_usd_args()
        if usd_type is not None:
            p = self._usd_geometry.CreatePrimvar(
                port_path,
                usd_type
            )
            p.Set(dcc_value)

    def set_customize_port_create_(self, port_path, type_path, dcc_value):
        category_name, type_name = type_path.split(unr_configure.Type.PATHSEP)
        key = category_name, type_name
        if key in UsdDataMapper.MAPPER:
            usd_type = UsdDataMapper.MAPPER[key]
            p = self._usd_geometry.CreatePrimvar(
                port_path,
                usd_type
            )
            p.Set(dcc_value)

    def set_customize_port_create_as_face_color(self, port_path, type_path, usd_value):
        category_name, type_name = type_path.split(unr_configure.Type.PATHSEP)
        key = category_name, type_name
        if key in UsdDataMapper.MAPPER:
            usd_type = UsdDataMapper.MAPPER[key]
            p = self._usd_geometry.CreatePrimvar(
                port_path,
                usd_type,
                UsdGeom.Tokens.uniform
            )
            p.Set(usd_value)

    def set_visible(self, boolean):
        p = self._usd_geometry.GetVisibilityAttr()
        if p:
            pass
        else:
            p = self._usd_geometry.CreateVisibilityAttr(
                UsdGeom.Tokens.inherited,
                True
            )
        #
        p.Set(
            UsdGeom.Tokens.inherited if boolean is True else UsdGeom.Tokens.invisible
        )

    def set_display_color_fill(self, color):
        pass


class UsdGeometryOpt_(object):
    def __init__(self, usd_fnc):
        self._usd_fnc = usd_fnc
        self._usd_prim = usd_fnc.GetPrim()

    def set_display_color_fill(self, color):
        p = self._usd_fnc.GetDisplayColorPrimvar()
        if p is None:
            p = self._usd_fnc.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )
        #
        r, g, b = color
        #
        p.Set(
            Vt.Vec3fArray([(r, g, b)])
        )


class UsdGeometryMeshOpt(UsdGeometryOpt):
    def __init__(self, usd_prim):
        super(UsdGeometryMeshOpt, self).__init__(usd_prim)
        self._usd_mesh = UsdGeom.Mesh(self._usd_prim)

    def get_points(self):
        p = self._usd_mesh.GetPointsAttr()
        if p.GetNumTimeSamples():
            v = p.Get(0)
        else:
            v = p.Get()
        return v

    def get_point_count(self):
        return len(self.get_points())

    def get_display_colors_as_fill(self, color):
        r, g, b = color
        return Vt.Vec3fArray([(r, g, b)])

    def set_display_color_fill(self, color):
        p = self._usd_mesh.GetDisplayColorPrimvar()
        if p:
            pass
        else:
            p = self._usd_mesh.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )
        #
        r, g, b = color
        #
        p.Set(
            Vt.Vec3fArray([(r, g, b)])
        )

    def set_display_colors(self, usd_colors):
        p = self._usd_mesh.GetDisplayColorPrimvar()
        if p:
            pass
        else:
            p = self._usd_mesh.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )
        p.Set(usd_colors)

    def get_display_colors(self):
        p = self._usd_mesh.GetDisplayColorPrimvar()
        if p:
            pass
        else:
            p = self._usd_mesh.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.constant
            )
        return p.Get()

    def get_bounding_box(self):
        b_box = self._usd_mesh.ComputeExtent()

    def get_face_vertex_counts(self):
        usd_mesh = self._usd_mesh
        a = usd_mesh.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return _Basic._get_int_array_(v)
        return []

    def get_face_vertex_indices(self):
        a = self._usd_mesh.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            v = a.Get(0)
        else:
            v = a.Get()
        if v:
            return _Basic._get_int_array_(v)
        return []

    def get_uv_map_names(self):
        list_ = []
        usd_mesh = self._usd_mesh
        usd_primvars = usd_mesh.GetAuthoredPrimvars()
        for i_primvar in usd_primvars:
            i_name = i_primvar.GetPrimvarName()
            if i_primvar.GetIndices():
                list_.append(i_name)
        return list_

    def get_uv_map(self, uv_map_name):
        a = self._usd_mesh.GetPrimvar(uv_map_name)
        uv_map_face_vertex_counts = self.get_face_vertex_counts()
        return uv_map_face_vertex_counts, _Basic._get_int_array_(a.GetIndices()), a.Get()

    def get_uv_map_coords(self, uv_map_name):
        a = self._usd_mesh.GetPrimvar(uv_map_name)
        return a.Get()

    def get_uv_map_face_vertex_counts(self, uv_map_name):
        return self.get_face_vertex_counts()

    def get_uv_map_face_vertex_indices(self, uv_map_name):
        a = self._usd_mesh.GetPrimvar(uv_map_name)
        return _Basic._get_int_array_(a.GetIndices())

    def get_uv_maps(self):
        dic = {}
        uv_map_names = self.get_uv_map_names()
        for i_uv_map_name in uv_map_names:
            uv_map = self.get_uv_map(i_uv_map_name)
            dic[i_uv_map_name] = uv_map
        return dic


class UsdMeshOpt(object):
    def __init__(self, usd_fnc):
        self._usd_mesh = usd_fnc
        self._usd_prim = usd_fnc.GetPrim()
        self._obj_path = self._usd_prim.GetPath().pathString

    def get_path(self):
        return self._obj_path
    @property
    def usd_instance(self):
        return self._usd_mesh

    def get_uv_map_names(self):
        list_ = []
        usd_primvars = self._usd_mesh.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            uv_map_name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                list_.append(uv_map_name)
        return list_

    def get_uv_map(self, uv_map_name):
        uv_primvar = self._usd_mesh.GetPrimvar(uv_map_name)
        if uv_primvar:
            uv_map_face_vertex_indices = uv_primvar.GetIndices()
            uv_map_coords = uv_primvar.Get()
            return uv_map_face_vertex_indices, uv_map_coords

    def set_uv_map_name_add(self, uv_map_name):
        pass

    def set_uv_map_name_create(self, uv_map_name):
        if self._usd_mesh.HasPrimvar(uv_map_name) is True:
            return self._usd_mesh.GetPrimvar(uv_map_name)
        else:
            bsc_core.LogMtd.trace_method_result(
                'uv-map create',
                u'uv-map-path="{}.{}"'.format(
                    self._obj_path, uv_map_name
                )
            )
            return self._usd_mesh.CreatePrimvar(
                uv_map_name,
                Sdf.ValueTypeNames.TexCoord2fArray,
                UsdGeom.Tokens.faceVarying
            )

    def _get_primvar_(self, primvar_name):
        if self._usd_mesh.HasPrimvar(primvar_name) is True:
            return self._usd_mesh.GetPrimvar(primvar_name)
        else:
            return self._usd_mesh.CreatePrimvar(
                primvar_name,
                Sdf.ValueTypeNames.TexCoord2fArray,
                UsdGeom.Tokens.faceVarying
            )

    def set_uv_map_create(self, uv_map_name, uv_map):
        if uv_map_name == 'map1':
            uv_map_name = 'st'
        #
        primvar = self.set_uv_map_name_create(uv_map_name)
        #
        uv_map_face_vertex_indices, uv_map_coords = uv_map
        primvar.Set(uv_map_coords)
        primvar.SetIndices(
            Vt.IntArray(uv_map_face_vertex_indices)
        )
    #
    def set_uv_map(self, uv_map_name, uv_map):
        primvar = self._usd_mesh.GetPrimvar(uv_map_name)
        #
        indices, values = uv_map
        primvar.Set(values)
        primvar.SetIndices(
            Vt.IntArray(indices)
        )

    def set_display_color_fill(self, color):
        UsdGeometryMeshOpt(
            self._usd_prim
        ).set_display_color_fill(
            color
        )

    def set_display_colors(self, usd_colors):
        UsdGeometryMeshOpt(
            self._usd_prim
        ).set_display_colors(
            usd_colors
        )

    def get_display_colors(self):
        return UsdGeometryMeshOpt(
            self._usd_prim
        ).get_display_colors()

    def set_display_color_as_face_vertices(self, data):
        p = self._usd_mesh.GetDisplayColorPrimvar()
        if not p:
            p = self._usd_mesh.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.faceVarying
            )
        #
        indices, values = data
        p.Set(values)
        p.SetIndices(
            Vt.IntArray(indices)
        )

    def set_display_color_as_face_color(self, data):
        p = self._usd_mesh.GetDisplayColorPrimvar()
        if not p:
            p = self._usd_mesh.CreateDisplayColorPrimvar(
                UsdGeom.Tokens.uniform
            )
        #
        values = data
        p.Set(values)

    def get_display_colors_as_fill(self, color):
        return UsdGeometryMeshOpt(
            self._usd_prim
        ).get_display_colors_as_fill(
            color
        )

    def get_display_color_map_from_uv_map(self, uv_map_name):
        uv_map = self.get_uv_map(uv_map_name)
        if uv_map:
            colors = []
            vertex_indices, coords = uv_map
            c = len(coords)
            for i in range(c):
                if i <= c:
                    i_x, i_y = coords[i]
                    i_rgb = (i_x-int(i_x) % 1, i_y-int(i_y) % 1, 0)
                    # i_rgb = (i_x / 10.0 % 10.0, i_y / 1.0 % 10.0, 0)
                else:
                    i_rgb = (0, 0, 1)
                #
                colors.append(i_rgb)
            return vertex_indices, Vt.Vec3fArray(colors)

    def get_face_color_fom_shell(self, offset=0, seed=0):
        vertex_counts, vertex_indices = self.get_face_vertices()
        face_to_shell_dict = bsc_core.MeshFaceShellMtd.get_shell_dict_from_face_vertices(
            vertex_counts, vertex_indices
        )
        max_shell_index = max(face_to_shell_dict.values())
        choice_colors = bsc_core.RawColorMtd.get_choice_colors(
            count=max_shell_index+1, maximum=1.0, offset=offset, seed=seed
        )
        colors = []
        c = len(vertex_counts)
        for i in range(c):
            i_shell_index = face_to_shell_dict[i]
            i_rgb = choice_colors[i_shell_index]
            colors.append(i_rgb)
        return Vt.Vec3fArray(colors)

    def get_face_count(self):
        usd_mesh = self._usd_mesh
        return usd_mesh.GetFaceCount()

    def get_face_vertices(self):
        return self.get_face_vertex_counts(), self.get_face_vertex_indices()

    def get_face_vertex_counts(self):
        usd_mesh = self._usd_mesh
        a = usd_mesh.GetFaceVertexCountsAttr()
        if a.GetNumTimeSamples():
            return a.Get(0)
        else:
            return a.Get()

    def get_face_vertex_indices(self, reverse=False):
        usd_mesh = self._usd_mesh
        a = usd_mesh.GetFaceVertexIndicesAttr()
        if a.GetNumTimeSamples():
            return a.Get(0)
        else:
            return a.Get()

    def get_points(self):
        p = self._usd_mesh.GetPointsAttr()
        if p.GetNumTimeSamples():
            return p.Get(0)
        else:
            return p.Get()

    def get_point_count(self):
        return len(self.get_points())

    def get_radius(self, pivot):
        o_x, o_y, o_z = pivot
        points = self.get_points()
        set_ = set()
        for i_point in points:
            i_x, i_y, i_z = i_point
            i_r = abs(math.sqrt((i_x+o_x)**2+(i_z+o_z)**2))
            set_.add(i_r)
        return max(set_)


class UsdNurbsCurvesOpt(object):
    def __init__(self, usd_fnc):
        pass


class UsdBasisCurvesOpt(object):
    def __init__(self, usd_fnc):
        pass

