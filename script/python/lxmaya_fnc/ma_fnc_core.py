# coding:utf-8
from lxutil_fnc import utl_fnc_abstract

from lxmaya_fnc import ma_fnc_configure

import lxbasic.objects as bsc_objects


class CheckerCreator(utl_fnc_abstract.AbsTaskMethodCreator):
    METHODS_CONFIGURE = ma_fnc_configure.Scheme.CHECKER_CONFIGURES
    #
    APPLICATION_NAME = 'maya'
    METHOD_MODULE_PATH = 'lxmaya_fnc.checker'
    def __init__(self, fnc_scn_isp_paths):
        super(CheckerCreator, self).__init__(fnc_scn_isp_paths)


class CheckerLoader(utl_fnc_abstract.AbsCheckerLoader):
    METHODS_CONFIGURE = ma_fnc_configure.Scheme.CHECKER_CONFIGURES
    def __init__(self, *args):
        super(CheckerLoader, self).__init__(*args)


class ExporterConfigure(utl_fnc_abstract.AbsExporterConfigure):
    CONFIGURE_CLASS = bsc_objects.Configure
    #
    PROPERTIES_CLASS = bsc_objects.Properties
    #
    METHODS_CONFIGURE_PATH = ma_fnc_configure.Scheme.EXPORTERS_CONFIGURE_PATH
    def __init__(self, *args):
        super(ExporterConfigure, self).__init__(*args)


class StpLoader(utl_fnc_abstract.AbsStpLoader):
    STEPS_SCHEME = ma_fnc_configure.Scheme.STEPS
    def __init__(self, *args):
        super(StpLoader, self).__init__(*args)


class LookContent(object):
    KEYS_FORMAT = '{}.{}.keys.{}.{}'
    VALUES_FORMAT = '{}.{}.values.{}.{}'
    def __init__(self, raw):
        self._raw_content = bsc_objects.Properties(None, raw)
    # key
    def set_name_key(self, look, var, seq, key):
        content_key_path = self.KEYS_FORMAT.format(look, var, ma_fnc_configure.Look.NAME, key)
        self._raw_content.set(content_key_path, seq)

    def set_points_uuid_key(self, look, var, seq, key):
        content_key_path = self.KEYS_FORMAT.format(look, var, ma_fnc_configure.Look.POINTS_UUID, key)
        self._raw_content.set(content_key_path, seq)

    def set_face_vertices_uuid_key(self, look, var, seq, key):
        content_key_path = self.KEYS_FORMAT.format(look, var, ma_fnc_configure.Look.FACE_VERTICES_UUID, key)
        self._raw_content.set(content_key_path, seq)
    # value
    def set_type_value(self, look, var, seq, value):
        content_key_path = self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.TYPE)
        self._raw_content.set(content_key_path, value)

    def set_path_value(self, look, var, seq, value):
        content_key_path = self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.PATH)
        self._raw_content.set(content_key_path, value)

    def set_material_assigns_value(self, look, var, seq, value):
        content_key_path = self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.MATERIAL_ASSIGNS)
        self._raw_content.set(content_key_path, value)

    def set_properties_value(self, look, var, seq, value):
        content_key_path = self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.PROPERTIES)
        self._raw_content.set(content_key_path, value)

    def set_visibilities_value(self, look, var, seq, value):
        content_key_path = self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.VISIBILITIES)
        self._raw_content.set(content_key_path, value)

    def set_uv_maps_value(self, look, var, seq, value):
        content_key_path = self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.UV_MAPS)
        self._raw_content.set(content_key_path, value)
    # get
    def get_material_assigns(self, look, var, key_dict):
        for key_type in ma_fnc_configure.Look.SEARCH_ORDER:
            if key_type in key_dict:
                key = key_dict[key_type]
                content_key_path = self.KEYS_FORMAT.format(look, var, key_type, key)
                seq = self._raw_content.get(content_key_path)
                if seq is not None:
                    return self._raw_content.get(
                        self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.MATERIAL_ASSIGNS)
                    )

    def get_properties(self, look, var, key_dict):
        for key_type in ma_fnc_configure.Look.SEARCH_ORDER:
            if key_type in key_dict:
                key = key_dict[key_type]
                content_key_path = self.KEYS_FORMAT.format(look, var, key_type, key)
                seq = self._raw_content.get(content_key_path)
                if seq is not None:
                    return self._raw_content.get(
                        self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.PROPERTIES)
                    )

    def get_visibilities(self, look, var, key_dict):
        for key_type in ma_fnc_configure.Look.SEARCH_ORDER:
            if key_type in key_dict:
                key = key_dict[key_type]
                content_key_path = self.KEYS_FORMAT.format(look, var, key_type, key)
                seq = self._raw_content.get(content_key_path)
                if seq is not None:
                    return self._raw_content.get(
                        self.VALUES_FORMAT.format(look, var, seq, ma_fnc_configure.Look.VISIBILITIES)
                    )
    #
    def get_raw(self):
        return self._raw_content.value
