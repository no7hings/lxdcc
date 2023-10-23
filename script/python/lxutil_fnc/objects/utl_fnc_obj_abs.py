# coding:utf-8
import six

import collections

from lxbasic import bsc_core

import lxcontent.objects as ctt_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil_fnc.dcc.dcc_objects as utl_fnc_dcc_objects


class AbsTaskMethodsLoader(object):
    CONFIGURE_CLS = None
    METHODS_CONFIGURE_PATH = None

    def __init__(self, task_properties, options=None):
        self._task_properties = task_properties
        self._configure = self.CONFIGURE_CLS(None, self.METHODS_CONFIGURE_PATH)
        #
        if isinstance(options, dict):
            for k, v in options.items():
                self._configure.set('option.{}'.format(k), v)
        #
        self._configure.set_flatten()
        #
        self._obj_scene = utl_fnc_dcc_objects.Scene()
        self._obj_scene.set_load_from_configure_(self.METHODS_CONFIGURE_PATH)
        self._obj_universe = self._obj_scene.universe
        #
        self._set_step_mapper_build_()

    @property
    def task_properties(self):
        return self._task_properties

    @property
    def obj_scene(self):
        return self._obj_scene

    @property
    def obj_universe(self):
        return self._obj_universe

    def _set_step_mapper_build_(self):
        self._step_mapper_dict = {}
        _ = self._configure.get('option.step_mapper')
        for k, v in _.items():
            for i in v:
                self._step_mapper_dict[i] = k

    def get_entity_method_obj_paths(self, entity_path):
        application = self.task_properties.get('application')
        key_path = 'entities{}.properties.method.{}'.format(
            '.'.join(entity_path.split('/')), application
        )
        method_paths = self._configure.get(key_path) or []
        return method_paths

    def get_entity_obj_path(self):
        task_properties = self._task_properties
        #
        branch = task_properties.get('branch')
        step = task_properties.get('step')
        step = self._step_mapper_dict.get(step, step)
        task = task_properties.get('task')
        _ = 'entities.project.{}.{}.{}'.format(branch, step, task)
        if self._configure.get(_) is not None:
            return '/'+'/'.join(_.split('.')[1:])
        _ = 'entities.project.{}.{}'.format(branch, step)
        if self._configure.get(_) is not None:
            return '/'+'/'.join(_.split('.')[1:])
        _ = 'entities.project.{}'.format(branch)
        if self._configure.get(_) is not None:
            return '/'+'/'.join(_.split('.')[1:])
        _ = 'entities.project'
        return '/'+'/'.join(_.split('.')[1:])

    def get_root_obj(self):
        return self.obj_universe.get_root()

    def get_obj(self, method_path):
        return self.obj_universe.get_obj(method_path)

    def get_module(self, method_path):
        obj = self.get_obj(method_path)
        if obj:
            application = self.task_properties.get('application')
            obj_attributes = obj.attributes
            module_path = obj_attributes.get('method.{}.module'.format(application))
            if module_path:
                module = bsc_core.PyModule(module_path)
                module.set_reload()
                return module

    def get_method_cls(self, method_path):
        module = self.get_module(method_path)
        if module:
            method_cls = module.get_method('Method')
            return method_cls

    def get_method(self, method_path):
        method_cls = self.get_method_cls(method_path)
        if method_cls is not None:
            method = method_cls(self._task_properties)
            method.obj = self.get_obj(method_path)
            return method

    def get_sorted_objs(self, method_paths):
        import copy

        lis = copy.deepcopy(method_paths)
        application = self.task_properties.get('application')
        for method_path in method_paths:
            obj = self.get_obj(method_path)
            obj_attributes = obj.attributes
            dependent_method_paths = obj_attributes.get('method.{}.dependent'.format(application)) or []
            if dependent_method_paths:
                for seq, dependent_method_path in enumerate(dependent_method_paths):
                    index = lis.index(method_path)
                    if dependent_method_path in lis:
                        sub_index = lis.index(dependent_method_path)
                        if sub_index > index:
                            lis.remove(dependent_method_path)
                            lis.insert(index-seq, dependent_method_path)
                    else:
                        bsc_core.Log.trace_method_warning(
                            'method-sorted',
                            'method-path="{}" from dependent(s) is non-assign'.format(dependent_method_path)
                        )
        return lis


class AbsMethodDef(object):
    def _set_method_def_init_(self):
        self._obj = None
        self._obj_attribute = None

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, obj):
        self._obj = obj

    @property
    def obj_attributes(self):
        return self._obj.attributes

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self.obj.path
        )


class AbsMethodCheckDef(object):
    FNC_ISP_IGNORE_CLS = None
    #
    DCC_NODE_CLS = utl_dcc_objects.Obj
    CONTENT_CLS = ctt_objects.Content

    def _set_method_check_def_init_(self):
        self._error_obj_content = self.CONTENT_CLS(
            value=collections.OrderedDict()
        )
        #
        self._check_tags = []
        self._is_check_passed = False
        self._is_check_ignored = False

    @property
    def obj(self):
        raise NotImplementedError()

    @property
    def obj_attributes(self):
        raise NotImplementedError()

    @property
    def check_results(self):
        return self._error_obj_content

    def set_obj_check_result_at(self, obj_path, check_tag, index, description=None):
        self.check_results.set(
            u'{}.{}.check_tag'.format(obj_path, index), check_tag
        )
        if description is not None:
            self.check_results.set(
                u'{}.{}.description'.format(obj_path, index), check_tag
            )

    def get_obj_check_tags(self, obj_path):
        check_tags_ = []
        indexes = self.check_results.get_branch_keys(obj_path)
        for index in indexes:
            i_check_tag = self.check_results.get(
                u'{}.{}.check_tag'.format(obj_path, index)
            )
            if i_check_tag not in check_tags_:
                check_tags_.append(i_check_tag)
        return '+'.join(check_tags_)

    def set_obj_files_check_result_at(self, obj_path, file_paths, check_tag, index):
        self.set_obj_check_result_at(obj_path, check_tag, index)
        #
        self.check_results.set(
            u'{}.{}.files'.format(obj_path, index), file_paths
        )

    def get_obj_files_check_result_at(self, obj_path, index):
        return self.check_results.get(
            u'{}.{}.files'.format(obj_path, index)
        ) or []

    def set_obj_comps_check_result_at(self, obj_path, comp_names, check_tag, index):
        self.set_obj_check_result_at(obj_path, check_tag, index)
        self.check_results.set(
            u'{}.{}.comps'.format(obj_path, index), comp_names
        )

    def get_obj_comps_check_result_at(self, obj_path, index):
        return self.check_results.get(
            u'{}.{}.comps'.format(obj_path, index)
        ) or []

    def get_check_description_at(self, index):
        obj_attributes = self.obj_attributes
        if obj_attributes is not None:
            _ = obj_attributes.get('method.check.description.index_{}'.format(index))
            if isinstance(_, six.string_types):
                return _
            elif isinstance(_, (tuple, list)):
                return u','.join(_)
        return u''

    def get_check_label(self):
        obj_attributes = self.obj_attributes
        return obj_attributes.get('method.check.label')

    def get_check_descriptions(self):
        descriptions = []
        obj_attributes = self.obj_attributes
        index_keys = obj_attributes.get_branch_keys('method.check.description')
        for seq, index_key in enumerate(index_keys):
            _ = obj_attributes.get('method.check.description.{}'.format(index_key))
            if isinstance(_, six.string_types):
                i_descriptions = _
            elif isinstance(_, (tuple, list)):
                i_descriptions = u','.join(_)
            else:
                i_descriptions = ''
            #
            descriptions.append(u'{}.{}'.format(seq+1, i_descriptions))
        return u'\n'.join(descriptions)

    def get_export_descriptions(self):
        descriptions = []
        obj_attributes = self.obj_attributes
        index_keys = obj_attributes.get_branch_keys('method.export.description')
        for seq, index_key in enumerate(index_keys):
            _ = obj_attributes.get('method.export.description.{}'.format(index_key))
            if isinstance(_, six.string_types):
                i_descriptions = _
            elif isinstance(_, (tuple, list)):
                i_descriptions = u','.join(_)
            else:
                i_descriptions = ''
            #
            descriptions.append(u'{}.{}'.format(seq+1, i_descriptions))
        return u'\n'.join(descriptions)

    def get_export_label(self):
        obj_attributes = self.obj_attributes
        return obj_attributes.get('method.export.label')

    def get_obj_check_description(self, obj_path):
        indexes = self.check_results.get_branch_keys(obj_path)
        lis = []
        for index in indexes:
            _ = self.get_check_description_at(index)
            if _:
                lis.append(_)
        return u';'.join(lis)

    def get_obj_paths(self):
        return self.check_results.get_branch_keys()

    def get_obj_file_paths(self, obj_path):
        pass

    def get_obj_descriptions(self):
        lis = []
        for obj_path, v in self.check_results.value.items():
            description = self.get_obj_check_description(obj_path)
            lis.append(u'obj="{}"\ndescription="{}"'.format(obj_path, description))
        return '\n'.join(lis)

    #
    def get_object_check_method(self, index):
        check_method_key = u'_check_method_{}'.format(index)
        if hasattr(self, check_method_key) is True:
            return self.__getattribute__(check_method_key)

    def get_object_repair_method(self, index):
        repair_method_key = u'_repair_method_{}'.format(index)
        if hasattr(self, repair_method_key) is True:
            return self.__getattribute__(repair_method_key)

    def set_check_run(self):
        raise NotImplementedError()

    def _set_check_debug_run_(self):
        # noinspection PyBroadException
        try:
            self.set_check_run()
        except Exception:
            from lxbasic import bsc_core
            bsc_core.LogException.trace()
            raise

    def set_check_result_update(self, task_properties):
        check_tags_ = []
        for obj_path, v in self.check_results.value.items():
            for index, check_content in v.items():
                i_check_tag = check_content['check_tag']
                if not i_check_tag in check_tags_:
                    check_tags_.append(i_check_tag)
        #
        bsc_core.Log.trace_method_result(
            'method-check-result-update',
            u'method-path="{}"'.format(self.obj.path)
        )
        #
        if not check_tags_:
            self._check_tags = 'passed'
        else:
            self._check_tags = '+'.join(check_tags_)
        #
        self._is_check_passed = 'error' not in self._check_tags
        self._is_check_ignored = False
        #
        task_properties.set(
            'method.{}.check.check_tag'.format(self.obj.path),
            self._check_tags
        )

    def set_check_rest(self):
        self._check_tags = 'error'
        self._is_check_passed = False
        self._is_check_ignored = False
        #
        self._error_obj_content = self.CONTENT_CLS(
            value=collections.OrderedDict()
        )

    def get_check_tags(self):
        return self._check_tags

    def get_is_check_passed(self):
        return self._is_check_passed

    def get_is_check_ignored(self):
        return self._is_check_ignored


class AbsMethodRepairDef(object):
    def _set_method_repair_def_init_(self):
        pass

    def set_repair_run(self):
        pass

    def _set_repair_debug_run_(self):
        # noinspection PyBroadException
        try:
            self.set_repair_run()
        except Exception:
            from lxbasic import bsc_core
            bsc_core.LogException.trace()
            raise

    def set_repair_result_update(self, task_properties):
        pass


class AbsMethodExportDef(object):
    def _set_method_export_def_init_(self):
        pass

    def set_export_run(self):
        raise NotImplementedError()

    def _set_export_pre_run_(self):
        pass

    def _set_export_post_run_(self):
        pass

    def _set_export_debug_run_(self, use_window=True):
        # noinspection PyBroadException
        try:
            self._set_export_pre_run_()
            #
            self.set_export_run()
            #
            self._set_export_post_run_()
        #
        except Exception:
            from lxbasic import bsc_core
            bsc_core.LogException.trace()
            raise

    def set_export_result_update(self, task_properties):
        pass


class AbsTaskMethod(
    AbsMethodDef,
    AbsMethodCheckDef,
    AbsMethodRepairDef,
    AbsMethodExportDef
):
    def __init__(self, task_properties):
        self._set_method_def_init_()
        self._set_method_check_def_init_()
        self._set_method_repair_def_init_()
        self._set_method_export_def_init_()
        #
        self._task_properties = task_properties

    @property
    def task_properties(self):
        return self._task_properties

    @task_properties.setter
    def task_properties(self, raw):
        self._task_properties = raw

    def set_check_run(self):
        raise NotImplementedError()

    def set_export_run(self):
        raise NotImplementedError()
