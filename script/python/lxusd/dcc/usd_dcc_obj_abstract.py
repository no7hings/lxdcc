# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, UsdGeom

from lxbasic import bsc_core

from lxutil import utl_core

from lxusd import usd_configure

from lxuniverse import unr_configure

import lxuniverse.abstracts as unr_abstracts


class AbsUsdObjScene(unr_abstracts.AbsObjScene):
    FILE_CLASS = None
    UNIVERSE_CLASS = None
    def __init__(self):
        super(AbsUsdObjScene, self).__init__()
        self._usd_stage = None
    @property
    def usd_stage(self):
        return self._usd_stage

    def set_restore(self):
        self._universe = self.UNIVERSE_CLASS()
        self._path_lstrip = None
        #
        self._usd_stage = None

    def set_load_from_file(self, file_path, root=None):
        file_obj = self.FILE_CLASS(file_path)
        if file_obj.get_is_exists() is True:
            file_ext = file_obj.ext
            if file_ext in ['.abc']:
                self._set_load_by_dot_abc_(file_obj, root)
            elif file_ext in ['.usd', '.usda']:
                self._set_load_by_dot_usd_(file_obj, root)

    def set_load_from_dot_abc(self, file_path, root=None):
        file_obj = self.FILE_CLASS(file_path)
        self._set_load_by_dot_abc_(file_obj, root=root)

    def set_load_from_dot_usd(self, file_path, root=None):
        file_obj = self.FILE_CLASS(file_path)
        self._set_load_by_dot_usd_(file_obj, root=root)

    def _set_load_by_dot_abc_(self, file_obj, root=None):
        self.set_restore()
        file_path = file_obj.path
        self._usd_stage = Usd.Stage.CreateInMemory()
        self._root = root
        #
        usd_root = self._usd_stage.GetPseudoRoot()
        if self._root is not None:
            dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(self._root, pathsep=usd_configure.Obj.PATHSEP)
            if dag_path_comps:
                dag_path_comps.reverse()
            for i in dag_path_comps:
                if i != usd_configure.Obj.PATHSEP:
                    usd_root = self._usd_stage.DefinePrim(i, '')
        #
        usd_root.GetReferences().AddReference('{}'.format(file_path), root.GetPath())
        self._usd_stage.Flatten()
        # base, ext = os.path.splitext(file_path)
        # self._usd_stage.Export('{}.usda'.format(base))

        for i_usd_prim in self._usd_stage.TraverseAll():
            self._set_obj_create_(i_usd_prim)

    def _set_load_by_dot_usd_(self, file_obj, root=None):
        self.set_restore()
        file_path = file_obj.path
        self._usd_stage = Usd.Stage.CreateInMemory()
        self._root = root
        #
        usd_root = self._usd_stage.GetPseudoRoot()
        if self._root is not None:
            dag_path_comps = bsc_core.DccPathDagMtd.get_dag_component_paths(self._root, pathsep=usd_configure.Obj.PATHSEP)
            if dag_path_comps:
                dag_path_comps.reverse()
            for i in dag_path_comps:
                if i != usd_configure.Obj.PATHSEP:
                    usd_root = self._usd_stage.DefinePrim(i, '')
        #
        usd_root.GetReferences().AddReference('{}'.format(file_path), usd_root.GetPath())
        self._usd_stage.Flatten()
        utl_core.Log.set_module_result_trace(
            'build universe',
            'file="{}"'.format(file_path)
        )
        with utl_core.GuiProgressesRunner.create(maximum=len([i for i in self._usd_stage.TraverseAll()]), label='build universe') as l_p:
            for i_usd_prim in self._usd_stage.TraverseAll():
                l_p.set_update()
                self._set_obj_create_(i_usd_prim)

    def _set_obj_create_(self, usd_prim):
        obj_category_name = unr_configure.ObjCategory.USD
        obj_type_name = usd_prim.GetTypeName()
        obj_path = usd_prim.GetPath().pathString
        #
        obj_category = self.universe.set_obj_category_create(obj_category_name)
        obj_type = obj_category.set_type_create(obj_type_name)
        _obj = obj_type.set_obj_register(obj_path)
        _obj._usd_obj = usd_prim
        return _obj
