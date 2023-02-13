# coding:utf-8
from lxobj import obj_configure, obj_abstract


class AbsObjScene(obj_abstract.AbsObjScene):
    CONFIGURE_CLASS = None
    def __init__(self):
        super(AbsObjScene, self).__init__()

    def set_restore(self):
        self._universe = self.UNIVERSE_CLASS()

    def set_load_from_configure(self, file_path):
        file_obj = self.FILE_CLASS(file_path)
        self._set_load_by_configure_(file_obj)

    def set_load_from_configure_(self, file_path):
        file_obj = self.FILE_CLASS(file_path)
        self._set_load_by_configure__(file_obj)

    def _set_load_by_configure__(self, file_obj):
        def rcs_fnc_(dic_):
            for k, v in dic_.items():
                if k == 'properties':
                    _obj_properties = v
                    _obj_path = v.get('obj_path')
                    if _obj_path:
                        _obj_type_name = v.get('obj_type')
                        _obj_attributes = v.get('obj_attributes')
                        self._set_obj_create_(_obj_type_name, _obj_path, _obj_properties, _obj_attributes)
                else:
                    rcs_fnc_(v)
        #
        self.set_restore()
        #
        file_path = file_obj.path
        configure = self.CONFIGURE_CLASS(None, file_path)
        configure.set_flatten()
        rcs_fnc_(configure.get('methods'))

    def _set_load_by_configure_(self, file_obj):
        pass

    def _set_obj_create_(self, obj_type_name, obj_path, obj_properties, obj_attributes=None):
        obj_category_name = obj_configure.ObjCategory.LYNXI
        obj_category = self.universe.set_obj_category_create(obj_category_name)
        obj_type = obj_category.set_type_create(obj_type_name)
        obj = obj_type.set_obj_create(obj_path)
        #
        if isinstance(obj_properties, dict):
            obj.properties = obj_properties
        #
        if isinstance(obj_attributes, dict):
            obj.attributes = obj_attributes
            obj.gui_attributes = obj_attributes['gui']
