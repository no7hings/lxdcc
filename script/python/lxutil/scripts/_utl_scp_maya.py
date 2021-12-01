# coding:utf-8
import glob

import os

import fnmatch

import parse

import copy

import yaml

project_name = 'cg7'


class RigReader(object):
    def __init__(self, asset_name):
        self._format_dict = dict(
            project_name=project_name,
            role_name='chr',
            step_name='rig',
            task_name='rigging',
            asset_name=asset_name,
            version='*'
        )
        self._scene_file_path_pattern = (
            '/l/prod/{project_name}/publish/assets/{role_name}/{asset_name}/{step_name}'
            '/{task_name}/{asset_name}.{step_name}.{task_name}.{version}/maya/{asset_name}.ma'
        )
        #
        self._set_run_()

    def _set_run_(self):
        self._set_file_raw_update_()
        self._set_line_raw_update_()
        self._set_mesh_raw_update_()
        return self._mesh_paths

    def _set_file_raw_update_(self):
        self._file_path = None
        glob_pattern = self._scene_file_path_pattern.format(**self._format_dict)
        _ = glob.glob(
            glob_pattern
        )
        if _:
            _.sort()
            self._file_path = _[-1]
        else:
            print u'Warning: asset "{}" is Non-exists'.format(
                self._format_dict['asset_name']
            )

    def _set_line_raw_update_(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                raw = f.read()
                sep = r';{}'.format(os.linesep)
                self._lines = [r'{}{}'.format(i, sep) for i in raw.split(sep)]

    def _set_mesh_raw_update_(self):
        self._mesh_path_dict_0 = {}
        self._mesh_path_dict_1 = {}
        self._mesh_paths = []
        if self._lines:
            parse_pattern = 'createNode mesh -n "{shape_name}" -p "{transform_name}";\n'
            filter_pattern = 'createNode mesh -n "*" -p "*";\n'
            _ = fnmatch.filter(self._lines, filter_pattern)
            if _:
                for line in _:
                    line_index = self._lines.index(line)
                    is_intermediate_object = self._get_is_attr_match_(line_index, 'io', 'yes')
                    if is_intermediate_object is False:
                        p = parse.parse(
                            parse_pattern, line
                        )
                        if p:
                            transform_name = p['transform_name']
                            shape_name = p['shape_name']
                            mesh_path = self._get_mesh_path_(transform_name, shape_name)
                            self._mesh_paths.append(mesh_path)
                            #
                            key_0 = mesh_path.split('/')[-2]
                            self._mesh_path_dict_0[key_0] = mesh_path
                            #
                            key_1 = mesh_path.split('/')[-1]
                            self._mesh_path_dict_1[key_1] = mesh_path

    def _get_is_attr_match_(self, line_index, attr_name, attr_value):
        def _rcs_fnc(line_index_):
            _next_line_index = line_index_ + 1
            line_raw = self._lines[_next_line_index]
            if fnmatch.filter([line_raw], filter_pattern):
                return True
            else:
                for custom_pattern in custom_patterns:
                    if fnmatch.filter([line_raw], custom_pattern):
                        return _rcs_fnc(_next_line_index)
                return False
        #
        custom_patterns = [
            '*rename -uid *',
            '*setAttr -k *',
            '*setAttr *'
        ]
        filter_pattern = '*setAttr ".{}" {};\n'.format(attr_name, attr_value)
        return _rcs_fnc(line_index)

    def _get_mesh_path_(self, transform_name, shape_name):
        def _rcs_fnc(name_):
            result_0 = fnmatch.filter(self._lines, match_pattern_0.format(name_))
            if result_0:
                p_0 = parse.parse(
                    parse_pattern_0, result_0[0]
                )
                if p_0:
                    path_args.append(p_0['name'])
                    _rcs_fnc(p_0['parent_name'])
            else:
                result_1 = fnmatch.filter(self._lines, match_pattern_1.format(name_))
                if result_1:
                    p_1 = parse.parse(
                        parse_pattern_1, result_1[0]
                    )
                    if p_1:
                        path_args.append(p_1['name'])

        path_args = [shape_name]
        parse_pattern_0 = 'createNode transform -n "{name}" -p "{parent_name}";\n'
        match_pattern_0 = 'createNode transform -n "{}" -p "*";\n'
        #
        parse_pattern_1 = 'createNode transform -n "{name}";\n'
        match_pattern_1 = 'createNode transform -n "{}";\n'
        _rcs_fnc(transform_name)
        #
        path_args.reverse()
        return '/' + '/'.join(path_args)

    def _test(self):
        pass
    @property
    def mesh_path_dict_0(self):
        return self._mesh_path_dict_0
    @property
    def mesh_path_dict_1(self):
        return self._mesh_path_dict_1


class SceneReader(object):
    def __init__(self, file_path):
        self._lines = []
        if os.path.exists(file_path):
            with open(file_path) as f:
                raw = f.read()
                sep = r';{}'.format(os.linesep)
                self._lines = [r'{}{}'.format(i, sep) for i in raw.split(sep)]

    def get_reference_raws(self):
        lis = []
        if self._lines:
            parse_format = '{extra_0} -rdi 1 -ns "{namespace}" -rfn "{reference_node_name}"{extra_1}-typ "{extra_2}"{extra_3}"{reference_file_path}";{extra_4}'
            pattern = '*file -rdi 1 -ns "*" -rfn "*"*-typ "*"*"*";*'
            results = fnmatch.filter(self._lines, pattern)
            if results:
                results.sort()
                for i in results:
                    p = parse.parse(
                        parse_format, i
                    )
                    if p:
                        lis.append(p.named)
        return lis


class ShotReader(object):
    def __init__(self, shot_name):
        self._step_names = [
            'rlo',
            'ani',
            'flo'
        ]
        self._format_dict = dict(
            project_name=project_name,
            sequence_name='*',
            step_name='*',
            task_name='*',
            shot_name=shot_name,
            version='*'
        )
        self._scene_file_path_pattern = (
            '/l/prod/{project_name}/publish/shots/{sequence_name}/{shot_name}/{step_name}'
            '/{task_name}/{shot_name}.{step_name}.{task_name}.{version}/scene/{shot_name}.ma'
        )
        self._manifest_file_path_pattern = (
            '/l/prod/{project_name}/publish/shots/{sequence_name}/{shot_name}/{step_name}'
            '/{task_name}/{shot_name}.{step_name}.{task_name}.{version}/manifest/{shot_name}.guess.yml'
        )
        #
        self._set_run_()

    def _set_run_(self):
        self._set_file_raw_update_()

    def _set_file_raw_update_(self):
        self._scene_file_paths = []
        self._manifest_file_paths = []
        for step_name in self._step_names:
            step_format_dict = copy.deepcopy(self._format_dict)
            step_format_dict['step_name'] = step_name
            glob_pattern = self._scene_file_path_pattern.format(**step_format_dict)
            _ = glob.glob(
                glob_pattern
            )
            _ = glob.glob(
                glob_pattern
            )
            if _:
                _.sort()
                for scene_file_path in _:
                    p = parse.parse(
                        self._scene_file_path_pattern, scene_file_path
                    )
                    if p:
                        format_dict = copy.deepcopy(self._format_dict)
                        for k, v in p.named.items():
                            format_dict[k] = v
                        #
                        self._scene_file_paths.append(scene_file_path)
                        manifest_file_path = self._manifest_file_path_pattern.format(**format_dict)
                        self._manifest_file_paths.append(manifest_file_path)

    def set_manifest_create(self, scene_file_path):
        if scene_file_path in self._scene_file_paths:
            index = self._scene_file_paths.index(scene_file_path)
            manifest_file_path = self._manifest_file_paths[index]
            b = ManifestBuilder(scene_file_path, manifest_file_path)
            b.set_run()
    @property
    def scene_file_paths(self):
        return self._scene_file_paths


class ManifestBuilder(object):
    def __init__(self, scene_file_path, manifest_file_path):
        self._format_dict = dict(
            project_name=project_name,
        )
        self._scene_file_path = scene_file_path
        self._manifest_file_path = manifest_file_path
        #
        self._asset_path_format = '{extra_0}/prod/{project_name}/publish/assets/{role_name}/{asset_name}/{step_name}/{extra_1}'
        self._scheme_path_dict = dict(
            sot_cmr='{extra_0}/prod/{project_name}/publish/assets/cam/{asset_name}/rig/{extra_1}',
            sot_anm='{extra_0}/prod/{project_name}/publish/assets/{role_name}/{asset_name}/{step_name}/{extra_1}'
        )
        self._scheme_key_path_dict = dict(
            sot_cmr='current.cam.{asset_name}.{namespace}.shot_camera_cache@var.publish_path',
            sot_anm='current.{role_name}.{asset_name}.{namespace}.shot_alembic_cache@var.publish_path'
        )
    @classmethod
    def _set_manifest_raw_update_(cls, manifest_raw, key_path, value):
        def rcs_fnc_(dict_, key_):
            if key_ not in dict_:
                _index = keys.index(key_)
                if _index == max_index:
                    _sub_dict = value
                else:
                    _sub_dict = {}
                dict_[key_] = _sub_dict
            else:
                _sub_dict = dict_[key_]
            return _sub_dict

        keys = key_path.split('.')
        max_index = len(keys) - 1
        sub_dict = manifest_raw
        for key in keys:
            sub_dict = rcs_fnc_(sub_dict, key)

    def _set_run_(self):
        manifest_raw = {}
        r = SceneReader(self._scene_file_path)
        reference_raws = r.get_reference_raws()
        for reference_raw in reference_raws:
            reference_file_path = reference_raw['reference_file_path']
            asset_path_format = self._asset_path_format
            format_dict = {}
            p = parse.parse(
                asset_path_format, reference_file_path
            )
            if p is None:
                continue
            format_dict['namespace'] = reference_raw['namespace']
            for ik, iv in p.named.items():
                format_dict[ik] = iv
            #
            role_name = format_dict['role_name']
            if role_name == 'cam':
                key_path_format = self._scheme_key_path_dict['sot_cmr']
            else:
                key_path_format = self._scheme_key_path_dict['sot_anm']
            #
            key_path = key_path_format.format(**format_dict)
            value = 'placeholder'
            #
            self._set_manifest_raw_update_(manifest_raw, key_path, value)
        #
        if manifest_raw:
            f = self._manifest_file_path
            if os.path.exists(f) is False:
                d = os.path.dirname(f)
                if os.path.exists(d) is False:
                    os.makedirs(d)
                with open(f, 'w') as yw:
                    yaml.dump(
                        manifest_raw, yw,
                        indent=4,
                        default_flow_style=False,
                        default_style=None,
                        canonical=False
                    )

    def set_run(self):
        self._set_run_()
