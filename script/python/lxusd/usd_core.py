# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Vt, UsdGeom, Gf

import fnmatch

from lxbasic import bsc_core

from lxusd import usd_configure

from lxutil import utl_core

from lxobj import obj_configure

import os


class UsdStageOpt(object):
    def __init__(self, *args):
        if not args:
            stage = Usd.Stage.CreateInMemory()
        else:
            if isinstance(args[0], Usd.Stage):
                stage = args[0]
            elif isinstance(args[0], (str, unicode)):
                file_path = args[0]
                if os.path.isfile(file_path) is True:
                    stage = Usd.Stage.Open(args[0])
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
            utl_core.Log.set_module_result_trace(
                'usd-layer-append',
                u'file="{}"'.format(file_path)
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'usd-layer-append',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_flatten(self):
        self._usd_stage.Flatten()

    def set_sublayer_prepend(self, file_path):
        root_layer = self._usd_stage.GetRootLayer()
        if os.path.isfile(file_path) is True:
            root_layer.subLayerPaths.insert(0, file_path)
            utl_core.Log.set_module_result_trace(
                'usd-layer-prepend',
                u'file="{}"'.format(file_path)
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'usd-layer-prepend',
                u'file="{}" is non-exist'.format(file_path)
            )

    def set_default_prim(self, obj_path):
        prim = self._usd_stage.GetPrimAtPath(obj_path)
        self._usd_stage.SetDefaultPrim(prim)
        #
        utl_core.Log.set_module_result_trace(
            'usd-stage-set-default-prim',
            u'obj="{}"'.format(obj_path)
        )

    def set_export_to(self, file_path):
        self._usd_stage.Export(file_path)
        utl_core.Log.set_module_result_trace(
            'usd-export',
            u'file="{}"'.format(file_path)
        )
        #
        # import os
        # base, ext = os.path.splitext(file_path)
        # self._usd_stage.Export(base + '.usda')
        # #
        # utl_core.Log.set_module_result_trace(
        #     'usd-geometry-export',
        #     'file-path: "{}"'.format(file_path)
        # )

    def set_obj_create_as_override(self, obj_path):
        utl_core.Log.set_module_result_trace(
            'override-prim create',
            u'obj="{}"'.format(obj_path)
        )
        return self._usd_stage.OverridePrim(obj_path)

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
                    self._usd_stage.DefinePrim(i_path, usd_configure.ObjType.TRANSFORM)
        #
        default_prim_path = self._usd_stage.GetPrimAtPath(dag_path_comps[-1])
        self._usd_stage.SetDefaultPrim(default_prim_path)

    def get_objs(self, regex):
        lis = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            i_usd_prim_opt = UsdPrimOpt(i_usd_prim)
            lis.append(i_usd_prim_opt.get_path())
        #
        dag_path_opt = bsc_core.DccPathDagOpt(regex)
        #
        child_paths = bsc_core.DccPathDagMtd.get_dag_children(
            dag_path_opt.get_parent_path(), lis
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

    def get_frame_range(self):
        return (
            int(self._usd_stage.GetStartTimeCode()),
            int(self._usd_stage.GetEndTimeCode())
        )

    def get_all_objs(self):
        lis = []
        for i_usd_prim in self._usd_stage.TraverseAll():
            lis.append(i_usd_prim)
        return lis

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
                            lis.append(_i_filter_child_path)
                        get_fnc_(_i_filter_child_path, _depth)
        #
        lis = []
        #
        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1

        get_fnc_('/', 0)
        return lis


class UsdStageDataOpt(object):
    def __init__(self, stage=None):
        self._usd_stage = stage
    @property
    def usd_instance(self):
        return self._usd_stage

    def set_create(self, type_, value):
        pass


class UsdPrimOpt(object):
    def __init__(self, prim):
        self._usd_prim = prim

    def get_type_name(self):
        return self._usd_prim.GetTypeName()

    def get_path(self):
        return self._usd_prim.GetPath().pathString

    def get_customize_ports(self):
        return self._usd_prim.GetAuthoredAttributes() or []

    def get_customize_attributes(self, includes=None):
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
        print self._usd_prim.GetParent()
        return self.__class__(self._usd_prim.GetParent()).get_path()

    def get_child_paths(self):
        return [self.__class__(i).get_path() for i in self._usd_prim.GetChildren()]

    def __str__(self):
        return '{}(path={})'.format(
            self.get_type_name(),
            self.get_path()
        )


class UsdDataMapper(object):
    MAPPER = {
        obj_configure.Type.CONSTANT_BOOLEAN: Sdf.ValueTypeNames.Bool,
        obj_configure.Type.CONSTANT_INTEGER: Sdf.ValueTypeNames.Int,
        obj_configure.Type.CONSTANT_FLOAT: Sdf.ValueTypeNames.Float,
        obj_configure.Type.CONSTANT_STRING: Sdf.ValueTypeNames.String,
        obj_configure.Type.ARRAY_STRING: Sdf.ValueTypeNames.StringArray,
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
    def __init__(self, prim):
        self._usd_prim = prim
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


class UsdGeometryOpt(object):
    def __init__(self, prim):
        self._usd_prim = prim
        self._usd_geometry = UsdGeom.Imageable(self._usd_prim)

    def set_customize_port_create(self, port_path, dcc_type, dcc_value):
        usd_type, usd_value = UsdDataMapper(dcc_type, dcc_value).get_usd_args()
        if usd_type is not None:
            p = self._usd_geometry.CreatePrimvar(
                port_path,
                usd_type
            )
            p.Set(dcc_value)
        else:
            print dcc_type

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


class UsdGeometryMeshOpt(UsdGeometryOpt):
    def __init__(self, prim):
        super(UsdGeometryMeshOpt, self).__init__(prim)
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

    def set_display_color(self, color):
        p = self._usd_mesh.GetDisplayColorAttr()
        if p:
            pass
        else:
            p = self._usd_mesh.CreateDisplayColorAttr()
        #
        r, g, b = color
        #
        p.Set(
            Vt.Vec3fArray([(r, g, b) for p in range(self.get_point_count())])
        )


class UsdMeshOpt(object):
    def __init__(self, mesh):
        self._usd_mesh = mesh
        self._usd_prim = mesh.GetPrim()
        self._obj_path = self._usd_prim.GetPath().pathString
    @property
    def usd_instance(self):
        return self._usd_mesh

    def get_uv_map_names(self):
        lis = []
        usd_primvars = self._usd_mesh.GetAuthoredPrimvars()
        for uv_primvar in usd_primvars:
            uv_map_name = uv_primvar.GetPrimvarName()
            if uv_primvar.GetIndices():
                lis.append(uv_map_name)
        return lis

    def get_uv_map(self, uv_map_name):
        uv_primvar = self._usd_mesh.GetPrimvar(uv_map_name)
        uv_map_face_vertex_indices = uv_primvar.GetIndices()
        uv_map_coords = uv_primvar.Get()
        return uv_map_face_vertex_indices, uv_map_coords

    def set_uv_map_name_add(self, uv_map_name):
        pass

    def set_uv_map_name_create(self, uv_map_name):
        if self._usd_mesh.HasPrimvar(uv_map_name) is True:
            return self._usd_mesh.GetPrimvar(uv_map_name)
        else:
            utl_core.Log.set_module_result_trace(
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
        primvar.SetIndices(Vt.IntArray(uv_map_face_vertex_indices))
    #
    def set_uv_map(self, uv_map_name, uv_map):
        primvar = self._usd_mesh.GetPrimvar(uv_map_name)
        #
        uv_map_face_vertex_indices, uv_map_coords = uv_map
        primvar.Set(uv_map_coords)
        primvar.SetIndices(Vt.IntArray(uv_map_face_vertex_indices))
