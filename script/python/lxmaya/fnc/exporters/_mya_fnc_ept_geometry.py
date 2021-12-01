# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import os

import copy

from lxbasic import bsc_core

from lxobj import obj_core

from lxutil import utl_core

from lxutil.dcc.dcc_objects import _utl_dcc_obj_storage

from lxmaya import ma_configure

import lxobj.core_objects as core_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

import lxusd.fnc.exporters as usd_fnc_exporters


class GeometryAbcExporter(object):
    FILE = 'file'
    FRAME_RANGE = 'frameRange'
    STEP = 'step'
    ROOT = 'root'
    ATTR = 'attr'
    #
    DATA_FORMAT = 'dataFormat'
    #
    NO_NORMAL = 'noNormals'
    RENDER_ONLY = 'ro'
    STRIP_NAMESPACE = 'stripNamespaces'
    UV_WRITE = 'uvWrite'
    WRITE_FACE_SETS = 'writeFaceSets'
    WHOLE_FRAME_GEO = 'wholeFrameGeo'
    WORLD_SPACE = 'worldSpace'
    WRITE_VISIBILITY = 'writeVisibility'
    EULER_FILTER = 'eulerFilter'
    WRITE_CREASES = 'writeCreases'
    WRITE_UV_SETS = 'writeUVSets'
    #
    OPTION = {
        NO_NORMAL: False,
        RENDER_ONLY: False,
        STRIP_NAMESPACE: True,
        UV_WRITE: True,
        WRITE_FACE_SETS: False,
        WHOLE_FRAME_GEO: False,
        WORLD_SPACE: True,
        WRITE_VISIBILITY: True,
        EULER_FILTER: False,
        WRITE_CREASES: False,
        WRITE_UV_SETS: True,
    }
    #
    OGAWA = 'ogawa'
    HDF = 'hdf'
    #
    DATA_FROAMTS = [
        OGAWA,
        HDF
    ]
    PLUG_NAME = 'AbcExport'
    def __init__(self, file_path, root=None, frame=None, step=None, attribute=None, option=None, data_format=None):
        self._file_path = file_path
        #
        dcc_root_dag_opt = bsc_core.DccPathDagOpt(root)
        self._root = dcc_root_dag_opt.set_translate_to('|').get_value()
        self._star_frame, self._end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        self._step = step
        self._attribute = attribute
        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v
                else:
                    raise KeyError()
        self._data_format = data_format
        #
        self._results = []
    @classmethod
    def _get_file_(cls, file_path):
        return '-{0} {1}'.format(cls.FILE, file_path.replace('\\', '/'))
    @classmethod
    def _get_option_(cls, option):
        if isinstance(option, dict):
            lis = ['-{0}'.format(k) for k, v in option.items() if v is True]
            if lis:
                return ' '.join(lis)
    @classmethod
    def _get_data_format_(cls, data_format):
        if isinstance(data_format, (str, unicode)):
            if data_format in cls.DATA_FROAMTS:
                return '-{0} {1}'.format(cls.DATA_FORMAT, data_format)
            return '-{0} {1}'.format(cls.DATA_FORMAT, cls.OGAWA)
        return '-{0} {1}'.format(cls.DATA_FORMAT, cls.OGAWA)
    @classmethod
    def _get_frame_(cls, star_frame, end_frame):
        return '-{0} {1} {2}'.format(cls.FRAME_RANGE, star_frame, end_frame)
    @classmethod
    def _get_step_(cls, step):
        if isinstance(step, (int, float)):
            return '-{0} {1}'.format(cls.STEP, step)
    @classmethod
    def _get_root_(cls, root):
        lis = cls._get_exists_dcc_paths_(root)
        if lis:
            return ' '.join(['-{0} {1}'.format(cls.ROOT, i) for i in lis])
    @classmethod
    def _get_exists_dcc_paths_(cls, obj_path_args):
        if isinstance(obj_path_args, (str, unicode)):
            if cmds.objExists(obj_path_args):
                return [cmds.ls(obj_path_args, long=1)[0]]
        elif isinstance(obj_path_args, (tuple, list)):
            return [cmds.ls(i, long=1)[0] for i in obj_path_args if cmds.objExists(i)]
    @classmethod
    def _get_strs_(cls, string, includes=None):
        lis = []
        if isinstance(string, (str, unicode)):
            if includes:
                if string in includes:
                    lis = [string]
            else:
                lis = [string]
        elif isinstance(string, (tuple, list)):
            for i in string:
                if includes:
                    if i in includes:
                        lis.append(i)
                else:
                    lis.append(i)
        return lis
    @classmethod
    def _get_attribute_(cls, attr_name):
        lis = cls._get_strs_(attr_name)
        #
        if lis:
            _ = ' '.join(['{0} {1}'.format(cls.ATTR, i) for i in lis])
        else:
            _ = None
        return _
    @staticmethod
    def _get_j_(js):
        _ = [i for i in js if i is not None]
        if _:
            return ' '.join(_)
    @classmethod
    def _set_cmd_run_(cls, j):
        """
        :param j: str
        :return: None
        """
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.AbcExport(j=j)
    #
    def set_run(self):
        js = [
            self._get_frame_(self._star_frame, self._end_frame),
            self._get_step_(self._step),
            self._get_attribute_(self._attribute),
            self._get_option_(self._option),
            self._get_data_format_(self._data_format),
            self._get_root_(self._root),
            self._get_file_(self._file_path)
        ]
        #
        file_ = _utl_dcc_obj_storage.OsFile(self._file_path)
        directory_ = file_.directory
        if directory_.get_is_exists() is False:
            directory_.set_create()
        #
        j = self._get_j_(js)
        if j:
            self._results = self._set_cmd_run_(j)
            if self._results:
                for i in self._results:
                    utl_core.Log.set_result_trace(
                        'export ".abc": "{}"'.format(i)
                    )
        return self._results

    def get_outputs(self):
        return self._results


class GeometryUsdExporter(object):
    OPTION = dict(
        exportUVs=1,
        exportColorSets=1,
        defaultMeshScheme='catmullClark',
        defaultUSDFormat='usdc',
        animation=0,
        eulerFilter=0,
        staticSingleSample=0,
        startTime=1,
        endTime=1,
        frameStride=1,
        frameSample=0.0,
        parentScope='',
        exportDisplayColor=0,
        shadingMode='displayColor',
        convertMaterialsTo='UsdPreviewSurface',
        exportInstances=1,
        exportVisibility=1,
        mergeTransformAndShape=0,
        stripNamespaces=1
    )
    PLUG_NAME = 'mayaUsdPlugin'
    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root

        self._option = copy.copy(self.OPTION)
        self._option['defaultUSDFormat'] = self._get_usd_format_(self._file_path)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

        self._results = []
    @classmethod
    def _get_usd_format_(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        if ext == '.usd':
            return 'usdc'
        elif ext == '.usda':
            return 'usda'
        raise TypeError()
    @classmethod
    def _get_usd_option_(cls, option):
        lis = []
        for k, v in option.items():
            if isinstance(v, bool):
                v = int(v)
            lis.append(';{}={}'.format(k, v))
        return ''.join(lis)
    @classmethod
    def _set_cmd_run_(cls, file_path, **kwargs):
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.file(file_path, **kwargs)

    def set_run(self):
        os_file = _utl_dcc_obj_storage.OsFile(self._file_path)
        os_file.set_directory_create()
        #
        usd_option = self._get_usd_option_(self._option)
        kwargs = dict(
            type='USD Export',
            options=usd_option,
            force=1,
            preserveReferences=1,
        )
        _selected_paths = []
        if self._root is not None:
            _selected_paths = cmds.ls(selection=1, long=1) or []
            cmds.select(self._root)
            kwargs['exportSelected'] = True
        else:
            kwargs['exportAll'] = True
        #
        _ = self._set_cmd_run_(self._file_path, **kwargs)
        if _:
            self._results = [self._file_path]
        #
        if self._results:
            for i in self._results:
                utl_core.Log.set_module_result_trace(
                    'maya-usd-exporter',
                    u'file="{}"'.format(i)
                )

        if 'exportSelected' in kwargs:
            if _selected_paths:
                cmds.select(_selected_paths)
            else:
                cmds.select(clear=1)

        return self._results

    def get_outputs(self):
        return self._results


class GeometryUsdExporter1(object):
    OPTION = {}
    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root

        self._option = copy.deepcopy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

        self._results = []

    def set_run(self):
        # noinspection PyUnresolvedReferences
        from papyUsd.maya import MayaUsdExport
        root = obj_core.DccPathDagMtd.get_dag_pathsep_replace(self._root, pathsep_tgt=ma_configure.Util.OBJ_PATHSEP)
        s_r = root
        r = '|'.join(s_r.split('|')[:-1])
        MayaUsdExport.MayaUsdExport().subTree(r, s_r, self._file_path)
        #
        self._results = [self._file_path]
        if self._results:
            for i in self._results:
                utl_core.Log.set_module_result_trace(
                    'maya-usd-exporter',
                    u'file="{}"'.format(i)
                )


class GeometryUsdExporter_(object):
    OPTION = dict(
        default_prim_path=None,
        with_uv=True,
        with_mesh=True,
        root_lstrip=None,
        use_override=False,
        export_selected=False,
    )
    def __init__(self, file_path, root=None, option=None):
        self._file_path = file_path
        self._root = root

        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v

        self._results = []

    def set_run(self):
        default_prim_path = self._option.get('default_prim_path')
        use_override = self._option['use_override']
        usd_root_lstrip = self._option['root_lstrip']
        #
        if self._root.startswith('|'):
            self._root = self._root.replace('|', '/')
        root_dag_path = core_objects.ObjDagPath(self._root)
        root_mya_dag_path = root_dag_path.set_translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        mya_root = root_mya_dag_path.path
        #
        root_mya_obj = mya_dcc_objects.Group(mya_root)
        if root_mya_obj.get_is_exists() is True:
            objs = root_mya_obj.get_descendants()
            if objs:
                usd_geometry_exporter = usd_fnc_exporters.GeometryExporter(
                    file_path=self._file_path, root=self._root,
                    option=dict(
                        default_prim_path=default_prim_path
                    )
                )
                c = len(objs)
                l_p = utl_core.LogProgressRunner(maximum=c, label='geometry-usd-export')
                for obj in objs:
                    l_p.set_update()
                    obj_mya_type = obj.type
                    obj_mya_path = obj.path
                    #
                    obj_usd_path = obj_core.DccPathDagMtd.get_dag_pathsep_replace(
                        obj_mya_path, pathsep_src=ma_configure.Util.OBJ_PATHSEP
                    )
                    obj_usd_path = obj_core.DccPathDagMtd.get_dag_path_lstrip(obj_usd_path, usd_root_lstrip)
                    if obj_mya_type == ma_configure.Util.TRANSFORM_TYPE:
                        transform_mya_obj = mya_dcc_objects.Transform(obj_mya_path)
                        transform_mya_obj_opt = mya_dcc_operators.TransformOpt(transform_mya_obj)
                        transform_usd_obj_opt = usd_geometry_exporter._set_transform_obj_opt_create_(
                            obj_usd_path, use_override=use_override
                        )
                        matrix = transform_mya_obj_opt.get_matrix()
                        transform_usd_obj_opt.set_matrix(matrix)
                    elif obj_mya_type == ma_configure.Util.MESH_TYPE:
                        mesh_obj = mya_dcc_objects.Mesh(obj_mya_path)
                        if mesh_obj.get_port('intermediateObject').get() is False:
                            mesh_mya_obj_opt = mya_dcc_operators.MeshOpt(mesh_obj)
                            if mesh_mya_obj_opt.get_is_invalid() is False:
                                mesh_usd_obj_opt = usd_geometry_exporter._set_mesh_obj_opt_create_(
                                    obj_usd_path, use_override=use_override
                                )
                                mesh_usd_obj_opt.set_create(
                                    face_vertices=mesh_mya_obj_opt.get_face_vertices(),
                                    points=mesh_mya_obj_opt.get_points(),
                                    uv_maps=mesh_mya_obj_opt.get_uv_maps()
                                )
                            else:
                                utl_core.Log.set_module_error_trace(
                                    'usd-mesh-export',
                                    'obj="{}" is invalid'.format(obj.path)
                                )
                #
                l_p.set_stop()
                #
                usd_geometry_exporter.set_run()
        else:
            utl_core.Log.set_module_warning_trace(
                'maya-usd-export',
                'obj="{}" is non-exists'.format(self._root)
            )


class DatabaseGeometryExport(object):
    OPTION = dict(
        force=False
    )
    def __init__(self, option=None):
        self._results = []
        self._errors = []
        self._warnings = []
        #
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                self._option[k] = v
        #
        self._selected_path = mya_dcc_objects.Selection.get_selected_paths(include=['mesh'])

    def _set_uv_map_export_run_(self):
        if self._selected_path:
            gp = utl_core.GuiProgressesRunner(maximum=len(self._selected_path))
            for path in self._selected_path:
                gp.set_update()
                mesh = mya_dcc_objects.Mesh(path)
                mesh_opt = mya_dcc_operators.MeshOpt(mesh)
                if mesh_opt.get_shell_count() == 1:
                    uv_maps = mesh_opt.get_uv_maps()
                    key = mesh_opt.get_face_vertices_as_uuid()
                    if bsc_core.DatabaseGeometryUvMapMtd.set_value(
                        key=key,
                        value=uv_maps,
                        force=self._option['force']
                    ) is True:
                        utl_core.Log.set_module_result_trace(
                            '{}'.format(self.__class__.__name__),
                            'obj="{}"'.format(mesh.path)
                        )
                else:
                    utl_core.Log.set_module_warning_trace(
                        '{}'.format(self.__class__.__name__),
                        'obj="{}" shell is more than "one"'.format(mesh.path)
                    )
            gp.set_stop()

    def set_run(self):
        self._set_uv_map_export_run_()
