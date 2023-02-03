# coding:utf-8
from __future__ import print_function

import os

import fnmatch

from lxbasic import bsc_core

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
    def _set_maya_ae_setup_(cls):
        from lxmaya import ma_ae_setup

        _ = utl_core.Environ.get_as_array(
            'LYNXI_MAYA_RESOURCES'
        )
        lis = []
        for i in _:
            path_opt = bsc_core.StgPathOpt(i)
            if path_opt.get_is_exists() is True:
                i_ae_path = '{}/ae'.format(path_opt.get_path())
                if bsc_core.StgPathOpt(i_ae_path).get_is_exists() is True:
                    lis.append(i_ae_path)
        #
        if lis:
            ma_ae_setup.set_ae_procs_setup(
                lis
            )
            utl_core.Log.set_module_result_trace(
                'maya-ae setup',
                'path="{}"'.format(', '.join(lis))
            )
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
        #
        if bsc_core.ApplicationMtd.get_is_maya():
            cls._set_maya_ae_setup_()
