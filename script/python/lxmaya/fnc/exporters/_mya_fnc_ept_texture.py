# coding:utf-8
import copy

import lxobj.objects as core_objects

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.dcc.dcc_operators as mya_dcc_operators

from lxutil.fnc import utl_fnc_obj_abs

from lxmaya import ma_configure


class TextureExporter(
    utl_fnc_obj_abs.AbsDccTextureExport,
    utl_fnc_obj_abs.AbsFncOptionMethod,
):
    OPTION = dict(
        directory_base='',
        directory='',
        location='',
        fix_name_blank=False,
        use_tx=False,
        width_reference=False,
        use_environ_map=False,
    )
    #
    def __init__(self, option=None):
        super(TextureExporter, self).__init__(option)
        self._directory_path_dst = self.get('directory')
        self._directory_path_base = self.get('directory_base')
        self._location = self.get('location')

    def set_run(self):
        root_dag_path = core_objects.ObjDagPath(self._location)
        root_mya_dag_path = root_dag_path.set_translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        #
        root_mya_obj = mya_dcc_objects.Group(root_mya_dag_path.path)
        if root_mya_obj.get_is_exists() is True:
            dcc_geometries = root_mya_obj.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(dcc_geometries)
            includes = objs_look_opt.get_texture_reference_paths()
            if includes:
                texture_references = mya_dcc_objects.TextureReferences
                #
                self._set_copy_as_src_(
                    directory_path_dst=self._directory_path_dst,
                    directory_path_base=self._directory_path_base,
                    dcc_objs=texture_references._get_objs_(includes),
                    #
                    fix_name_blank=self.get('fix_name_blank'),
                    use_tx=self.get('use_tx'),
                    with_reference=self.get('width_reference'),
                    #
                    ignore_missing_texture=True,
                    use_environ_map=self.get('use_environ_map'),
                    #
                    repath_fnc=texture_references.set_obj_repath_to
                )
