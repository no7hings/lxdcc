# coding:utf-8
import collections

from lxarnold import and_configure


class AbsLookOpt(object):
    def __init__(self, *args):
        self._obj = args[0]
    @property
    def obj(self):
        return self._obj

    def get_material_paths(self):
        return [self.obj.get_input_port('material').get()]


class ShapeLookOpt(AbsLookOpt):
    def __init__(self, *args):
        super(ShapeLookOpt, self).__init__(*args)

    def get_material_assigns(self):
        material_assigns = collections.OrderedDict()
        material_paths = self.get_material_paths()
        if material_paths:
            for material_path in material_paths:
                material_assigns['all'] = material_path
        return material_assigns

    def get_properties(self):
        properties = collections.OrderedDict()
        obj_type_name = self.obj.type.name
        keys = and_configure.Data.OBJ_CONFIGURE.get('properties.{}'.format(obj_type_name))
        for key in keys:
            port = self.obj.get_input_port(key)
            if port is not None:
                if port.get_is_enumerate():
                    raw = port.get_as_index()
                else:
                    raw = port.get()
                properties[key] = raw
        return properties

    def set_properties_convert_to(self, application):
        dic = collections.OrderedDict()
        dic_ = self.get_properties()
        convert_dict = and_configure.Data.DCC_IMPORTER_CONFIGURE.get(
            'properties.to-{}.{}'.format(application, self.obj.type.name)
        )
        for k, v in convert_dict.items():
            if k in dic_:
                dic[v] = dic_[k]
        return dic

    def get_visibilities(self):
        visibilities = collections.OrderedDict()
        keys = and_configure.Data.OBJ_CONFIGURE.get('visibilities')
        for key in keys:
            port = self.obj.get_input_port(key)
            if port is not None:
                visibilities[key] = port.get()
        return visibilities

    def set_visibilities_convert_to(self, application):
        dic = collections.OrderedDict()
        dic_ = self.get_visibilities()
        convert_dict = and_configure.Data.DCC_IMPORTER_CONFIGURE.get(
            'visibilities.to-{}'.format(application)
        )
        for k, v in convert_dict.items():
            if k in dic_:
                dic[v] = dic_[k]
        return dic
