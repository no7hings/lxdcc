# coding:utf-8
import six

import yaml

import collections

import lxuniverse.abstracts as unr_abstracts

from lxutil import utl_configure, utl_core

from lxutil.dcc.dcc_objects import _utl_dcc_obj_utility


class AbsTaskMethodCreator(object):
    CONFIGURE_CLASS = None
    METHODS_CONFIGURE = None
    METHODS_CONFIGURE_PATH = None
    #
    APPLICATION_NAME = None
    METHOD_MODULE_PATH = None
    def __init__(self, method_keys):
        self._method_keys = method_keys
        self._method_dict = collections.OrderedDict()
    @property
    def application_name(self):
        return self.APPLICATION_NAME

    def get_method_keys(self):
        return self._method_keys

    def set_method(self, method_key, method):
        self._method_dict[method_key] = method

    def get_method(self, method_key):
        return self._method_dict[method_key]

    def set_methods_create(self):
        return [self._set_method_create_(i) for i in self.get_method_keys() if i]
    # noinspection PyUnusedLocal
    def _set_method_create_(self, method_key, *args):
        sub_paths = method_key.split('/')
        class_name = '_'.join(sub_paths)
        module_path = ''.join([self.METHOD_MODULE_PATH, '.'.join(sub_paths)])
        format_dict = {
            'module_path': module_path,
            'class_name': class_name
        }
        # noinspection PyBroadException
        cmd = 'from {module_path} import Method; method = Method(method_key, *args)'.format(**format_dict)
        method = None
        exec cmd
        return method


class AbsFncLoaderDef(object):
    # noinspection PyUnusedLocal
    def _set_fnc_loader_def_init_(self, configure):
        self._configure = configure
        #
        self._language = 'eng'
        self._enable = True
        # ui
        self._icon = self.configure.get('icon')
        self._label = self.configure.get('label')
        #
        self._description = self.configure.get('description')
        # python
        self._command = self.configure.get('command')
        self._method = self.configure.get('method')
    @property
    def configure(self):
        return self._configure
    @property
    def key(self):
        return self.configure.key
    @property
    def enable(self):
        return self._enable
    @property
    def language(self):
        return self._language
    # ui
    @property
    def icon(self):
        return self._icon
    @property
    def label(self):
        if isinstance(self._label, six.string_types):
            return self._label
        elif isinstance(self._label, dict):
            return self._label.keys()[0]
        return ''
    @label.setter
    def label(self, raw):
        self._label = raw
    @property
    def description(self):
        if isinstance(self._description, six.string_types):
            return self._description
        elif isinstance(self._description, dict):
            return self._description.keys()[0]
        return ''
    #
    @property
    def command(self):
        return self._command
    @property
    def method(self):
        return self._method

    def __str__(self):
        return '{}(key="{}")'.format(
            self.__class__.__name__,
            self.key
        )

    def __repr__(self):
        return self.__str__()


class AbsCheckerLoader(AbsFncLoaderDef):
    METHODS_CONFIGURE = None
    METHODS_CONFIGURE_PATH = None
    def __init__(self, method_key):
        super(AbsCheckerLoader, self).__init__()
        configure = self.METHODS_CONFIGURE.get_content(method_key)
        self._set_fnc_loader_def_init_(configure)
        #
        self._descriptions = self.configure.get('descriptions')
    @property
    def descriptions(self):
        return self._descriptions
    @descriptions.setter
    def descriptions(self, raw):
        if isinstance(raw, (tuple, list)):
            self._descriptions = raw
        elif isinstance(raw, six.string_types):
            _ = yaml.load(
                raw
            )
            if isinstance(_, (tuple, list)):
                self._descriptions = _

    def get_description_keys(self):
        lis = []
        value = self._descriptions
        for i in value:
            if isinstance(i, six.string_types):
                lis.append(i)
            elif isinstance(i, dict):
                lis.append(i.keys()[0])
        return lis

    def get_description_key_at(self, index):
        return self.get_description_keys()[index]

    def get_gui_descriptions(self):
        lis = []
        _ = self._descriptions or []
        for index in range(len(_)):
            lis.append(self.get_gui_description_at(index))
        return u'\n'.join(lis)

    def get_gui_description_at(self, index):
        lis = []
        _ = self._descriptions
        raw = _[index]
        if isinstance(raw, six.string_types):
            lis.append(
                '{}.{}'.format(index + 1, raw)
            )
        elif isinstance(raw, dict):
            key = raw.keys()[0]
            value = raw.values()[0]
            lis.append(
                '{}.{}'.format(index + 1, key)
            )
            content = self.configure._set_content_create_(key, value)
            #
            notes = content.get('notes')
            if isinstance(notes, (tuple, list)):
                lis.append(u'    - Note(s):')
                [lis.append(u'        {}'.format(i)) for i in notes]
            repair_description = content.get('repair.description')
            if repair_description is not None:
                lis.append(
                    u'    - Repair-description: {}'.format(repair_description)
                )
            ignore_enable = content.get('ignore.enable')
            if ignore_enable is not None:
                lis.append(
                    u'    - Ignore-enable: {}'.format(ignore_enable)
                )
        return u'\n'.join(lis)

    def get_ignore_enable_at(self, index):
        _ = self._descriptions
        raw = _[index]
        if isinstance(raw, dict):
            key = raw.keys()[0]
            value = raw.values()[0]
            content = self.configure._set_content_create_(key, value)
            ignore_enable = content.get('ignore.enable')
            if ignore_enable is not None:
                return ignore_enable
            return True
        return True

    def get_ignore_value_at(self, index):
        _ = self._descriptions
        raw = _[index]
        if isinstance(raw, dict):
            key = raw.keys()[0]
            value = raw.values()[0]
            content = self.configure._set_content_create_(key, value)
            ignore_enable = content.get('ignore.value')
            if ignore_enable is not None:
                return ignore_enable
            return False
        return False


class AbsStpLoader(object):
    STEPS_SCHEME = None
    def __init__(self, method_key):
        self._scheme = self.STEPS_SCHEME.get_content(method_key)
    @classmethod
    def get_key(cls, properties):
        project = properties.get('project')
        branch = properties.get('branch')
        step = properties.get('step')
        task = properties.get('task')
        task_key = '{}/{}/{}'.format(branch, step, task)
        if cls.STEPS_SCHEME.get(task_key) is not None:
            return task_key
        step_key = '{}/{}'.format(branch, step)
        if cls.STEPS_SCHEME.get(step_key) is not None:
            return step_key
        branch_key = branch
        if cls.STEPS_SCHEME.get(branch_key) is not None:
            return branch_key
        return 'project'
    @property
    def scheme(self):
        return self._scheme

    def get_checker_keys(self):
        return self.get_keys('checker')

    def get_exporter_keys(self):
        return self.get_keys('exporter')

    def get_keys(self, method_type):
        keys = self.scheme.get(method_type)
        return self.STEPS_SCHEME.set_variant_convert(keys) or []


# inspection object definition
class AbsIspObjDef(object):
    FNC_ISP_IGNORE_CLASS = None
    #
    FNC_OBJ_CLASS = _utl_dcc_obj_utility.Obj
    def _set_isp_obj_def_init_(self):
        self._error_obj_raw_dict = {}
        #
        self._is_check_passed = False
        self._is_check_ignored = False
    @property
    def loader(self):
        raise NotImplementedError()
    @property
    def error_object_raw_dict(self):
        return self._error_obj_raw_dict

    def set_error_obj_raw_add(self, error_obj, check_index):
        if isinstance(error_obj, six.string_types):
            error_obj = self.FNC_OBJ_CLASS(error_obj)
        #
        obj_path = error_obj.path
        obj_is_ignored = self._get_object_is_ignored_at_(error_obj, check_index)
        error_raw = error_obj, check_index, obj_is_ignored
        if obj_path in self.error_object_raw_dict:
            raw = self.error_object_raw_dict[obj_path]
        else:
            raw = {}
            self.error_object_raw_dict[obj_path] = raw
        #
        if error_raw not in raw:
            raw[check_index] = error_obj, obj_is_ignored

    def set_error_obj_update(self, is_error, error_obj, check_index):
        if is_error is True:
            self.set_error_obj_raw_add(error_obj, check_index)

    def get_error_object_raw(self, obj_path):
        return self.error_object_raw_dict.get(obj_path) or []

    def get_object_check_method(self, check_index):
        check_method_key = u'_check_method_{}'.format(check_index)
        if hasattr(self, check_method_key) is True:
            return self.__getattribute__(check_method_key)

    def get_object_repair_method(self, check_index):
        repair_method_key = u'_repair_method_{}'.format(check_index)
        if hasattr(self, repair_method_key) is True:
            return self.__getattribute__(repair_method_key)

    def _set_object_ignore_at_(self, obj, check_index, boolean):
        ignore_enable = self.loader.get_ignore_enable_at(check_index)
        if ignore_enable is True:
            if hasattr(obj, 'get_port') is True:
                port = obj.get_port(utl_configure.Port.VALIDATION_IGNORES)
                if port:
                    if port.get_is_exists() is False:
                        port.set_create(raw_type='string')
                    if port.get_is_exists() is True:
                        raw = port.get()
                        validation_ignore = self.FNC_ISP_IGNORE_CLASS(raw)
                        validation_ignore.set(self.loader.key, check_index, boolean)
                        port.set(validation_ignore.raw_string)
                        #
                        obj_path = obj.path
                        _ = self._get_object_is_ignored_at_(obj, check_index)
                        self.error_object_raw_dict[obj_path][check_index] = obj, _
                        return _
                    return False
        return False

    def _get_object_is_ignored_at_(self, obj, check_index):
        is_isp_ignore = self.loader.get_ignore_value_at(check_index)
        if is_isp_ignore is True:
            return True
        if hasattr(obj, 'get_port') is True:
            port = obj.get_port(utl_configure.Port.VALIDATION_IGNORES)
            if port:
                if port.get_is_exists() is False:
                    return False
                else:
                    raw = port.get()
                    validation_ignore = self.FNC_ISP_IGNORE_CLASS(raw)
                    return validation_ignore.get(self.loader.key, check_index)
        return False

    def _set_check_result_update_(self):
        isp_is_passed = True
        isp_is_ignored = False
        for k, v in self.error_object_raw_dict.items():
            for obj, obj_is_ignored in v.values():
                if obj_is_ignored is True:
                    isp_is_ignored = True
                    continue
                else:
                    isp_is_passed = False
                    break

        self._is_check_passed = isp_is_passed
        self._is_check_ignored = isp_is_passed is True and isp_is_ignored is True

    def get_is_check_passed(self):
        return self._is_check_passed

    def get_is_check_ignored(self):
        return self._is_check_ignored


# inspection object with component definition
class AbsIspObjCompDef(object):
    FNC_OBJ_CLASS = _utl_dcc_obj_utility.Obj
    def _set_isp_obj_component_def_init_(self):
        self._error_obj_comp_raw_dict = {}

    def set_error_obj_raw_add(self, error_obj, check_index):
        raise NotImplementedError
    @property
    def error_object_component_raw_dict(self):
        return self._error_obj_comp_raw_dict

    def set_error_obj_comp_raw_add(self, obj_path, check_index, error_comp):
        error_raw = error_comp, check_index
        if obj_path in self.error_object_component_raw_dict:
            error_raws = self.error_object_component_raw_dict[obj_path]
        else:
            error_raws = []
            self.error_object_component_raw_dict[obj_path] = error_raws
        #
        if error_raw not in error_raws:
            error_raws.append(error_raw)

    def set_error_obj_comps_update(self, obj, check_index, error_obj_comps):
        if error_obj_comps:
            self.set_error_obj_raw_add(obj, check_index)
            #
            obj_path = obj.path
            for sub_obj in error_obj_comps:
                if isinstance(sub_obj, six.string_types):
                    sub_obj = self.FNC_OBJ_CLASS(sub_obj)
                self.set_error_obj_comp_raw_add(
                    obj_path, check_index, sub_obj
                )
            return True
        return False

    def get_error_obj_comp_raw_at(self, obj_path):
        return self.error_object_component_raw_dict.get(obj_path) or []


# inspection object with file definition
class AbsIspObjFileDef(object):
    def _set_isp_obj_source_def_init_(self):
        self._error_obj_file_raw_dict = {}

    def set_error_obj_raw_add(self, error_obj, check_index):
        raise NotImplementedError
    @property
    def error_object_file_raw_dict(self):
        return self._error_obj_file_raw_dict

    def set_error_obj_file_raw_add(self, obj_path, check_index, error_file):
        error_raw = error_file, check_index
        if obj_path in self.error_object_file_raw_dict:
            error_raws = self.error_object_file_raw_dict[obj_path]
        else:
            error_raws = []
            self.error_object_file_raw_dict[obj_path] = error_raws
        #
        if error_raw not in error_raws:
            error_raws.append(error_raw)

    def set_error_obj_files_update(self, obj, check_index, error_obj_files):
        if error_obj_files:
            self.set_error_obj_raw_add(obj, check_index)
            #
            obj_path = obj.path
            for sub_obj in error_obj_files:
                self.set_error_obj_file_raw_add(
                    obj_path, check_index, sub_obj
                )
            return True
        return False

    def get_error_object_file_raw(self, obj_path):
        return self.error_object_file_raw_dict.get(obj_path) or []


# inspection object with source definition
class AbsIspObjSourceDef(object):
    def _set_isp_obj_source_def_init_(self):
        self._error_obj_source_raw_dict = {}

    def set_error_obj_raw_add(self, error_obj, check_index):
        raise NotImplementedError
    @property
    def error_object_source_raw_dict(self):
        return self._error_obj_source_raw_dict

    def set_error_obj_source_raw_add(self, obj_path, check_index, error_node):
        error_raw = error_node, check_index
        if obj_path in self.error_object_source_raw_dict:
            error_raws = self.error_object_source_raw_dict[obj_path]
        else:
            error_raws = []
            self.error_object_source_raw_dict[obj_path] = error_raws
        #
        if error_raw not in error_raws:
            error_raws.append(error_raw)

    def set_error_obj_sources_update(self, obj, check_index, error_obj_sources):
        if error_obj_sources:
            self.set_error_obj_raw_add(obj, check_index)
            #
            obj_path = obj.path
            for sub_obj in error_obj_sources:
                self.set_error_obj_source_raw_add(
                    obj_path, check_index, sub_obj
                )
            return True
        return False

    def get_error_object_source_raw(self, obj_path):
        return self.error_object_source_raw_dict.get(obj_path) or []


# inspection
class AbsChecker(
    AbsIspObjDef,
    AbsIspObjCompDef,
    AbsIspObjFileDef,
    AbsIspObjSourceDef
):
    FNC_CHECKER_LOADER_CLASS = None
    #
    EXCEPT_DCC_PATHS = []
    def __init__(self, method_key, *args):
        self.op_isp_loader = self.FNC_CHECKER_LOADER_CLASS(
            method_key
        )
        #
        self._is_repairable = False
        #
        self._set_isp_obj_def_init_()
        self._set_isp_obj_component_def_init_()
        self._set_isp_obj_source_def_init_()
        self._set_isp_obj_source_def_init_()
        #
        self._error_obj_source_raw_dict = {}
    @property
    def icon(self):
        return None
    @property
    def loader(self):
        return self.op_isp_loader

    def get_error_description_at(self, index):
        raw = self.loader.get_description_key_at(index)
        return raw.format(**self._format_dict_())

    def set_restore(self):
        self._error_objs = []
        self._error_obj_raw_dict = {}
        #
        self._error_obj_comp_raw_dict = {}
        self._error_obj_file_raw_dict = {}
        self._error_obj_source_raw_dict = {}
        #
        self._is_check_passed = False

    def _set_objs_check_(self, objs, include_indices=None):
        """
        :param objs: list(instance(obj))
        :param include_indices: list(int(index), ...) or None
        :return: None
        """
        for obj in objs:
            for check_index, error_description in enumerate(self.loader.get_description_keys()):
                # include filter
                if include_indices is not None:
                    if check_index not in include_indices:
                        continue
                #
                check_method = self.get_object_check_method(check_index)
                if check_method is not None:
                    _results = check_method(obj, check_index)
                else:
                    utl_core.Log.set_error_trace(
                        u"\"{}\" check method is Non-exists".format(self.loader.label)
                    )

        self._set_check_result_update_()

    def set_check_run(self):
        raise NotImplementedError()

    def set_repair_run(self):
        self._set_objs_repair_()

    def _set_objs_repair_(self, include_indices=None):
        for k, v in self.error_object_raw_dict.items():
            for check_index, (obj, obj_is_ignored) in v.items():
                if obj_is_ignored is True:
                    continue
                # include filter
                if include_indices is not None:
                    if check_index not in include_indices:
                        continue
                repair_method = self.get_object_repair_method(check_index)
                if repair_method is not None:
                    repair_method(obj)
                else:
                    utl_core.Log.set_error_trace(
                        u"\"{}\" repair method is Non-configure".format(self.loader.label)
                    )

    def _format_dict_(self):
        return {
            'self': self,
            'configure': self.loader.configure,
            'include_paths': '; '.join(['"{}"'.format(i) for i in self.EXCEPT_DCC_PATHS])
        }


class AbsConfigureDef(
    unr_abstracts.AbsObjDef,
    unr_abstracts.AbsObjDagDef,
    unr_abstracts.AbsObjGuiDef
):
    PATHSEP = '/'
    PROPERTIES_CLASS = None
    def _set_configure_def_init_(self, key, raw):
        self._key = key
        self._properties = self.PROPERTIES_CLASS(key, raw)
        #
        path = self.get('path')
        self._set_obj_dag_def_init_(path)
        self._set_obj_def_init_(
            self._get_obj_name_(path)
        )
        self._set_obj_gui_def_init_()
    #
    @property
    def key(self):
        return self._key
    @property
    def properties(self):
        return self._properties

    def get(self, key):
        return self._properties.get(key)
    #
    @property
    def pathsep(self):
        return self.PATHSEP
    @property
    def type(self):
        return self.get('type')
    #
    @property
    def icon(self):
        icon_name = self.get('icon')
        return utl_core.Icon.get(icon_name)
    @property
    def label(self):
        return self.get('label')
    @property
    def description(self):
        _ = self.get('description')
        if isinstance(_, (tuple, list)):
            return u';\n'.join(_) + u'.'
        return str(_)

    def _set_dag_create_(self, path):
        pass

    def _get_child_paths_(self, *args, **kwargs):
        pass

    def _set_child_create_(self, path):
        pass


class AbsTaskMethodConfigure(AbsConfigureDef):
    CONFIGURE_CLASS = None
    #
    METHODS_CONFIGURE_PATH = None
    def __init__(self, key):
        methods_configure = self.CONFIGURE_CLASS(None, self.METHODS_CONFIGURE_PATH)
        methods_configure.set_flatten()
        value = methods_configure.get(key)
        if value is None:
            value = methods_configure.get('/null')
            value['path'] = key
        self._set_configure_def_init_(key, value)

    def _set_dag_create_(self, path):
        return self.__class__(path)


class AbsExporterConfigure(AbsTaskMethodConfigure):
    def __init__(self, key):
        super(AbsExporterConfigure, self).__init__(key)


class AbsTaskMethod(object):
    METHOD_CONFIGURE_CLASS = None
    def __init__(self, key):
        self._configure = self.METHOD_CONFIGURE_CLASS(key)
    @property
    def configure(self):
        return self._configure


class AbsTaskExporter(AbsTaskMethod):
    def __init__(self, key, task_properties):
        super(AbsTaskExporter, self).__init__(key)
        self._task_properties = task_properties
        self._is_check_passed = False
    @property
    def task_properties(self):
        return self._task_properties

    def get_is_check_passed(self):
        return self._is_check_passed

    def set_check_run(self):
        self._is_check_passed = True

    def set_export_run(self):
        raise NotImplementedError()
