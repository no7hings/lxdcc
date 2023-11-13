# coding:utf-8
import collections

import fnmatch

import parse

import re

import hashlib

import struct

import uuid

import os

import lxbasic.core as bsc_core

from lxutil import utl_core


class Uuid(object):
    BASIC = '4908BDB4-911F-3DCE-904E-96E4792E75F1'

    @classmethod
    def get_new(cls):
        return str(uuid.uuid1()).upper()

    @classmethod
    def get_by_hash_value(cls, hash_value):
        return str(uuid.uuid3(uuid.UUID(Uuid.BASIC), str(hash_value))).upper()

    @classmethod
    def get_by_string(cls, string):
        return str(uuid.uuid3(uuid.UUID(Uuid.BASIC), str(string))).upper()

    @classmethod
    def get_by_file(cls, file_path):
        if os.path.isfile(file_path):
            timestamp = os.stat(file_path).st_mtime
            return str(
                uuid.uuid3(uuid.UUID(Uuid.BASIC), 'file="{}"; timestamp={}; version=2.0'.format(file_path, timestamp))
                ).upper()
        return str(uuid.uuid3(uuid.UUID(Uuid.BASIC), str('file="{}"'.format(file_path)))).upper()


class Hash(object):
    @classmethod
    def get_pack_format(cls, max_value):
        o = 'q'
        if max_value < 128:
            o = 'b'
        elif max_value < 32768:
            o = 'h'
        elif max_value < 4294967296:
            o = 'i'
        return o

    @classmethod
    def get_hash_value(cls, raw, as_unique_id=False):
        raw_str = str(raw)
        pack_array = [ord(i) for i in raw_str]
        s = hashlib.md5(
            struct.pack('%s%s'%(len(pack_array), cls.get_pack_format(max(pack_array))), *pack_array)
        ).hexdigest()
        if as_unique_id is True:
            return Uuid.get_by_hash_value(s)
        return s.upper()


class LineMatcher(object):
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
    def parse_pattern(self):
        return self._pattern

    @property
    def pattern(self):
        return self._fnmatch_pattern

    @property
    def fnmatch_pattern(self):
        return self._fnmatch_pattern


class AbsFileReader(object):
    SEP = '\n'
    LINE_MATCHER_CLS = None

    def __init__(self, file_path):
        self._file_path = file_path
        self._set_line_raw_update_()

    def _set_line_raw_update_(self):
        self._lines = []
        bsc_core.Log.trace_method_result(
            'file read is started',
            u'file="{}"'.format(self._file_path)
        )
        if self._file_path is not None:
            with open(self._file_path) as f:
                raw = f.read()
                sep = self.SEP
                self._lines = self._get_lines_(raw, sep)
        #
        bsc_core.Log.trace_method_result(
            'file read is completed',
            u'file="{}"'.format(self._file_path)
        )

    @classmethod
    def _get_lines_(cls, raw, sep):
        return [r'{}{}'.format(i, sep) for i in raw.split(sep)]

    @property
    def file_path(self):
        return self._file_path

    @property
    def lines(self):
        return self._lines

    @classmethod
    def _get_matches_(cls, pattern, lines):
        lis = []
        pattern_0 = cls.LINE_MATCHER_CLS(pattern)
        lines = fnmatch.filter(
            lines, pattern_0.fnmatch_pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.parse_pattern, line
            )
            if p:
                variants = p.named
                lis.append((line, variants))
        #
        return lis


class DotMaMeshMtd(object):
    @classmethod
    def get_edge_vertices(cls, ports):
        all_port_names = ports.keys()
        vertex_indices = []
        #
        port_paths = []
        if 'ed[0]' in ports:
            port_paths = ['fc[0]']
        port_paths += fnmatch.filter(
            all_port_names, 'ed?*:*?'
        )
        if port_paths:
            for port_path in port_paths:
                data = ports[port_path].get('data')
                cls._set_edge_vertices_update_(data, vertex_indices)
        return vertex_indices

    @classmethod
    def _set_edge_vertices_update_(cls, data, vertex_indices):
        for i in data.split('\n'):
            i = i.lstrip().rstrip()
            _ = i.split(' ')
            for j in _:
                vertex_index = int(j)
                vertex_indices.append(vertex_index)

    @classmethod
    def get_face_vertices(cls, ports):
        edge_vertex_indices = cls.get_edge_vertices(ports)
        #
        all_port_names = ports.keys()
        face_edge_indices = []
        #
        face_vertex_counts = []
        face_vertex_indices = []
        #
        port_paths = []
        if 'fc[0]' in ports:
            port_paths = ['fc[0]']
        port_paths += fnmatch.filter(
            all_port_names, 'fc?*:*?'
        )
        if port_paths:
            for port_path in port_paths:
                data = ports[port_path].get('data')
                cls._set_face_vertices_update_(
                    data, face_vertex_counts, face_vertex_indices, face_edge_indices, edge_vertex_indices
                    )
        # print 'edge_vertex_indices =', edge_vertex_indices
        # print 'face_edge_indices =', face_edge_indices
        # print 'face_vertex_indices =', face_vertex_indices
        return face_vertex_counts, face_vertex_indices

    @classmethod
    def _set_face_vertices_update_(
            cls, data, face_vertex_counts, face_vertex_indices, face_edge_indices, edge_vertex_indices
            ):
        for i in data.split('\n'):
            i = i.lstrip().rstrip()
            if i.startswith('f'):
                _ = i.split(' ')
                count = int(_[1])
                face_vertex_counts.append(count)
                for j in _[2:]:
                    edge_index = int(j)
                    if edge_index >= 0:
                        vertex_index = edge_vertex_indices[edge_index*3]
                    else:
                        vertex_index = edge_vertex_indices[(abs(edge_index)-1)*3+1]
                    #
                    face_vertex_indices.append(vertex_index)
                    #
                    face_edge_indices.append(edge_index)

    @classmethod
    def get_points(cls, ports):
        all_port_names = ports.keys()
        points = []
        port_paths = fnmatch.filter(
            all_port_names, 'vt?*:*?'
        )
        if port_paths:
            for port_path in port_paths:
                data = ports[port_path].get('data')
                cls._set_points_update_(data, points)
        return points

    @classmethod
    def _set_points_update_(cls, data, points):
        for i in data.split('\n'):
            i = i.lstrip().rstrip()
            _ = i.split(' ')
            for j in _:
                points.append(float(j))


class DotMaFileReader(AbsFileReader):
    SEP = ';\n'
    LINE_MATCHER_CLS = LineMatcher
    FILE_REFERENCE_DICT = {
        'file': 'ftn',
        'reference': 'fn[0]',
        'xgmPalette': 'xfn',
        'xgmDescription': None,
        'gpuCache': 'cfn',
        'AlembicNode': 'fn',
        #
        'aiImage': 'filename',
        'aiMaterialx': 'filename',
        'aiVolume': 'filename',
        'aiStandIn': 'dso',
    }

    def __init__(self, file_path):
        super(DotMaFileReader, self).__init__(file_path)
        self._file_lines = self._get_file_lines_()
        self._obj_lines = self._get_obj_lines_()
        self._port_lines = None
        self._obj_raws = collections.OrderedDict()
        self._objs = collections.OrderedDict()

    def _get_references_(self):
        lis = []
        pattern = self.LINE_MATCHER_CLS(
            u'file -rdi {a} -ns "{namespace}" -rfn "{obj}"{b}-typ{c}"{file_type}"{d}"{file}"{r}'
            )
        lines = fnmatch.filter(
            self.lines, pattern.fnmatch_pattern
        )
        for line in lines:
            p = parse.parse(
                pattern.parse_pattern, line
            )
            if p:
                file_path = p.named['file']
                lis.append(file_path)
        return lis

    def _get_obj_path_(self, obj_parent_name, obj_name):
        def _rcs_fnc(obj_name_):
            _obj_name = obj_name_
            _obj_parent_name = '*'
            if obj_name_ is not None:
                if '|' in obj_name_:
                    _ = obj_name_.split('|')
                    _obj_name = _[-1]
                    if len(_) > 3:
                        _obj_parent_name = '|'.join(_[:-1])
                    else:
                        _obj_parent_name = _[1]
                #
                _match_pattern_0 = matcher_0.parse_pattern.format(
                    **dict(obj_name=_obj_name, obj_parent_name=_obj_parent_name)
                )
                _result_0 = fnmatch.filter(
                    self._lines, _match_pattern_0
                )
                if _result_0:
                    _p_0 = parse.parse(
                        matcher_0.parse_pattern, _result_0[0]
                    )
                    if _p_0:
                        path_args.append(_p_0['obj_name'])
                        _rcs_fnc(_p_0['obj_parent_name'])
                else:
                    _match_pattern_1 = matcher_1.parse_pattern.format(**dict(obj_name=_obj_name))
                    _result_1 = fnmatch.filter(self._lines, _match_pattern_1)
                    if _result_1:
                        _p_1 = parse.parse(
                            matcher_1.parse_pattern, _result_1[0]
                        )
                        if _p_1:
                            path_args.append(_p_1['obj_name'])

        path_args = [obj_name]
        matcher_0 = self.LINE_MATCHER_CLS('createNode transform -n "{obj_name}" -p "{obj_parent_name}";\n')
        matcher_1 = self.LINE_MATCHER_CLS('createNode transform -n "{obj_name}";\n')
        #
        _rcs_fnc(obj_parent_name)
        #
        path_args.reverse()
        return '/'+'/'.join(path_args)

    def _get_obj_by_path_(self, obj_path):
        _ = obj_path.split('/')
        obj_name = _[-1]
        for matcher in [
            self.LINE_MATCHER_CLS('createNode {obj_type} -n "{obj_name}" -p "{obj_parent_name}";\n'),
            self.LINE_MATCHER_CLS('createNode {obj_type} -n "{obj_name}";\n')
        ]:
            pattern = matcher.parse_pattern.format(
                **dict(obj_type='*', obj_name=obj_name, obj_parent_name='*')
            )
            results = fnmatch.filter(
                self._obj_lines, pattern
            )
            if results:
                line = results[0]
                p = parse.parse(
                    matcher.parse_pattern, line
                )
                if p:
                    variants = p.named
                    properties = collections.OrderedDict()
                    properties['line'] = line
                    properties['obj_type'] = variants['obj_type']
                    properties['obj_name'] = variants['obj_name']
                    return properties

    def _get_file_lines_(self):
        return fnmatch.filter(
            self._lines, '*file -rdi *;\n'
        ) or []

    def _get_obj_lines_(self):
        return fnmatch.filter(
            self._lines, 'createNode *;\n'
        ) or []

    def _get_port_lines_(self):
        return fnmatch.filter(
            self._lines, '\tsetAttr *;\n'
        )

    def _get_obj_children_(self, obj_path):
        dic = collections.OrderedDict()
        obj = self._get_obj_by_path_(obj_path)
        if obj:
            _ = obj_path.split('/')
            obj_name_ = _[-1]
            obj_path_ = obj_path.replace('/', '|')
            for matcher in [
                self.LINE_MATCHER_CLS('createNode {obj_type} -n "{obj_name}" -p "{obj_parent_name}";\n'),
                self.LINE_MATCHER_CLS('createNode {obj_type} -n "{obj_name}" -p "{obj_parent_path}";\n')
            ]:
                pattern = matcher.parse_pattern.format(
                    **dict(
                        obj_type='*',
                        obj_name='*',
                        obj_parent_name=obj_name_,
                        obj_parent_path=obj_path_
                    )
                )
                results = fnmatch.filter(
                    self._obj_lines, pattern
                )
                if results:
                    for line in results:
                        p = parse.parse(
                            matcher.parse_pattern, line
                        )
                        if p:
                            variants = p.named
                            i_obj_name = variants['obj_name']
                            i_obj_type = variants['obj_type']
                            i_obj_path = '{}/{}'.format(obj_path, i_obj_name)
                            properties = collections.OrderedDict()
                            properties['line'] = line
                            properties['obj_type'] = i_obj_type
                            properties['obj_name'] = i_obj_name
                            #
                            # print '<obj-create> "{}"'.format(i_obj_path)
                            dic[i_obj_path] = properties
        return dic

    def _get_obj_descendants_(self, obj_path):
        def rcs_fnc_(obj_path_):
            _child_objs = self._get_obj_children_(obj_path_)
            for _obj_path, _obj_properties in _child_objs.items():
                dic[_obj_path] = _obj_properties
                rcs_fnc_(_obj_path)

        #
        dic = collections.OrderedDict()
        obj = self._get_obj_by_path_(obj_path)
        if obj:
            rcs_fnc_(obj_path)
        return dic

    @classmethod
    def _set_obj_filter_(cls, objs, root, obj_types):
        dic = collections.OrderedDict()
        for obj_path, obj_properties in objs.items():
            obj_type = obj_properties['obj_type']
            #
            if obj_path.startswith('{}/'.format(root)) is False:
                continue
            #
            if obj_type not in obj_types:
                continue
            #
            dic[obj_path] = obj_properties
        return dic

    def _get_objs_(self):
        dic = collections.OrderedDict()
        #
        obj_matcher = self.LINE_MATCHER_CLS('createNode {obj_type} -n "{obj_name}";\n')
        lines = fnmatch.filter(
            self._lines, obj_matcher.fnmatch_pattern
        )
        for line in lines:
            properties = collections.OrderedDict()
            p = parse.parse(
                obj_matcher.parse_pattern, line
            )
            if p:
                line_index = self._lines.index(line)
                unique_id = self._get_uuid_at_line_(self._lines[line_index+1])
                obj_variants = p.named
                obj_name_matcher = self.LINE_MATCHER_CLS(
                    '{obj_name}" -p "{obj_parent_name}'
                )
                obj_type = obj_variants['obj_type']
                obj_name = obj_variants['obj_name']
                obj_path = obj_name
                obj_parent_name = None
                if fnmatch.filter(
                        [obj_name], obj_name_matcher.fnmatch_pattern
                ):
                    name_p = parse.parse(
                        obj_name_matcher.parse_pattern, obj_name
                    )
                    if name_p:
                        name_variants = name_p.named
                        obj_name = name_variants['obj_name']
                        obj_parent_name = name_variants['obj_parent_name']
                #
                if obj_type in ['transform', 'mesh']:
                    obj_path = self._get_obj_path_(obj_parent_name, obj_name)
                #
                properties['line'] = line
                properties['obj_type'] = obj_type
                properties['obj_name'] = obj_name
                properties['unique_id'] = unique_id
                dic[obj_path] = properties
        #
        return dic

    def _get_uuid_at_line_(self, line):
        pattern = self.LINE_MATCHER_CLS('{l}rename -uid "{unique_id}";\n')
        results = fnmatch.filter(
            [line], pattern.fnmatch_pattern
        )
        if results:
            result = results[0]
            p = parse.parse(
                pattern.parse_pattern, result
            )
            if p:
                variants = p.named
                return variants['unique_id']

    def _get_obj_port_lines_(self, obj_properties):
        line = obj_properties['line']
        dic = collections.OrderedDict()
        obj_line_index = self._obj_lines.index(line)
        start_index = self._lines.index(line)
        if (obj_line_index+1) < len(self._obj_lines):
            next_line = self._obj_lines[obj_line_index+1]
        else:
            next_line = 'select -ne :time1;\n'
        #
        end_index = self._lines.index(next_line)
        return self._lines[start_index+2:end_index]

    def _get_obj_ports_(self, obj_path, obj_properties):
        dic = collections.OrderedDict()
        lines = self._get_obj_port_lines_(obj_properties)
        for line in lines:
            raw = self._get_port_properties_at_line_(line)
            if isinstance(raw, dict):
                port_path = raw.get('port_path')
                data_type = raw.get('data_type')
                data = raw.get('data')
                #
                properties = collections.OrderedDict()
                properties['date_type'] = data_type
                properties['data'] = data
                if data_type == 'array':
                    properties['size'] = int(raw.get('size'))
                dic[port_path] = properties
                # print '<port-create> "{}"'.format('{}.{}'.format(obj_path, port_path))
        return dic

    def _get_obj_is_io_(self, obj_properties):
        lines = self._get_obj_port_lines_(obj_properties)
        return fnmatch.filter(lines, '\tsetAttr ".io" yes;\n') != []

    def _get_port_properties_at_line_(self, line):
        matchers = [
            (self.LINE_MATCHER_CLS('\tsetAttr -ch {capacity} ".{port_path}" -type "{data_type}" \n\t\t{data};\n'), None,
             None),
            (self.LINE_MATCHER_CLS('\tsetAttr -s {size} -ch {capacity} ".{port_path}";\n'), 'array', None),
            (self.LINE_MATCHER_CLS(
                '\tsetAttr -s {size} -ch {capacity} ".{port_path}" -type "{data_type}" \n\t\t{data};\n'
                ), 'array', None),
            (self.LINE_MATCHER_CLS('\tsetAttr -s {size} -ch {capacity} ".{port_path}"\n\t\t{data};\n'), 'array', None),
            (self.LINE_MATCHER_CLS('\tsetAttr ".{port_path}" -type "{data_type}" \n\t\t{data};\n'), None, None),
            (self.LINE_MATCHER_CLS('\tsetAttr ".{port_path}"\n\t\t{data};\n'), None, None),
            #
            (self.LINE_MATCHER_CLS('\tsetAttr -s {size} ".{port_path}" {data};\n'), 'array', None),
            (self.LINE_MATCHER_CLS('\tsetAttr -s {size} ".{port_path}";\n'), 'array', None),
            #
            (self.LINE_MATCHER_CLS('\tsetAttr ".{port_path}" yes;\n'), 'bool', True),
            (self.LINE_MATCHER_CLS('\tsetAttr ".{port_path}" no;\n'), 'bool', False),
            (self.LINE_MATCHER_CLS('\tsetAttr ".{port_path}" -type "{data_type}" "{data}";\n'), None, None),
            (self.LINE_MATCHER_CLS('\tsetAttr ".{port_path}" {data};\n'), None, None),
        ]
        for i in matchers:
            matcher, data_type, data = i
            results = fnmatch.filter(
                [line], matcher.fnmatch_pattern
            )
            if results:
                p = parse.parse(
                    matcher.parse_pattern, line
                )
                if p:
                    variants = p.named
                    if data_type is not None:
                        variants['data_type'] = data_type
                    if data is not None:
                        variants['data'] = data
                    return variants

    def get_mesh_info(self, root):
        dic = collections.OrderedDict()
        if root is not None:
            objs = self._get_obj_descendants_(root)
            if objs:
                mesh_objs = self._set_obj_filter_(objs, root=root, obj_types=['mesh'])
                if mesh_objs:
                    maximum = len(mesh_objs)
                    mesh_dict = collections.OrderedDict()
                    dic['mesh'] = mesh_dict

                    with bsc_core.LogProcessContext.create(maximum, 'mesh-info-read') as l_p:
                        for seq, (obj_path, obj_properties) in enumerate(mesh_objs.items()):
                            l_p.set_update()
                            #
                            if self._get_obj_is_io_(obj_properties) is True:
                                continue
                            #
                            obj_orig_path = '{}Orig'.format(obj_path)
                            if obj_orig_path in mesh_objs:
                                obj_properties = mesh_objs[obj_orig_path]
                            #
                            ports = self._get_obj_ports_(obj_path, obj_properties)
                            #
                            face_vertex_counts, face_vertex_indices = DotMaMeshMtd.get_face_vertices(ports)
                            face_count = len(face_vertex_counts)
                            face_vertices_uuid = Hash.get_hash_value(
                                (face_vertex_counts, face_vertex_indices), as_unique_id=True
                            )
                            #
                            points = DotMaMeshMtd.get_points(ports)
                            point_count = len(points)
                            points_uuid = Hash.get_hash_value(
                                points, as_unique_id=True
                            )
                            #
                            info = collections.OrderedDict()
                            mesh_dict[obj_path] = info
                            info['face-vertices-uuid'] = face_vertices_uuid
                            info['face-count'] = face_count
                            #
                            info['points-uuid'] = points_uuid
                            info['point-count'] = point_count
            else:
                print 'root is not exists'
        return dic

    def get_reference_file_paths(self, auto_convert=True):
        lis = []
        for line in self._file_lines:
            for matcher in [
                self.LINE_MATCHER_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_MATCHER_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_MATCHER_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" -typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_MATCHER_CLS(
                    'file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -typ "{file_type}" "{file_path}";\n'
                ),
                #
                self.LINE_MATCHER_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_MATCHER_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" \n\t\t-typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_MATCHER_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -op "v=0;" -typ "{file_type}" "{file_path}";\n'
                ),
                self.LINE_MATCHER_CLS(
                    '{l}file -rdi {depth} -ns "{namespace}" -rfn "{obj_path}" -typ "{file_type}" "{file_path}";\n'
                ),
            ]:
                results = fnmatch.filter(
                    [line], matcher.fnmatch_pattern
                )
                if results:
                    result = results[0]
                    p = parse.parse(
                        matcher.parse_pattern, result
                    )
                    if p:
                        variants = p.named
                        file_path = variants.get('file_path')
                        if auto_convert is True:
                            file_path = bsc_core.StgPathMapper.map_to_current(file_path)
                        lis.append(file_path)
                        break
        return lis


class DotAssFileReader(AbsFileReader):
    LINE_MATCHER_CLS = LineMatcher

    def __init__(self, file_path):
        super(DotAssFileReader, self).__init__(file_path)

    def _set_file_paths_convert_(self):
        self._texture_paths = []
        replace_lis = []
        if self._lines:
            matcher = self.LINE_MATCHER_CLS(
                '{l}filename "{file_path}"\n'
            )
            results = fnmatch.filter(
                self._lines, matcher.fnmatch_pattern
            )
            if results:
                for i_line in results:
                    i_p = parse.parse(
                        matcher.parse_pattern, i_line
                    )
                    if i_p:
                        i_variants = i_p.named
                        i_file_path = i_variants['file_path']
                        # noinspection PyArgumentEqualDefault
                        i_new_file_path = bsc_core.StgEnvPathMapper.map_to_env(
                            i_file_path, pattern='[KEY]'
                        )
                        #
                        if i_new_file_path is not None:
                            i_new_line = i_line.replace(i_file_path, i_new_file_path)

                            replace_lis.append(
                                (i_line, i_new_line, i_file_path, i_new_file_path)
                            )
        #
        for i_line, i_new_line, i_file_path, i_new_file_path in replace_lis:
            index = self._lines.index(i_line)
            self._lines[index] = i_new_line
            bsc_core.Log.trace_method_result(
                'dot-ass path-convert',
                'file="{}" >> "{}"'.format(i_file_path, i_new_file_path)
            )

        utl_core.File.set_write(self._file_path, ''.join(self._lines))

    def get_is_from_maya(self):
        if self._lines:
            if len(self._lines) >= 3:
                _ = self._lines[2]
                if fnmatch.filter([_], '### host app: MtoA *'):
                    return True
        return False

    def get_is_from_katana(self):
        if self._lines:
            if len(self._lines) >= 3:
                _ = self._lines[2]
                if fnmatch.filter([_], '### host app: KtoA *'):
                    return True
        return False


class DotUsdaFileReader(AbsFileReader):
    SEP = '\n'
    LINE_MATCHER_CLS = LineMatcher

    def __init__(self, file_path):
        super(DotUsdaFileReader, self).__init__(file_path)

    def get_frame_range(self):
        m_0 = self.LINE_MATCHER_CLS('    startTimeCode = {value}\n')
        m_1 = self.LINE_MATCHER_CLS('    endTimeCode = {value}\n')
        results_0 = fnmatch.filter(
            self._lines, m_0.fnmatch_pattern
        )
        start_frame = 0
        if results_0:
            p_0 = parse.parse(
                m_0.parse_pattern, results_0[0]
            )
            if p_0:
                start_frame = int(p_0['value'])

        results_1 = fnmatch.filter(
            self._lines, m_1.fnmatch_pattern
        )
        end_frame = 0
        if results_1:
            p_1 = parse.parse(
                m_1.parse_pattern, results_1[0]
            )
            if p_1:
                end_frame = int(p_1['value'])
        return start_frame, end_frame


if __name__ == '__main__':
    d = DotUsdaFileReader(
        '/l/prod/cgm/publish/assets/flg/xiangzhang_tree_g/mod/mod_dynamic/xiangzhang_tree_g.mod.mod_dynamic.v001/cache/usd/xiangzhang_tree_g.usda'
    )

    print d.get_frame_range()
