# coding:utf-8
import re

import fnmatch

import parse

from lxutil import utl_configure, utl_core

from lxbasic import bsc_core

from lxbasic.objects import bsc_obj_abs

import lxbasic.objects as bsc_objects

import copy

import os


class Content(bsc_obj_abs.AbsContent):
    PATHSEP = '.'
    def __init__(self, key=None, value=None):
        super(Content, self).__init__(key, value)


class Configure(bsc_obj_abs.AbsConfigure):
    PATHSEP = '.'
    def __init__(self, key=None, value=None):
        super(Configure, self).__init__(key, value)


class Property(object):
    def __init__(self, key, value):
        self._key = key
        self._value = value
    @property
    def key(self):
        return self._key
    @property
    def value(self):
        return self._value

    def __str__(self):
        return '{} = {}'.format(
            self._key, self._value
        )


class Properties(bsc_obj_abs.AbsContent):
    PATHSEP = '.'
    PROPERTY_CLASS = Property
    def __init__(self, obj, raw):
        super(Properties, self).__init__(value=raw)
        self._obj = obj

    def get_property(self, key):
        return self.PROPERTY_CLASS(key, self.get(key))


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


class DotAssReader(bsc_obj_abs.AbsFileReader):
    def __init__(self, file_path):
        super(DotAssReader, self).__init__(file_path)

    def _set_run_(self):
        self._set_geometry_path_raw_update_()
        self._get_file_paths_()

    def _set_geometry_path_raw_update_(self):
        self._geometry_paths = []
        if self._lines:
            parse_pattern = '{extra_0}maya_full_name "{geometry_path}"{extra_1}'
            filter_pattern = '*maya_full_name "*"*'
            results = fnmatch.filter(self._lines, filter_pattern)
            if results:
                for i_result in results:
                    p = parse.parse(
                        parse_pattern, i_result
                    )
                    if p:
                        path = p['geometry_path']
                        if not path.endswith('/procedural_curves'):
                            self._geometry_paths.append(path.replace('|', '/'))

    def _get_file_paths_(self):
        self._texture_paths = []
        if self._lines:
            parse_pattern = '{extra_0}filename "{texture_path}"{extra_1}'
            filter_pattern = '*filename "*"*'
            results = fnmatch.filter(self._lines, filter_pattern)
            if results:
                for i_result in results:
                    p = parse.parse(
                        parse_pattern, i_result
                    )
                    if p:
                        self._texture_paths.append(p['texture_path'])
        return self._texture_paths
    @property
    def geometry_paths(self):
        return self._geometry_paths
    @property
    def texture_paths(self):
        return self._texture_paths

    def get_file_paths(self):
        return self._get_file_paths_()


class DotXgenFileReader(bsc_obj_abs.AbsFileReader):
    SEP = '\n\n'
    FILE_REFERENCE_DICT = {
        'Palette': ['xgDataPath', 'xgProjectPath'],
        'Description': ['xgDataPath', 'xgProjectPath']
    }
    def __init__(self, file_path):
        super(DotXgenFileReader, self).__init__(file_path)

    def _get_obj_raws_(self):
        lis = []
        utl_core.Log.set_module_result_trace(
            'file parse is started', 'file="{}"'.format(
                self._file_path
            )
        )
        pattern_0 = _Pattern(u'{obj_type}\n{port_lines}\n')
        lines = fnmatch.filter(
            self.lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                variant = p.named
                lis.append((line, variant))
        utl_core.Log.set_module_result_trace(
            'file parse is completed', 'file="{}"'.format(
                self._file_path
            )
        )
        return lis
    @classmethod
    def _get_obj_port_raws_(cls, raw):
        dic = {}
        sep = '\n'
        _ = cls._get_lines_(raw, sep)
        for i in _:
            __ = i.strip().split('\t')
            port_name, port_raw, port_type = __[0], __[-1], None
            dic[port_name] = port_type, port_raw
        return dic

    def _get_file_paths_(self):
        lis = []
        obj_raws = self._get_obj_raws_()
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            if i_obj_type in self.FILE_REFERENCE_DICT:
                i_port_dict = self._get_obj_port_raws_(i_variants['port_lines'])
                i_obj_name = i_port_dict['name'][-1]
                #
                i_port_names = self.FILE_REFERENCE_DICT[i_obj_type]
                for j_port_name in i_port_names:
                    if j_port_name in i_port_dict:
                        j_port_type, j_port_raw = i_port_dict[j_port_name]
                        raw = dict(
                            obj_type=i_obj_type,
                            obj_name=i_obj_name,
                            port_name=j_port_name,
                            port_type=j_port_type,
                            port_raw=j_port_raw,
                            line_index=self.lines.index(i_line),
                            line=i_line,
                        )
                        lis.append(raw)
        return lis

    def get_file_paths(self):
        return self._get_file_paths_()

    def set_repair(self):
        lis = []
        project_directory_path = self.get_project_directory_path()
        project_directory_path = bsc_core.StoragePathOpt(
            project_directory_path
        ).get_path()
        _ = self.get_file_paths()
        for i in _:
            i_port_name = i['port_name']
            if i_port_name == 'xgDataPath':
                i_raw = i['port_raw']
                if i_raw.startswith('${PROJECT}'):
                    i_new_raw = i_raw.replace('${PROJECT}', project_directory_path)
                    #
                    if i_raw != i_new_raw:
                        i_line_index = i['line_index']
                        i_line = i['line']
                        i_new_line = i_line.replace(i_raw, i_new_raw)
                        lis.append(
                            (i_line_index, i_new_line)
                        )
                        utl_core.Log.set_module_result_trace(
                            u'xgen collection directory repair',
                            u'directory="{}" >> "{}"'.format(
                                i_raw, i_new_raw
                            )
                        )

        for i_line_index, i_line in lis:
            self.lines[i_line_index] = i_line

    def get_project_directory_path(self):
        obj_raws = self._get_obj_raws_()
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            if i_obj_type == 'Palette':
                i_port_dict = self._get_obj_port_raws_(i_variants['port_lines'])
                j_port_type, j_port_raw = i_port_dict['xgProjectPath']
                return j_port_raw

    def set_collection_directory_repath(self, xgen_collection_directory_path, xgen_collection_name):
        _ = self.get_file_paths()
        lis = []
        utl_core.Log.set_module_result_trace(
            u'xgen collection directory repath is started',
            u'directory="{}"'.format(
                xgen_collection_directory_path
            )
        )
        for i in _:
            i_port_name = i['port_name']
            if i_port_name == 'xgDataPath':
                i_raw = i['port_raw']
                i_raw = bsc_core.StoragePathOpt(
                    i_raw
                ).get_path()
                #
                i_obj_type = i['obj_type']
                i_obj_name = i['obj_name']
                if i_obj_type == 'Description':
                    i_new_raw = u'{}/{}/'.format(xgen_collection_directory_path, xgen_collection_name)
                else:
                    i_new_raw = u'{}/{}'.format(xgen_collection_directory_path, xgen_collection_name)
                #
                if i_raw != i_new_raw:
                    i_line_index = i['line_index']
                    i_line = i['line']
                    i_new_line = i_line.replace(i_raw, i_new_raw)
                    #
                    lis.append(
                        (i_line_index, i_new_line)
                    )
                    utl_core.Log.set_module_result_trace(
                        u'xgen collection directory repath',
                        u'obj="{}"'.format(
                            i_obj_name
                        )
                    )
                    utl_core.Log.set_module_result_trace(
                        u'xgen collection directory repath',
                        u'directory="{}" >> "{}"'.format(
                            i_raw, i_new_raw
                        )
                    )
        #
        for i_line_index, i_line in lis:
            self.lines[i_line_index] = i_line
        #
        utl_core.Log.set_module_result_trace(
            u'xgen collection directory repath is completed',
            u'directory="{}"'.format(
                xgen_collection_directory_path
            )
        )

    def set_project_directory_repath(self, xgen_project_directory_path):
        _ = self.get_file_paths()
        lis = []
        utl_core.Log.set_module_result_trace(
            u'xgen project directory repath is started',
            u'directory="{}"'.format(
                xgen_project_directory_path
            )
        )
        for i in _:
            i_port_name = i['port_name']
            if i_port_name == 'xgProjectPath':
                i_raw = i['port_raw']
                i_raw = bsc_core.StoragePathOpt(
                    i_raw
                ).get_path()
                #
                i_obj_name = i['obj_name']
                #
                i_new_raw = xgen_project_directory_path
                #
                if i_raw != i_new_raw:
                    i_line_index = i['line_index']
                    i_line = i['line']
                    i_new_line = i_line.replace(i_raw, i_new_raw)
                    lis.append(
                        (i_line_index, i_new_line)
                    )
                    utl_core.Log.set_module_result_trace(
                        u'xgen project directory repath',
                        u'obj="{}"'.format(
                            i_obj_name
                        )
                    )
                    utl_core.Log.set_module_result_trace(
                        u'xgen project directory repath',
                        u'directory="{}" >> "{}"'.format(
                            i_raw, i_new_raw
                        )
                    )
        #
        for i_line_index, i_line in lis:
            self.lines[i_line_index] = i_line
        #
        utl_core.Log.set_module_result_trace(
            u'xgen project directory repath is completed',
            u'directory="{}"'.format(
                xgen_project_directory_path
            )
        )

    def get_description_properties(self):
        d = bsc_objects.Dict()
        utl_core.Log.set_module_result_trace(
            'file parse is started', 'file="{}"'.format(
                self._file_path
            )
        )
        obj_raws = self._get_obj_raws_()
        enable = False
        cur_description_name = None
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            i_port_dict = self._get_obj_port_raws_(i_variants['port_lines'])
            #
            if i_obj_type == 'Description':
                enable = True
                cur_description_name = i_port_dict['name'][-1]
            elif i_obj_type.startswith('Patches'):
                enable = False
            #
            i_key = cur_description_name
            if i_obj_type != 'Description':
                if cur_description_name is not None:
                    i_key = '{}.{}'.format(cur_description_name, i_obj_type)
                else:
                    i_key = i_obj_type
            #
            if enable is True:
                if '\t' not in i_obj_type:
                    for j_port_name, (j_port_type, j_port_raw) in i_port_dict.items():
                        j_key = '{}.{}'.format(i_key, j_port_name)
                        # print j_key, j_port_raw
                        d.set(j_key, j_port_raw)
                else:
                    pass
                    j_key = '{}.extra'.format(cur_description_name)
                    d.set_element_add(j_key, i_obj_type)
                    # print i_obj_type
        return d

    def get_collection_data_directory_path(self):
        pass

    def set_save(self):
        utl_core.File.set_write(
            self.file_path, u''.join(self.lines)
        )


class DotMaFileReader(bsc_obj_abs.AbsFileReader):
    SEP = ';\n'
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

    def _get_references_(self):
        lis = []
        pattern = _Pattern(u'file -rdi {a} -ns "{namespace}" -rfn "{obj}"{b}-typ{c}"{file_type}"{d}"{file}"{r}')
        lines = fnmatch.filter(
            self.lines, pattern.pattern
        )
        for i_line in lines:
            p = parse.parse(
                pattern.format, i_line
            )
            if p:
                file_path = p.named['file']
                lis.append(file_path)
        return lis

    def _get_obj_raws_(self):
        lis = []
        pattern_0 = _Pattern(u'createNode {obj_type} -n "{obj_name}"{r}')
        lines = fnmatch.filter(
            self.lines, pattern_0.pattern
        )
        for i_line in lines:
            p = parse.parse(
                pattern_0.format, i_line
            )
            if p:
                variants = p.named
                lis.append((i_line, variants))
        #
        return lis

    def _get_obj_port_raws_(self, line):
        dic = {}
        index = self.lines.index(line)
        #
        is_end = False
        p_index = index+2
        p_maximum = 10000
        c = 0
        while is_end is False:
            p_line = self.lines[p_index]
            is_port_s = self._get_is_port_(p_line)
            if is_port_s:
                # check max raw size
                p_line_size = len(p_line)
                if p_line_size < 1000:
                    port_raw = self._get_obj_port_raw_(p_line)
                    if port_raw is not None:
                        port_variant = port_raw
                        port_name, port_type, port_raw = port_variant['port_name'], port_variant['port_type'], port_variant['port_raw']
                        dic[port_name] = port_type, port_raw
                else:
                    print 'error: line [{}...] is to large({})'.format(p_line[:50], p_line_size)
            else:
                is_end = True
            if c == p_maximum:
                is_end = True
            p_index += 1
            c += 1
        return dic
    @classmethod
    def _get_is_port_(cls, line):
        pattern_0 = _Pattern(u'{l}setAttr{r}')
        results = fnmatch.filter(
            [line], pattern_0.pattern
        )
        if results:
            return True
        #
        pattern_1 = _Pattern(u'{l}addAttr{r}')
        results = fnmatch.filter(
            [line], pattern_1.pattern
        )
        if results:
            return True
        return False
    @classmethod
    def _get_obj_port_raw_(cls, line):
        pattern_0 = _Pattern(u'{l}setAttr ".{port_name}" -type "{port_type}"{m}"{port_raw}";{r}')
        results = fnmatch.filter(
            [line], pattern_0.pattern
        )
        if results:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                variant = p.named
                return variant
        pattern_1 = _Pattern(u'{l}setAttr ".{port_name}" {port_raw};{r}')
        results = fnmatch.filter(
            [line], pattern_1.pattern
        )
        if results:
            p = parse.parse(
                pattern_1.format, line
            )
            if p:
                variant = p.named
                variant['port_type'] = None
                return variant
        pattern_2 = _Pattern(u'{l}addAttr {m0} -ln "{port_name}" -dt "{port_type}";{r}')
        results = fnmatch.filter(
            [line], pattern_2.pattern
        )
        if results:
            p = parse.parse(
                pattern_2.format, line
            )
            if p:
                variant = p.named
                variant['port_raw'] = None
                return variant
    @classmethod
    def _get_obj_uuid_raw_(cls, line):
        pattern = _Pattern(u'{l}rename -uuid "{raw}"{r}')
        results = fnmatch.filter(
            [line], pattern.pattern
        )
        if results:
            result = results[0]
            p = parse.parse(
                pattern.format, result
            )
            print p

    def _test_(self):
        self._get_file_paths_()

    def _get_file_paths_(self):
        lis = []
        obj_raws = self._get_obj_raws_()
        print 'start file-path: "{}"'.format(self.file_path)
        for i_obj_raw in obj_raws:
            i_line, i_variants = i_obj_raw
            i_obj_type = i_variants['obj_type']
            i_obj_name = i_variants['obj_name']
            if i_obj_type in self.FILE_REFERENCE_DICT:
                i_port_name = self.FILE_REFERENCE_DICT[i_obj_type]
                if i_port_name is not None:
                    # print 'start obj: "{}"'.format(obj_name)
                    port_raws = self._get_obj_port_raws_(i_line)
                    if i_port_name in port_raws:
                        i_port_type, i_port_raw = port_raws[i_port_name]
                        raw = dict(
                            obj_type=i_obj_type,
                            obj_name=i_obj_name,
                            port_name=i_port_name,
                            port_type=i_port_type,
                            port_raw=i_port_raw
                        )
                        if i_obj_type == 'file':
                            i_file_path = i_port_raw
                            i_file_base = os.path.basename(i_file_path)
                            # sequence
                            if 'ufe' in port_raws:
                                _, i_sequence = port_raws['ufe']
                                if i_sequence == 'yes':
                                    i_results = re.findall(r'[0-9]{3,4}', i_file_base)
                                    if i_results:
                                        i_file_path = i_file_path.replace(i_results[-1], '<f>')
                                        raw['port_raw'] = i_file_path
                            # udim
                            if 'uvt' in port_raws:
                                _, is_udim = port_raws['uvt']
                                if is_udim == '3':
                                    i_results = re.findall(r'[0-9][0-9][0-9][0-9]', i_file_base)
                                    if i_results:
                                        i_file_path = i_file_path.replace(i_results[-1], '<udim>')
                                        raw['port_raw'] = i_file_path
                        #
                        lis.append(raw)
                    # print 'end obj: "{}"'.format(obj_name)
        print 'end file-path: "{}"'.format(self.file_path)
        return lis

    def get_file_paths(self):
        return self._get_file_paths_()


class DotMtlxFileReader(bsc_obj_abs.AbsFileReader):
    SEP = '\n'
    LINE_MATCHER_CLS = _Pattern
    PROPERTIES_CLASS = Properties
    def __init__(self, file_path):
        super(DotMtlxFileReader, self).__init__(file_path)

    def _get_material_assign_matches_(self):
        return self._get_matches_(
            pattern=u'{l}<materialassign name="material_assign__{geometry_type}__{index}" material="{material}" geom="{geometry}" />{r}',
            lines=self.lines
        )

    def _get_property_set_assign_matches_(self):
        return self._get_matches_(
            pattern=u'{l}<propertysetassign name="{assign_name}" propertyset="{property_set_name}" geom="{geometry}" />{r}',
            lines=self.lines
        )

    def _get_property_set_raw_(self, property_set_name):
        def get_property_fnc_():
            pass

        matches = self._get_matches_(
            pattern=u'{l}<propertyset name="%s">{r}' % property_set_name,
            lines=self._lines
        )
        if matches:
            line, properties = matches[-1]
            index = self._lines.index(line)

            index += 1

            property_line = self._lines[index]
            pattern = u'{l}<property >{r}'
            print property_line

    def get_material_assign_raws(self):
        return self._get_material_assign_matches_()

    def get_geometries_properties(self):
        lis = []
        material_assign_raws = self._get_material_assign_matches_()
        for material_assign_raw in material_assign_raws:
            geometry_properties = self.PROPERTIES_CLASS(self, {})
            line, properties = material_assign_raw
            geometry_properties.set('type', properties['geometry_type'])
            geometry_properties.set('path', properties['geometry'])
            geometry_properties.set('material', properties['material'])
            lis.append(geometry_properties)
        property_set_assign_raws = self._get_property_set_assign_matches_()
        for property_set_assign_raw in property_set_assign_raws:
            line, properties = property_set_assign_raw
            property_set_name = properties['property_set_name']
            property_set_raw = self._get_property_set_raw_(property_set_name)
        return lis


class DotOslFileReader(bsc_obj_abs.AbsFileReader):
    SEP = '\n'
    LINE_MATCHER_CLS = _Pattern
    PROPERTIES_CLASS = Properties
    def __init__(self, file_path):
        super(DotOslFileReader, self).__init__(file_path)

    def _get_shader_start_line_(self):
        _ = self._get_matches_(
            pattern='shader {shader_name}({extra}',
            lines=self.lines
        )
        print _

    def _get_shader_lines_(self):
        index = 0
        p_index = index + 2
        is_end = False
        p_maximum = 10000
        c = 0
        while is_end is False:
            pass

    def get_port_args(self):
        print self._get_matches_(
            pattern='',
            lines=self.lines
        )


class DotUsdaFile(object):
    OPTION = dict(
        root='master',
        preset=dict(
            up_axis='Y',
            linear_unit=0.01
        ),
        option=dict(
            indent=4,
            linesep="\n"
        )
    )
    def __init__(self, file_path):
        self._file_path = file_path
    @classmethod
    def _set_option_update_(cls, option, directory_path):
        def rcs_fnc_(v_):
            if isinstance(v_, dict):
                for _k, _v in v_.items():
                    if _k.endswith('file'):
                        v_[_k] = os.path.relpath(_v, directory_path)
                    elif _k.endswith('file_dict'):
                        v_[_k] = {k: os.path.relpath(v, directory_path) for k, v in _v.items()}
                    else:
                        rcs_fnc_(_v)
            elif isinstance(v_, (tuple, list)):
                for _i in v_:
                    rcs_fnc_(_i)
            else:
                pass
            #
        rcs_fnc_(option)
    @classmethod
    def _set_write_(cls, key, file_path, option):
        directory_path = os.path.dirname(file_path)
        #
        j2_template = utl_configure.Jinja.USDA.get_template(key)
        kwargs = copy.copy(cls.OPTION)
        #
        cls._set_option_update_(option, directory_path)
        #
        kwargs.update(option)
        raw = j2_template.render(**kwargs)
        bsc_core.StorageFileOpt(file_path).set_write(
            raw
        )
        utl_core.Log.set_module_result_trace(
            'usda-file-write',
            u'file="{}"'.format(file_path)
        )

    def set_surface_look_write(self, look_root_name, look_pass_name, look_pass_names, look_file_path, look_properties_file_dict):
        self._set_write_(
            key='surface-look.j2',
            file_path=self._file_path,
            option=dict(
                look_root=look_root_name,
                look_pass=look_pass_name,
                look_passes=look_pass_names,
                look_file=look_file_path,
                look_properties_file_dict=look_properties_file_dict
            )
        )

    def set_surface_registry_write(self, look_file_path, uv_map_file_path):
        self._set_write_(
            key='surface-registry.j2',
            file_path=self._file_path,
            option=dict(
                look_file=look_file_path,
                uv_map_file=uv_map_file_path,
            )
        )


if __name__ == '__main__':
    d = DotMaFileReader(
        '/data/f/test_sequence/butterfly_a.ma'
    )
    print re.findall(r'[0-9]{3,4}', 'test.1.exr')
    print d.get_file_paths()
