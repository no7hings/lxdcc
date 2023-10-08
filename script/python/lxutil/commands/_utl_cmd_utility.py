# coding:utf-8
import fnmatch

import os

import parse

import re

import glob


def set_open_maya_standalone():
    pass


class MayaReferenceReader(object):
    def __init__(self, file_path):
        self._lines = []
        if os.path.exists(file_path):
            with open(file_path) as f:
                raw = f.read()
                sep = r';{}'.format(os.linesep)
                self._lines = [r'{}{}'.format(i, sep) for i in raw.split(sep)]
        #
        self._variants = []
        self._dcc_paths = []
        self._plf_file_paths = []
    
    def set_refresh(self):
        self._variants = []
        self._dcc_paths = []
        self._plf_file_paths = []
        if self._lines:
            parse_format = '{extra_0} -rdi 1 -ns "{self.reference.namespace}" -rfn "{self.reference.dcc_path}"{extra_1}-typ "{extra_2}"{extra_3}"{self.reference.plf_file_path}";{extra_4}'
            pattern = '*file -rdi 1 -ns "*" -rfn "*"*-typ "*"*"*";*'
            results = fnmatch.filter(self._lines, pattern)
            if results:
                results.sort()
                for i in results:
                    format_dict = {}
                    p = parse.parse(
                        parse_format, i
                    )
                    if p:
                        for k, v in p.named.items():
                            if k.startswith('self.'):
                                format_dict[k] = v
                        #
                        self._variants.append(format_dict)
                        self._dcc_paths.append(format_dict['self.reference.dcc_path'])
                        self._plf_file_paths.append(format_dict['self.reference.plf_file_path'])
        return self._variants

    def get_dcc_paths(self):
        return self._dcc_paths
    
    def get_plf_file_paths(self):
        return self._plf_file_paths

    def get_reference_edits(self, dcc_path):
        pattern = '*setAttr ".ed" -type "dataReferenceEdits"*"{}"*'.format(dcc_path)
        results = fnmatch.filter(self._lines, pattern)
        if results:
            _ = results[0]
            return [str(i).lstrip().rstrip() for i in _.split(os.linesep)]
        return []


def get_reference_raws_from_maya_ascii(file_path):
    lis = []
    if os.path.exists(file_path):
        with open(file_path) as f:
            raw = f.read()
            sep = r';{}'.format(os.linesep)
            ls = [r'{}{}'.format(i, sep) for i in raw.split(sep)]
            parse_format = 'file -rdi 1 -ns "{self.reference.namespace}" -rfn "{self.reference.dcc_path}" -typ "{extra_0}"{extra_1}"{self.reference.plf_file_path}";{extra_2}'
            results = fnmatch.filter(ls, 'file -rdi 1 -ns "*" -rfn "*" -typ "*"*"*";*')
            if results:
                results.sort()
                for i in results:
                    format_dict = {}
                    p = parse.parse(
                        parse_format, i
                    )
                    if p:
                        for k, v in p.named.items():
                            if k.startswith('self.'):
                                format_dict[k] = v

                        lis.append(format_dict)
    return lis


def get_multiply_file_paths(file_path, ext_includes=None):
    def get_ext_replace_fnc_(file_path_, ext_):
        return os.path.splitext(file_path_)[0] + ext_
    #
    def set_os_path_reduce_fnc_(file_path_, pathsep_):
        path_ = file_path_.replace('\\', pathsep_)
        _ = path_.split(pathsep_)
        new_path = pathsep_.join([_i for _i in _ if _i])
        if path_.startswith(pathsep_):
            return pathsep_ + new_path
        return new_path
    #
    re_keys = [
        ('<udim>', 4),
        ('#', -1),
        (r'\$F04', 4),
        (r'\$F', 4),
        (r'%04d', 4),
    ]
    pathsep = '/'
    # convert pathsep
    file_path = set_os_path_reduce_fnc_(file_path, pathsep)
    #
    directory = os.path.dirname(file_path)
    base = os.path.basename(file_path)
    base_new = base
    for k, c in re_keys:
        r = re.finditer(k, base, re.IGNORECASE) or []
        for i in r:
            start, end = i.span()
            if c == -1:
                s = '[0-9]'
                base_new = base_new.replace(base[start:end], s, 1)
            else:
                s = '[0-9]' * c
                base_new = base_new.replace(base[start:end], s, 1)
    #
    glob_pattern = pathsep.join([directory, base_new])
    #
    list_ = glob.glob(glob_pattern)
    if list_:
        list_.sort()
    #
    add_list_ = []
    if isinstance(ext_includes, (tuple, list)):
        for ext in ext_includes:
            for i in list_:
                add_ = get_ext_replace_fnc_(i, ext)
                if os.path.isfile(add_) is True:
                    add_list_.append(add_)
    return list_ + add_list_
