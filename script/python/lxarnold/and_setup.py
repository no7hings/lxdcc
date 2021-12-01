# coding:utf-8
from __future__ import print_function

import sys

import os

import fnmatch

from lxutil import utl_core, utl_abstract


class AbsArnoldSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(AbsArnoldSetup, self).__init__(root)
    @classmethod
    def _set_procedural_setup_(cls, *args):
        [cls._set_environ_add_('ARNOLD_PROCEDURAL_PATH', i) for i in args]
    @classmethod
    def _set_plugin_setup_(cls, *args):
        [cls._set_environ_add_('ARNOLD_PLUGIN_PATH', i) for i in args]

    def set_run(self):
        NotImplementedError()


class MtoaSetup(AbsArnoldSetup):
    def __init__(self, root):
        super(MtoaSetup, self).__init__(root)

    def set_run(self):
        self._set_python_setup_('{}/scripts'.format(self._root))
        self._set_library_setup_('{}/bin'.format(self._root))
        self._set_procedural_setup_('{}/procedurals'.format(self._root))
        self._set_plugin_setup_('{}/plugins'.format(self._root), '{}/procedurals'.format(self._root))
        self._set_bin_setup_('{}/bin'.format(self._root))


class KtoaSetup(AbsArnoldSetup):
    def __init__(self, root):
        super(KtoaSetup, self).__init__(root)

    def set_run(self):
        pass


class MayaSetup(object):
    def __init__(self):
        pass
    @classmethod
    def run(cls):
        raw = os.environ.get('MAYA_PLUG_IN_PATH')
        if raw:
            paths = raw.split(os.pathsep)
            if paths:
                match_pattern = '*/mtoa/*/plug-ins'
                results = fnmatch.filter(paths, match_pattern)
                if results:
                    mtoa_plugin_path = results[0]
                    MtoaSetup(mtoa_plugin_path).set_run()
