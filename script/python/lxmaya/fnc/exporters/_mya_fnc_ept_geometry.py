# coding:utf-8
import six
# noinspection PyUnresolvedReferences
from maya import cmds

import os

import copy

from lxbasic import bsc_core

from lxobj import obj_core

from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxmaya import ma_configure, ma_core

import lxobj.core_objects as core_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxusd import usd_core

import lxusd.fnc.exporters as usd_fnc_exporters

from lxutil.fnc import utl_fnc_obj_abs


class GeometryAbcExporter(object):
    FILE = 'file'
    FRAME_RANGE = 'frameRange'
    FRAME_RELATIVE_SAMPLE = 'frameRelativeSample'
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
    ATTR_PREFIX = 'attrPrefix'
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
    def __init__(self, file_path, root=None, frame=None, step=None, attribute=None, attribute_prefix=None, option=None, data_format=None):
        self._file_path = file_path
        #
        self._root = self._get_location_(root)
        self._star_frame, self._end_frame = mya_dcc_objects.Scene.get_frame_range(frame)
        self._step = step
        self._attribute = attribute
        self._attribute_prefix = attribute_prefix
        self._option = copy.copy(self.OPTION)
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
    def _get_location_(cls, raw):
        if raw is not None:
            if isinstance(raw, six.string_types):
                _ = [raw]
            elif isinstance(raw, (tuple, list)):
                _ = list(raw)
            else:
                raise TypeError()
            return map(lambda x: bsc_core.DccPathDagOpt(x).set_translate_to('|').to_string(), _)
        return []
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
        if isinstance(data_format, six.string_types):
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
        if isinstance(obj_path_args, six.string_types):
            if cmds.objExists(obj_path_args):
                return [cmds.ls(obj_path_args, long=1)[0]]
        elif isinstance(obj_path_args, (tuple, list)):
            return [cmds.ls(i, long=1)[0] for i in obj_path_args if cmds.objExists(i)]
    @classmethod
    def _get_strs_(cls, string, includes=None):
        lis = []
        if isinstance(string, six.string_types):
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
            _ = ' '.join(['-{0} {1}'.format(cls.ATTR, i) for i in lis])
        else:
            _ = None
        return _
    @classmethod
    def _get_attribute_prefix_(cls, attr_name):
        lis = cls._get_strs_(attr_name)
        #
        if lis:
            _ = ' '.join(['-{0} {1}'.format(cls.ATTR_PREFIX, i) for i in lis])
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
            self._get_attribute_prefix_(self._attribute_prefix),
            self._get_option_(self._option),
            self._get_data_format_(self._data_format),
            self._get_root_(self._root),
            self._get_file_(self._file_path)
        ]
        #
        file_ = utl_dcc_objects.OsFile(self._file_path)
        directory_ = file_.directory
        if directory_.get_is_exists() is False:
            directory_.set_create()
        #
        j = self._get_j_(js)
        if j:
            self._results = self._set_cmd_run_(j)
            utl_core.Log.set_module_result_trace(
                'alembic export',
                'file="{}"'.format(file_.path)
            )
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
        os_file = utl_dcc_objects.OsFile(self._file_path)
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
        with_curve=False,
        root_lstrip=None,
        use_override=False,
        export_selected=False,
        namespace_clear=True,
        with_visible=True,
        with_display_color=True,
        #
        port_match_patterns=[]
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
        with_visible = self._option['with_visible']
        with_display_color = self._option['with_display_color']
        port_match_patterns = self._option['port_match_patterns']
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
            mya_objs = root_mya_obj.get_descendants()
            if mya_objs:
                usd_geometry_exporter = usd_fnc_exporters.GeometryExporter(
                    option=dict(
                        file=self._file_path,
                        location=self._root,
                        default_prim_path=default_prim_path
                    )
                )
                c = len(mya_objs)
                l_p = utl_core.log_progress_bar(maximum=c, label='geometry-usd export')
                #
                for i_mya_obj in mya_objs:
                    l_p.set_update()
                    #
                    i_mya_obj_type = i_mya_obj.type
                    i_mya_obj_path = i_mya_obj.path
                    #
                    i_usd_obj_path = bsc_core.DccPathDagMtd.get_dag_pathsep_replace(
                        i_mya_obj_path, pathsep_src=ma_configure.Util.OBJ_PATHSEP
                    )
                    i_usd_obj_path = bsc_core.DccPathDagMtd.get_dag_path_lstrip(i_usd_obj_path, usd_root_lstrip)
                    # clean namespace
                    if ':' in i_usd_obj_path:
                        utl_core.Log.set_module_warning_trace(
                            'usd-mesh export',
                            'obj="{}" has namespace'.format(i_usd_obj_path)
                        )
                    #
                    i_usd_obj_path = bsc_core.DccPathDagMtd.get_dag_path_with_namespace_clear(
                        i_usd_obj_path
                    )
                    i_usd_obj_path = bsc_core.DccPathDagMtd.set_dag_path_cleanup(
                        i_usd_obj_path
                    )
                    if i_mya_obj_type == ma_configure.Util.TRANSFORM_TYPE:
                        transform_mya_obj = mya_dcc_objects.Transform(i_mya_obj_path)
                        transform_mya_obj_opt = mya_dcc_operators.TransformOpt(transform_mya_obj)
                        transform_usd_obj_opt = usd_geometry_exporter._set_transform_opt_create_(
                            i_usd_obj_path, use_override=use_override
                        )
                        matrix = transform_mya_obj_opt.get_matrix()
                        transform_usd_obj_opt.set_matrix(matrix)
                        #
                        if with_visible is True:
                            transform_usd_obj_opt.set_visible(
                                transform_mya_obj.get_visible()
                            )
                    #
                    elif i_mya_obj_type == ma_configure.Util.MESH_TYPE:
                        i_mya_mesh = mya_dcc_objects.Mesh(i_mya_obj_path)
                        if i_mya_mesh.get_port('intermediateObject').get() is False:
                            i_mya_mesh_opt = mya_dcc_operators.MeshOpt(i_mya_mesh)
                            if i_mya_mesh_opt.get_is_invalid() is False:
                                i_usd_mesh_opt = usd_geometry_exporter._set_mesh_opt_create_(
                                    i_usd_obj_path, use_override=use_override
                                )
                                i_usd_mesh_opt.set_create(
                                    face_vertices=i_mya_mesh_opt.get_face_vertices(),
                                    points=i_mya_mesh_opt.get_points(),
                                    uv_maps=i_mya_mesh_opt.get_uv_maps()
                                )
                                # export visibility
                                if with_visible is True:
                                    i_usd_mesh_opt.set_visible(
                                        i_mya_mesh.get_visible()
                                    )
                                # export color use name
                                if with_display_color is True:
                                    color = bsc_core.RawTextOpt(i_mya_mesh.name).to_rgb_(
                                        maximum=1
                                    )
                                    i_usd_mesh_opt.set_display_color_fill(
                                        color
                                    )
                            else:
                                utl_core.Log.set_module_error_trace(
                                    'usd-mesh export',
                                    'obj="{}" is invalid'.format(i_mya_obj.path)
                                )
                    # nurbs curve
                    elif i_mya_obj_type == ma_configure.Util.CURVE_TYPE:
                        i_mya_curve = mya_dcc_objects.Curve(i_mya_obj_path)
                        if i_mya_curve.get_port('intermediateObject').get() is False:
                            i_mya_curve_opt = mya_dcc_operators.NurbsCurveOpt(i_mya_curve)
                            if i_mya_curve_opt.get_is_invalid() is False:
                                i_usd_curve_opt = usd_geometry_exporter._set_basis_curves_create_(
                                    i_usd_obj_path, use_override=use_override
                                )
                                counts, points, widths = i_mya_curve_opt.get_usd_basis_curve_data()
                                i_usd_curve_opt.set_create(
                                    counts, points, widths
                                )
                                if with_display_color is True:
                                    color = bsc_core.RawTextOpt(i_mya_curve.name).to_rgb_(
                                        maximum=1
                                    )
                                    i_usd_curve_opt.set_display_color_fill(
                                        color
                                    )
                    # xgen description
                    elif i_mya_obj_type == ma_configure.Util.XGEN_DESCRIPTION:
                        i_mya_xgen_description = mya_dcc_objects.Shape(i_mya_obj_path)
                        i_mya_xgen_description_guide_opt = mya_dcc_operators.XgenDescriptionOpt(
                            i_mya_xgen_description
                        )
                        if i_mya_xgen_description_guide_opt.get_is_exists() is True:
                            i_usd_curve_opt = usd_geometry_exporter._set_basis_curves_create_(
                                i_usd_obj_path, use_override=use_override
                            )
                            counts, points, widths = i_mya_xgen_description_guide_opt.get_usd_basis_curve_data()
                            i_usd_curve_opt.set_create(
                                counts, points, widths
                            )
                            if with_display_color is True:
                                color = bsc_core.RawTextOpt(i_mya_xgen_description.name).to_rgb_(
                                    maximum=1
                                )
                                i_usd_curve_opt.set_display_color_fill(
                                    color
                                )

                    # xgen guide
                    # elif i_mya_obj_type == ma_configure.Util.XGEN_SPLINE_GUIDE:
                    #     i_mya_xgen_spline_guide = mya_dcc_objects.Shape(i_mya_obj_path)
                    #     i_mya_xgen_spline_guide_opt = mya_dcc_operators.XgenSplineGuideOpt(
                    #         i_mya_xgen_spline_guide
                    #     )
                    #     if i_mya_xgen_spline_guide_opt.get_is_exists() is True:
                    #         i_usd_curve_opt = usd_geometry_exporter._set_basis_curves_create_(
                    #             i_usd_obj_path, use_override=use_override
                    #         )
                    #         counts, points, widths = i_mya_xgen_spline_guide_opt.get_usd_basis_curve_data()
                    #         i_usd_curve_opt.set_create(
                    #             counts, points, widths
                    #         )
                    #         if with_display_color is True:
                    #             color = bsc_core.RawTextOpt(i_mya_xgen_spline_guide.name).to_rgb_(
                    #                 maximum=1
                    #             )
                    #             i_usd_curve_opt.set_display_color_fill(
                    #                 color
                    #             )

                    if port_match_patterns:
                        i_geometry_usd_fnc = usd_geometry_exporter._get_geometry_fnc_(i_usd_obj_path)
                        if i_geometry_usd_fnc is not None:
                            i_customize_ports = ma_core.CmdObjOpt(i_mya_obj_path).get_customize_ports()
                            for j_port in i_customize_ports:
                                if j_port.get_is_naming_matches(port_match_patterns) is True:
                                    j_key = j_port.port_path
                                    j_value = j_port.get()
                                    if j_value is None:
                                        j_value = ''
                                    usd_core.UsdPrimOpt._set_customize_attribute_add_(
                                        i_geometry_usd_fnc, j_key, j_value
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
                    if bsc_core.DtbGeometryUvMapFileMtd.set_value(
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


class CameraAbcExport(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        file='',
        location='',
        frame=(1, 1),
    )
    def __init__(self, option):
        super(CameraAbcExport, self).__init__(option)
        option = self.get_option()
        location = option.get('location')
        g = mya_dcc_objects.Group(bsc_core.DccPathDagOpt(location).set_translate_to('|').to_string())
        self._camera_shape_paths = g.get_all_shape_paths(include_obj_type='camera')
        self._camera_transform_paths = map(lambda x: mya_dcc_objects.Shape(x).transform.path, self._camera_shape_paths)

    def _set_pre_run_(self):
        for i in self._camera_shape_paths:
            i_camera_shape = mya_dcc_objects.Shape(i)
            i_camera_shape.get_port('overscan').set(1)
            #
            i_camera_shape.get_port('lx_film_fit').set_create('long')
            i_camera_shape.get_port('lx_film_fit').set(
                i_camera_shape.get_port('filmFit').get()
            )
            i_camera_shape.get_port('lx_camera_tag').set_create('string')
            i_camera_shape.get_port('lx_camera_tag').set(
                'main'
            )

    def set_run(self):
        self._set_pre_run_()
        option = self.get_option()
        GeometryAbcExporter(
            file_path=option.get('file'),
            root=self._camera_transform_paths,
            frame=option.get('frame'),
            attribute=['lx_film_fit', 'lx_camera_tag']
        ).set_run()


class GeometryUvMapUsdExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        file='',
        location='',
        root='',
        #
        display_color=(0.75, .75, 0.5),
        subdiv_dict={}
    )
    def __init__(self, option):
        super(GeometryUvMapUsdExporter, self).__init__(option)
    @classmethod
    def _set_subdiv_(cls, obj_path, subdiv_count):
        _ = cmds.listConnections(obj_path, destination=0, source=1, type='polySmoothFace')
        if _:
            ma_core.CmdObjOpt(_[0]).set('divisions', subdiv_count)
            ma_core.CmdObjOpt(_[0]).set('smoothUVs', 0)
            return _
        return cmds.polySmooth(
            obj_path,
            dv=subdiv_count,
            mth=0,
            sdt=0,
            ovb=1,
            ofb=3,
            ofc=0,
            ost=0,
            ocr=0,
            bnr=1,
            c=1,
            kb=1,
            ksb=1,
            khe=0,
            kt=1,
            kmb=1,
            suv=0,
            peh=0,
            sl=1,
            dpe=1,
            ps=0.1,
            ro=1,
            ch=1
        )
    @classmethod
    def _get_tmp_usd_file_(cls):
        user_directory_path = bsc_core.StgTmpBaseMtd.get_user_directory('usd-export')
        return '{}/{}.usd'.format(
            user_directory_path,
            bsc_core.TimestampOpt(
                bsc_core.TimeBaseMtd.get_timestamp()
            ).get_as_tag_36()
        )
    @classmethod
    def _set_tmp_usd_export_(cls, file_path, location, root):
        GeometryUsdExporter_(
            file_path=file_path,
            root=location,
            option=dict(
                default_prim_path=root,
                with_uv=True,
                with_mesh=True,
                use_override=False
            )
        ).set_run()

    def set_run(self):
        subdiv_dict = self.get('subdiv_dict')
        post_deletes = []
        if subdiv_dict:
            for k, v in subdiv_dict.items():
                i_obj_path = bsc_core.DccPathDagOpt(
                    k
                ).set_translate_to('|')
                # i_results = self._set_subdiv_(
                #     i_obj_path, v
                # )
                # post_deletes.extend(i_results)
        #
        file_path = self.get('file')
        temp_usd_file_path = self._get_tmp_usd_file_()
        location = self.get('location')
        root = self.get('root')

        self._set_tmp_usd_export_(
            temp_usd_file_path, location, root
        )

        # print temp_usd_file_path
        # temp_usd_file_path = '/l/temp/temporary/usd-export/2022_0913-dongchangbao/RI58SQ.usd'

        usd_fnc_exporters.GeometryUvMapExporter(
            file_path=file_path,
            root=root,
            option=dict(
                file_0=temp_usd_file_path,
                file_1=temp_usd_file_path,
                display_color=self.get('display_color')
            )
        ).set_run()

