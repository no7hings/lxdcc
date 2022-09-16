# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds, mel

import copy

import os

from lxmaya import ma_configure, ma_core

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxmaya.fnc import mya_fnc_obj_core

import lxusd.dcc.dcc_operators as usd_dcc_operators

from lxusd import usd_configure, usd_core

from lxutil import utl_core

from lxutil.fnc import utl_fnc_obj_abs

from lxbasic import bsc_core


class GeometryUsdImporter_(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        uv_map_file=None,
        root_override=None,
        #
        port_match_patterns=[]
    )
    PLUG_NAME = None
    OBJ_PATHSEP = ma_configure.Util.OBJ_PATHSEP
    def __init__(self, file_path, root=None, option=None):
        super(GeometryUsdImporter_, self).__init__(file_path, root, option)
        #
        self._usd_stage_opt = usd_core.UsdStageOpt()
        self._usd_stage = self._usd_stage_opt.usd_instance
        #
        if bsc_core.StoragePathOpt(self._file_path).get_is_file() is True:
            self._usd_stage_opt.set_sublayer_append(self._file_path)
            uv_map_file_path = self._option.get('uv_map_file')
            if uv_map_file_path is not None:
                self._usd_stage_opt.set_sublayer_prepend(uv_map_file_path)
            #
            self._usd_stage.Flatten()
        else:
            utl_core.Log.set_module_warning_trace(
                '{}'.format(self.__class__.__name__),
                'file="{}" is non-exist'.format(self._file_path)
            )

    def set_run(self):
        c = len([i for i in self._usd_stage.TraverseAll()])
        if c:
            root_override = self._option['root_override']
            if root_override is not None:
                self._set_path_create_(root_override)
            #
            with utl_core.log_progress_bar(maximum=c, label='usd import') as l_p:
                for i_usd_prim in self._usd_stage.TraverseAll():
                    l_p.set_update()
                    i_usd_prim_type_name = i_usd_prim.GetTypeName()
                    if i_usd_prim_type_name == usd_configure.ObjType.TRANSFORM:
                        mya_fnc_obj_core.FncUsdTransform(i_usd_prim, location=root_override).set_create()
                    elif i_usd_prim_type_name == usd_configure.ObjType.MESH:
                        mya_fnc_obj_core.FncUsdMesh(i_usd_prim, location=root_override).set_create()
    @classmethod
    def _set_path_create_(cls, path):
        dag_path = bsc_core.DccPathDagOpt(path)
        paths = dag_path.get_component_paths()
        if paths:
            paths.reverse()
            for i_path in paths:
                if i_path != '/':
                    cls._set_transform_create_by_path_(i_path)

    def set_meshes_uv_maps_import_run(self, uv_map_face_vertices_contrast=True):
        for i_usd_prim in self._usd_stage.TraverseAll():
            i_usd_prim_type_name = i_usd_prim.GetTypeName()
            if i_usd_prim_type_name == usd_configure.ObjType.MESH:
                self._set_mesh_uv_maps_(
                    i_usd_prim,
                    uv_map_face_vertices_contrast=uv_map_face_vertices_contrast
                )
    @classmethod
    def _set_transform_create_by_path_(cls, path, matrix=None):
        dag_path = bsc_core.DccPathDagOpt(path)
        mya_dag_path = dag_path.set_translate_to(cls.OBJ_PATHSEP)
        mya_obj = mya_dcc_objects.Transform(mya_dag_path.path)
        if mya_obj.get_is_exists() is False:
            mya_obj_opt = mya_dcc_operators.TransformOpt(mya_obj)
            if mya_obj_opt.set_create() is True:
                if matrix is not None:
                    mya_obj_opt.set_matrix(matrix)
    @classmethod
    def _set_mesh_uv_maps_(cls, prim, uv_map_face_vertices_contrast=True):
        obj_path = prim.GetPath().pathString
        usd_dag_path = bsc_core.DccPathDagOpt(obj_path)
        mya_dag_path = usd_dag_path.set_translate_to(cls.OBJ_PATHSEP)
        #
        mya_obj_path = mya_dag_path.path
        mya_obj = mya_dcc_objects.Node(mya_obj_path)
        if mya_obj.get_is_exists() is True:
            if mya_obj.type == 'mesh':
                mesh_mya_obj_opt = mya_dcc_operators.MeshOpt(mya_obj)
                mesh_usd_obj_opt = usd_dcc_operators.MeshOpt(prim)
                #
                face_vertices_uuid_src = mesh_usd_obj_opt.get_face_vertices_as_uuid()
                face_vertices_uuid_tgt = mesh_mya_obj_opt.get_face_vertices_as_uuid()
                if face_vertices_uuid_src == face_vertices_uuid_tgt:
                    uv_maps = mesh_usd_obj_opt.get_uv_maps()
                    if uv_maps:
                        if uv_map_face_vertices_contrast is True:
                            uv_map_face_vertices_uuid_src = mesh_usd_obj_opt.get_uv_map_face_vertices_as_uuid()
                            uv_map_face_vertices_uuid_tgt = mesh_mya_obj_opt.get_uv_map_face_vertices_as_uuid()
                            if uv_map_face_vertices_uuid_src == uv_map_face_vertices_uuid_tgt:
                                # noinspection PyArgumentEqualDefault
                                mesh_mya_obj_opt.set_uv_maps(uv_maps, clear=False)
                            else:
                                utl_core.Log.set_module_warning_trace(
                                    'uv-map(s)-import',
                                    'obj="{}" uv-map-face-vertices is changed'.format(obj_path)
                                )
                        else:
                            uv_map_face_vertices_uuid_src = mesh_usd_obj_opt.get_uv_map_face_vertices_as_uuid()
                            uv_map_face_vertices_uuid_tgt = mesh_mya_obj_opt.get_uv_map_face_vertices_as_uuid()
                            clear = uv_map_face_vertices_uuid_src != uv_map_face_vertices_uuid_tgt
                            mesh_mya_obj_opt.set_uv_maps(uv_maps, clear=clear)
                    else:
                        utl_core.Log.set_module_warning_trace(
                            'uv-map(s)-import',
                            'obj="{}" uv-map is non-exists'.format(obj_path)
                        )
                else:
                    utl_core.Log.set_module_warning_trace(
                        'uv-map(s)-import',
                        'obj="{}" face-vertices is changed'.format(obj_path)
                    )
        else:
            utl_core.Log.set_module_warning_trace(
                'uv-map(s)-import',
                'obj="{}" is non-exists'.format(obj_path)
            )


class GeometryUsdImporter0(object):
    """
-apiSchema	-api	string (multi)	none	Imports the given API schemas' attributes as Maya custom attributes. This only recognizes API schemas that have been applied to prims on the stage. The attributes will properly round-trip if you re-export back to USD.
-chaser	-chr	string(multi)	none	Specify the import chasers to execute as part of the export. See "Import Chasers" below.
-chaserArgs	-cha	string[3] multi	none	Pass argument names and values to import chasers. Each argument to -chaserArgs should be a triple of the form: (<chaser name>, <argument name>, <argument value>). See "Import Chasers" below.
-excludePrimvar	-epv	string (multi)	none	Excludes the named primvar(s) from being imported as color sets or UV sets. The primvar name should be the full name without the primvars: namespace prefix.
-file	-f	string	none	Name of the USD being loaded
-frameRange	-fr	float float	none	The frame range of animations to import
-importInstances	-ii	bool	true	Import USD instanced geometries as Maya instanced shapes. Will flatten the scene otherwise.
-metadata	-md	string (multi)	hidden, instanceable, kind	Imports the given USD metadata fields as Maya custom attributes (e.g. USD_hidden, USD_kind, etc.) if they're authored on the USD prim. The metadata will properly round-trip if you re-export back to USD.
-parent	-p	string	none	Name of the Maya scope that will be the parent of the imported data.
-primPath	-pp	string	none (defaultPrim)	Name of the USD scope where traversing will being. The prim at the specified primPath (including the prim) will be imported. Specifying the pseudo-root (/) means you want to import everything in the file. If the passed prim path is empty, it will first try to import the defaultPrim for the rootLayer if it exists. Otherwise, it will behave as if the pseudo-root was passed in.
-preferredMaterial	-prm	string	lambert	Indicate a preference towards a Maya native surface material for importers that can resolve to multiple Maya materials. Allowed values are none (prefer plugin nodes like pxrUsdPreviewSurface and aiStandardSurface) or one of lambert, standardSurface, blinn, phong. In displayColor shading mode, a value of none will default to lambert.
-readAnimData	-ani	bool	false	Read animation data from prims while importing the specified USD file. If the USD file being imported specifies startTimeCode and/or endTimeCode, Maya's MinTime and/or MaxTime will be expanded if necessary to include that frame range. Note: Only some types of animation are currently supported, for example: animated visibility, animated transforms, animated cameras, mesh and NURBS surface animation via blend shape deformers. Other types are not yet supported, for example: time-varying curve points, time-varying mesh points/normals, time-varying NURBS surface points
-shadingMode	-shd	string[2] multi	useRegistry UsdPreviewSurface	Ordered list of shading mode importers to try when importing materials. The search stops as soon as one valid material is found. Allowed values for the first parameter are: none (stop search immediately, must be used to signal no material import), displayColor (if there are bound materials in the USD, create corresponding Lambertian shaders and bind them to the appropriate Maya geometry nodes), pxrRis (attempt to reconstruct a Maya shading network from (presumed) Renderman RIS shading networks in the USD), useRegistry (attempt to reconstruct a Maya shading network from (presumed) UsdShade shading networks in the USD) the second item in the parameter pair is a convertMaterialFrom flag which allows specifying which one of the registered USD material sources to explore. The full list of registered USD material sources can be found via the mayaUSDListShadingModesCommand command.
-useAsAnimationCache	-uac	bool	false	Imports geometry prims with time-sampled point data using a point-based deformer node that references the imported USD file. When this parameter is enabled, MayaUSDImportCommand will create a pxrUsdStageNode for the USD file that is being imported. Then for each geometry prim being imported that has time-sampled points, a pxrUsdPointBasedDeformerNode will be created that reads the points for that prim from USD and uses them to deform the imported Maya geometry. This provides better import and playback performance when importing time-sampled geometry from USD, and it should reduce the weight of the resulting Maya scene since it will bypass creating blend shape deformers with per-object, per-time sample geometry. Only point data from the geometry prim will be computed by the deformer from the referenced USD. Transform data from the geometry prim will still be imported into native Maya form on the Maya shape's transform node. Note: This means that a link is created between the resulting Maya scene and the USD file that was imported. With this parameter off (as is the default), the USD file that was imported can be freely changed or deleted post-import. With the parameter on, however, the Maya scene will have a dependency on that USD file, as well as other layers that it may reference. Currently, this functionality is only implemented for Mesh prims/Maya mesh nodes.
-verbose	-v	noarg	false	Make the command output more verbose.
-variant	-var	string[2]	none	Set variant key value pairs
-importUSDZTextures	-itx	bool	false	Imports textures from USDZ archives during import to disk. Can be used in conjuction with -importUSDZTexturesFilePath to specify an explicit directory to write imported textures to. If not specified, requires a Maya project to be set in the current context.
-importUSDZTexturesFilePath	-itf	string	none	Specifies an explicit directory to write imported textures to from a USDZ archive. Has no effect if -importUSDZTextures is not specified.
    """
    OPTION = dict()
    PLUG_NAME = 'mayaUsdPlugin'
    OBJ_PATHSEP = ma_configure.Util.OBJ_PATHSEP
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
    def _set_cmd_run_(cls, file_path, **kwargs):
        cmds.loadPlugin(cls.PLUG_NAME, quiet=1)
        return cmds.file(file_path, **kwargs)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        cmds.mayaUSDImport(
            file=self._file_path
        )


class GeometryAbcImporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        namespace=':',
        hidden=False
    )
    PLUG_NAME = 'AbcImport'
    OBJ_PATHSEP = ma_configure.Util.OBJ_PATHSEP
    def __init__(self, file_path, root=None, option=None):
        super(GeometryAbcImporter, self).__init__(file_path, root, option)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        namespace_temporary = 'alembic_import_{}'.format(utl_core.System.get_time_tag())
        root = bsc_core.DccPathDagOpt(self._root).set_translate_to(
            self.OBJ_PATHSEP
        ).path
        group = mya_dcc_objects.Group(root)
        group.set_dag_components_create()
        #
        cmds.file(
            self._file_path,
            i=1,
            options='v=0;',
            type='Alembic',
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace_temporary,
            preserveReferences=1
        )
        utl_core.Log.set_module_result_trace(
            'geometry abc import',
            'file="{}"'.format(self._file_path)
        )
        #
        hidden = self._option['hidden']
        #
        namespace_obj = mya_dcc_objects.Namespace(namespace_temporary)
        self._results = []
        objs = namespace_obj.get_objs()
        for obj in objs:
            utl_core.Log.set_module_result_trace(
                'geometry abc import',
                u'obj="{}"'.format(obj.path)
            )
            if obj.type == 'transform':
                if hidden is True:
                    obj.set_visible(False)
                #
                target_obj_path = '{}|{}'.format(
                    root,  bsc_core.DccPathDagMtd.get_dag_name_with_namespace_clear(obj.name)
                )
                if cmds.objExists(target_obj_path) is False:
                    obj.set_parent_path(root)
                else:
                    obj.set_delete()

            obj._set_path_update_()
            dcc_dag_path = bsc_core.DccPathDagOpt(obj.path).set_namespace_clear_to()
            self._results.append(dcc_dag_path.path)
        #
        namespace_obj.set_delete()
        return self._results


class GeometryXgenImporter(
    utl_fnc_obj_abs.AbsFncOptionMethod,
    utl_fnc_obj_abs.AbsDotXgenDef
):
    OPTION = dict(
        xgen_collection_file='',
        xgen_collection_directory='',
        xgen_location='',
        #
        grow_file='',
        grow_location='',
        #
        namespace=':',
    )
    PLUG_NAME = 'xgenToolkit'
    def __init__(self, option=None):
        super(GeometryXgenImporter, self).__init__(option)
    @classmethod
    def set_glow_import(cls, grow_file, grow_location):
        if isinstance(grow_file, (str, unicode)):
            file_paths = [grow_file]
        else:
            file_paths = grow_file
        #
        for i_file_path in file_paths:
            results = GeometryAbcImporter(
                file_path=i_file_path,
                root=grow_location,
                option=dict(
                    namespace=':',
                    hidden=True
                )
            ).set_run()
            if results:
                utl_core.Log.set_module_result_trace(
                    'xgen glow import',
                    u'result="{}"'.format(','.join(results))
                )
    @classmethod
    def set_xgen_import(cls, xgen_collection_file, xgen_collection_directory, xgen_location):
        # noinspection PyUnresolvedReferences
        import xgenm as xg
        # noinspection PyUnresolvedReferences
        import xgenm.xgGlobal as xgg
        #
        group = mya_dcc_objects.Group(
            bsc_core.DccPathDagOpt(xgen_location).set_translate_to('|').get_value()
        )
        group.set_dag_components_create()
        #
        if isinstance(xgen_collection_file, (str, unicode)):
            file_paths = [xgen_collection_file]
        else:
            file_paths = xgen_collection_file
        #
        namespace = ''
        for i_file_path in file_paths:
            i_xgen_collection_name = xg.importPalette(
                str(i_file_path),
                [],
                namespace
            )
            i_xgen_collection_data_directory = '{}/{}'.format(
                xgen_collection_directory, i_xgen_collection_name
            )
            cmds.xgmSetAttr(
                attribute='xgDataPath',
                object=i_xgen_collection_name,
                palette=i_xgen_collection_name,
                value=i_xgen_collection_data_directory,
            )
            for i_xgen_guide in mya_dcc_objects.Group(
                bsc_core.DccPathDagOpt(xgen_location).set_translate_to('|').value
            ).get_all_paths(include_obj_type=['xgmSplineGuide']):
                mya_dcc_objects.Node(i_xgen_guide).set('width', .01)
            #
            if ma_core._get_is_ui_mode_() is True:
                mel.eval('XgCreateDescriptionEditor;')
                de = xgg.DescriptionEditor
                de.clearCacheAction.setChecked(True)
                de.updateClearControls()
                de.previewAutoAction.setChecked(False)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        xgen_collection_file = self.get('xgen_collection_file')
        xgen_collection_directory = self.get('xgen_collection_directory')
        xgen_location = self.get('xgen_location')
        #
        grow_file = self.get('grow_file')
        grow_location = self.get('grow_location')
        if grow_file:
            self.set_glow_import(
                grow_file,
                grow_location,
            )
        #
        if xgen_collection_file:
            self.set_xgen_import(
                xgen_collection_file,
                xgen_collection_directory,
                xgen_location
            )


class DatabaseGeometryImporter(object):
    def __init__(self):
        self._selected_path = mya_dcc_objects.Selection.get_selected_paths(include=['mesh'])

    def _set_uv_map_export_import_(self):
        if self._selected_path:
            g_p = utl_core.GuiProgressesRunner(maximum=len(self._selected_path))
            for path in self._selected_path:
                g_p.set_update()
                mesh = mya_dcc_objects.Mesh(path)
                mesh_opt = mya_dcc_operators.MeshOpt(mesh)
                if mesh_opt.get_shell_count() == 1:
                    key = mesh_opt.get_face_vertices_as_uuid()
                    uv_maps = bsc_core.DatabaseGeometryUvMapMtd.get_value(key)
                    mesh_opt.set_uv_maps(uv_maps, clear=True)
            #
            g_p.set_stop()

    def set_run(self):
        self._set_uv_map_export_import_()

