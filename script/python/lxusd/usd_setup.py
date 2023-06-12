# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_abstract


class UsdSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(UsdSetup, self).__init__(root)

    def set_run(self):
        self.add_bin_fnc(
            '{}/bin'.format(self._root)
        )
        self.add_library_env_fnc(
            '{}/lib'.format(self._root),
            '{}/lib64'.format(self._root)
        )
        self.add_python_env_fnc(
            '{}/lib/python'.format(self._root)
        )
    @classmethod
    def build_environ(cls):
        cls.add_environ_fnc(
            'PXR_AR_DEFAULT_SEARCH_PATH',
            bsc_core.StgPathMapMtd.map_to_current('/l/prod')
        )
        cls.add_environ_fnc(
            'PXR_AR_DEFAULT_SEARCH_PATH',
            bsc_core.StgPathMapMtd.map_to_current('/t/prod')
        )


class UsdArnoldSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(UsdArnoldSetup, self).__init__(root)

    def set_run(self):
        self.add_library_env_fnc(
            '{}/lib'.format(self._root), '{}/bin'.format(self._root)
        )
