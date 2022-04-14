# coding:utf-8
from lxbasic import bsc_core

from lxutil.dcc import utl_dcc_opt_abs

import lxbasic.objects as bsc_objects


class AndShaderOpt(utl_dcc_opt_abs.AbsObjOpt):
    def __init__(self, *args, **kwargs):
        super(AndShaderOpt, self).__init__(*args, **kwargs)
        
    def get_type_name(self):
        return self._obj.get_port('nodeType').get()

    def set_type_name(self, obj_type_name):
        self._obj.get_port('nodeType').set(obj_type_name)
        self._obj.ktn_obj.checkDynamicParameters()

    def set_create(self, obj_type_name):
        ktn_obj, is_create = self._obj.get_dcc_instance('ArnoldShadingNode')
        self._obj.get_port('nodeType').set(obj_type_name)
        self._obj.ktn_obj.checkDynamicParameters()
        return is_create

    def get_enable_port(self, and_port_path):
        return self._obj.get_port(
            'parameters.{}.enable'.format(and_port_path)
        )

    def get_value_port(self, and_port_path):
        return self._obj.get_port(
            'parameters.{}.value'.format(and_port_path)
        )

    def get_port_value(self, and_port_path):
        port = self.get_value_port(and_port_path)
        if port:
            return port.get()

    def set_port_value(self, and_port_path, value):
        self.get_enable_port(and_port_path).set(True)
        self.get_value_port(and_port_path).set(value)

    def set(self, key, value):
        self.set_port_value(key, value)

    def set_colour_by_type_name(self):
        type_name = self.get_type_name()
        r, g, b = bsc_core.TextOpt(type_name).to_rgb(maximum=1)
        attributes = self._obj.ktn_obj.getAttributes()
        attributes['ns_colorr'] = r
        attributes['ns_colorg'] = g
        attributes['ns_colorb'] = b
        self._obj.ktn_obj.setAttributes(attributes)

    def set_duplicate_with_source(self):
        print self.get_properties()
        # source_objs = self._obj.get_all_source_objs()
        # for source_obj in source_objs:
        #     print source_obj.get_properties()

    def get_properties(self):
        properties = bsc_objects.Properties(self)
        properties.set(
            'type', self.get_type_name(),
        )
        properties.set(
            'path', self._obj.path,
        )
        attributes = self._obj.get_attributes()
        properties.set(
            'attributes', attributes.value
        )
        return properties

    def get_ports(self):
        return self._obj.get_port('parameters').get_children()

    def get_attributes(self):
        attributes = bsc_objects.Properties(self)
        ports = self.get_ports()
        for port in ports:
            enable_port = port.get_child('enable')
            value_port = port.get_child('value')
            if enable_port is not None:
                attributes.set(
                    enable_port.port_path, enable_port.get()
                )
                attributes.set(
                    value_port.port_path, value_port.get()
                )
        return attributes

    def get_port_source(self, and_port_path):
        return self._obj.get_input_port(and_port_path).get_source()

    def set_port_source(self, and_port_path, source, validation=False):
        self._obj.get_input_port(and_port_path).set_source(source, validation)

    def set_port_source_disconnect(self, and_port_path):
        self._obj.get_input_port(and_port_path).set_disconnect()

    def get_port_targets(self, and_port_path):
        return self._obj.get_output_port(and_port_path).get_targets()

    def set_port_target(self, and_port_path, target, validation=False):
        self._obj.get_output_port(and_port_path).set_target(target, validation)

    def set_port_targets_disconnect(self, and_port_path):
        self._obj.get_output_port(and_port_path).set_disconnect()
