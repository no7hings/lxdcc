# coding:utf-8
import fnmatch

import re

import parse

import collections

from lxdeadline import ddl_configure

from Deadline import DeadlineConnect

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects


class _Pattern(object):
    def __init__(self, pattern):
        self._pattern = pattern
        self._fnmatch_pattern = self._get_fnmatch_pattern_(self._pattern)
    @classmethod
    def _get_fnmatch_pattern_(cls, variant):
        if variant is not None:
            re_pattern = re.compile(r'[{](.*?)[}]', re.S)
            #
            keys = re.findall(re_pattern, variant)
            s = variant
            if keys:
                for key in keys:
                    s = s.replace('{{{}}}'.format(key), '*')
            return s
        return variant
    @property
    def format(self):
        return self._pattern
    @property
    def pattern(self):
        return self._fnmatch_pattern


class AbsContentRaw(object):
    SEP = '\n'
    def __init__(self, raw):
        self._raw = raw
        self._set_line_raw_update_()
    @classmethod
    def _get_lines_(cls, raw, sep):
        return [u'{}{}'.format(i, sep) for i in raw.split(sep)]
    @property
    def lines(self):
        return self._lines

    def _set_line_raw_update_(self):
        self._lines = []
        if self._raw is not None:
            raw = self._raw
            sep = self.SEP
            self._lines = self._get_lines_(raw, sep)


class DdlContentRaw(AbsContentRaw):
    SEP = '\n'
    def __init__(self, raw):
        super(DdlContentRaw, self).__init__(raw)

    def _get_stouts__(self):
        self._memories = []
        self._errors = []
        self._warnings = []
        pattern_0 = _Pattern('{time}: {index}: STDOUT: {content}')
        contents_0 = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        pattern_0_outs = []
        for i in contents_0:
            p = parse.parse(
                pattern_0.format, i
            )
            if p:
                raw = p['content']
                raw = raw.lstrip().rstrip()
                pattern_0_outs.append(raw)
        #
        pattern_1 = _Pattern('{time} {memory}MB {status} | {content}')
        contents_1 = fnmatch.filter(
            pattern_0_outs, pattern_1.pattern
        )
        pattern_1_outs = []
        for i in contents_1:
            p = parse.parse(
                pattern_1.format, i
            )
            if p:
                memory = int(p['memory'].lstrip().rstrip())
                time = p['time']
                status = p['status'].lstrip().rstrip()
                raw = p['content']
                raw = raw.lstrip().rstrip()
                pattern_1_outs.append(raw)
                if status == 'ERROR':
                    print i
                self._memories.append(memory)
        #
        pattern_2 = _Pattern('[{module}] {content}')
        contents_2 = fnmatch.filter(
            pattern_1_outs, pattern_2.pattern
        )
        for i in contents_2:
            p = parse.parse(
                pattern_2.format, i
            )
            if p:
                print p['module']

    def _get_stouts_(self, content=False):
        lis = []
        pattern_0 = _Pattern('{time}: {index}: STDOUT: {content}')
        lines = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                if content is True:
                    lis.append(p['content'] + self.SEP)
                else:
                    lis.append(line)
        return lis

    def get_stouts(self, content=False):
        _ = self._get_stouts_(content)
        if _:
            return ''.join(_)

    def _get_infos_(self, content=False):
        lis = []
        pattern_0 = _Pattern('{time}: {index}: INFO: {content}')
        lines = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                if content is True:
                    lis.append(p['content'] + self.SEP)
                else:
                    lis.append(line)
        return lis

    def get_infos(self, content=False):
        _ = self._get_infos_()
        if _:
            return ''.join(_)


class ArnoldStoutRaw(AbsContentRaw):
    SEP = '\n'
    def __init__(self, raw):
        super(ArnoldStoutRaw, self).__init__(raw)

    def _get_results_(self, status=None, keyword=None, content=False):
        lis = []
        pattern_0 = _Pattern('{time} {memory}MB {status} | {content}')
        lines = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                _content = p['content'].lstrip().rstrip()
                _status = p['status'].lstrip().rstrip()
                if status is not None:
                    if _status != status:
                        continue
                #
                if keyword is not None:
                    if keyword not in _content:
                        continue
                #
                if content is True:
                    lis.append(p['content'] + self.SEP)
                else:
                    lis.append(line)
        return lis

    def get_errors(self, keyword=None, content=False):
        _ = self._get_results_(status='ERROR', keyword=keyword, content=content)
        if _:
            return ''.join(_)

    def get_warnings(self, keyword=None, content=False):
        _ = self._get_results_(status='WARNING', keyword=keyword, content=content)
        if _:
            return ''.join(_)


class DdlConnectOpt(object):
    def __init__(self):
        self._ddl_instance = DeadlineConnect.DeadlineCon(
            ddl_configure.Util.HOST, ddl_configure.Util.PORT
        )
    @property
    def ddl_instance(self):
        return self._ddl_instance


class DdlCacheMtd(object):
    CONTENT = bsc_objects.Content(
        value=collections.OrderedDict()
    )
    #
    METHOD_PATH_PATTERN = '{type}.{name}.{engine}.{script}'
    @classmethod
    def set_ddl_job_id_add(cls, method_key, ddl_group_key, ddl_job_key, ddl_job_id):
        cls.CONTENT.add_element(
            '{}.{}.{}.job-ids'.format(method_key, ddl_group_key, ddl_job_key),
            ddl_job_id
        )
    @classmethod
    def set_ddl_method_update(cls, ddl_method_path, ddl_method):
        cls.CONTENT.add_element(
            '{}.job-ids'.format(ddl_method_path),
            ddl_method.get_ddl_job_id()
        )
    @classmethod
    def get_ddl_method_job_ids(cls, ddl_method_path):
        return cls.CONTENT.get(
            '{}.job-ids'.format(ddl_method_path)
        )
    @classmethod
    def set_ddl_rsv_task_method_update(cls, method_key, rsv_task_version, ddl_rsv_task_method):
        cls.set_ddl_job_id_add(
            method_key,
            rsv_task_version,
            cls.get_ddl_rsv_task_method_job_name(ddl_rsv_task_method),
            ddl_rsv_task_method.get_ddl_job_id()
        )
    @classmethod
    def get_ddl_rsv_task_method_job_ids(cls, method_key, rsv_task_version, ddl_job_key):
        return cls.CONTENT.get(
            '{}.{}.{}.job-ids'.format(
                method_key,
                rsv_task_version,
                ddl_job_key
            )
        )
    @classmethod
    def set_ddl_rsv_task_method_reset(cls, method_key, rsv_task_version):
        cls.CONTENT.set(
            '{}.{}'.format(method_key, rsv_task_version),
            collections.OrderedDict()
        )
    @classmethod
    def get_ddl_rsv_task_method_job_name(cls, ddl_rsv_task_method):
        return '[{}][{}]'.format(ddl_rsv_task_method.ENGINE, ddl_rsv_task_method.SCRIPT)
    @classmethod
    def get_ddl_method_option(cls):
        pass
    @classmethod
    def get_ddl_job_ids(cls, method_options):
        lis = []
        for method_option in method_options:
            job_ids = cls.get_ddl_method_job_ids(cls.get_ddl_method_path(method_option)) or []
            lis.extend(job_ids)
        return lis
    @classmethod
    def get_ddl_method_path(cls, method_option):
        return cls.METHOD_PATH_PATTERN.format(
            **bsc_core.ArgDictStringOpt(method_option).value
        )


class DdlMethodCacheOpt(object):
    METHOD_TYPE = 'method'
    METHOD_PATH_PATTERN = '{type}.{name}.{engine}.{script}'
    def __init__(self, **kwargs):
        self._path = DdlCacheMtd.get_ddl_method_path(
            kwargs['option']
        )

    def set_update(self, ddl_method):
        DdlCacheMtd.set_ddl_method_update(
            self._path,
            ddl_method
        )

    def get_job_ids(self):
        return DdlCacheMtd.get_ddl_method_job_ids(
            self._path
        )


class DdlMethodOption(object):
    @classmethod
    def get(cls, **kwargs):
        # type=method&name=database&configure=cjd&engine=houdini-python&script=set_geometry_unify_by_usd_file
        return 'type={type}&name={name}&configure={configure}&engine={engine}&script={script}&group={group}&pool={pool}'.format(
            **kwargs
        )
    @classmethod
    def get_geometry_unify(cls, configure='cjd'):
        return cls.get(
            type='method',
            name='database',
            #
            configure=configure,
            engine='houdini-python',
            script='set_geometry_unify_by_usd_file',
            #
            pool='emergency',
            group='all',
        )
    @classmethod
    def get_geometry_uv_assign(cls, configure='cjd'):
        return cls.get(
            type='method',
            name='database',
            #
            configure=configure,
            engine='houdini-python',
            script='set_geometry_uv_map_assign_by_usd_file',
            #
            pool='emergency',
            group='all',
        )


class AbsDdlRsvTaskOption(DdlMethodOption):
    @classmethod
    def _get_rsv_task_version_(cls, rsv_task_properties):
        if rsv_task_properties.get('shot'):
            return '{project}.{shot}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        elif rsv_task_properties.get('asset'):
            return '{project}.{asset}.{step}.{task}.{version}'.format(**rsv_task_properties.value)
        else:
            raise TypeError()


class DdlRsvTaskMethodOption(AbsDdlRsvTaskOption):
    TYPE = 'rsv-task-method'
    SCRIPT_OPTION_PATTERN_DICT = dict(
        maya_camera_export='file={file}&with_camera_persp_abc={with_camera_persp_abc}',
        katana_render_export='file={file}&create_scene={create_scene}'
    )
    # python
    @classmethod
    def get_python_look_preview_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='python',
            script='set_look_preview_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_method_option(cls, key):
        return
    @classmethod
    def get_script_option_pattern(cls, key):
        return cls.SCRIPT_OPTION_PATTERN_DICT[key]
    @classmethod
    def get_script_option(cls, key, **kwargs):
        return cls.SCRIPT_OPTION_PATTERN_DICT[key].format(**kwargs)
    # maya
    @classmethod
    def get_maya_scene_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_scene_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_maya_geometry_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_geometry_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_maya_look_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_look_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_maya_cfx_look_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_cfx_look_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_maya_camera_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_camera_create_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_maya_geometry_import(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_geometry_import_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_maya_look_import(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='maya',
            script='set_look_import_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    # houdini
    @classmethod
    def get_houdini_scene_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='houdini-python',
            script='set_scene_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_houdini_geometry_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='houdini-python',
            script='set_geometry_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_houdini_look_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='houdini-python',
            script='set_look_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    # katana
    @classmethod
    def get_katana_scene_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='katana-python',
            script='set_scene_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_katana_geometry_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='katana-python',
            script='set_geometry_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_katana_look_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='katana-python',
            script='set_look_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_katana_cfx_look_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='katana-python',
            script='set_cfx_look_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_katana_render_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='katana-python',
            script='set_render_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    # usd
    @classmethod
    def get_usd_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='usd',
            script='set_usd_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    # shotgun
    @classmethod
    def get_shotgun_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='shotgun',
            script='set_shotgun_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    @classmethod
    def get_shotgun_render_export(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='shotgun',
            script='set_render_export_by_any_scene_file',
            #
            pool='subprogress',
            group='subprogress',
        )
    #
    SCRIPT_METHOD_DICT = dict(
        maya_camera_expor=get_maya_camera_export
    )


class DdlRsvTaskRenderOption(AbsDdlRsvTaskOption):
    TYPE = 'rsv-task-render'
    @classmethod
    def get_katana_scene_render(cls, rsv_task_properties):
        project = rsv_task_properties.get('project')
        name = cls._get_rsv_task_version_(rsv_task_properties)
        return cls.get(
            type=cls.TYPE,
            name=name,
            #
            configure=project,
            engine='katana-render',
            script='scene_render',
            #
            pool='all',
            group='all',
        )
