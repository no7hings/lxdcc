# coding:utf-8
import os

import fnmatch

import parse


class DotAssReader(object):
    def __init__(self, file_path):
        self._file_path = file_path

        self._set_run_()

    def _set_run_(self):
        self._set_line_raw_update_()
        self._set_geometry_path_raw_update_()
        self._set_texture_path_raw_update_()

    def _set_line_raw_update_(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                raw = f.read()
                sep = '\n'
                self._lines = [r'{}{}'.format(i, sep) for i in raw.split(sep)]

    def _set_geometry_path_raw_update_(self):
        self._geometry_paths = []
        if self._lines:
            parse_pattern = '{extra_0}maya_full_name "{geometry_path}"{extra_1}'
            filter_pattern = '*maya_full_name "*"*'
            results = fnmatch.filter(self._lines, filter_pattern)
            if results:
                for result in results:
                    p = parse.parse(
                        parse_pattern, result
                    )
                    if p:
                        path = p['geometry_path']
                        if not path.endswith('/procedural_curves'):
                            self._geometry_paths.append(path.replace('|', '/'))

    def _set_texture_path_raw_update_(self):
        self._texture_paths = []
        if self._lines:
            parse_pattern = '{extra_0}filename "{texture_path}"{extra_1}'
            filter_pattern = '*filename "*"*'
            results = fnmatch.filter(self._lines, filter_pattern)
            if results:
                for result in results:
                    p = parse.parse(
                        parse_pattern, result
                    )
                    if p:
                        self._texture_paths.append(p['texture_path'])
    @property
    def geometry_paths(self):
        return self._geometry_paths
    @property
    def texture_paths(self):
        return self._texture_paths
