# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_abstract


class UsdSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(UsdSetup, self).__init__(root)

    def set_run(self):
        self._set_bin_setup_('{}/bin'.format(self._root))
        self._set_library_setup_('{}/lib'.format(self._root), '{}/bin'.format(self._root), '{}/lib64'.format(self._root))
        self._set_python_setup_('{}/lib/python'.format(self._root))
    @classmethod
    def set_environs_setup(cls):
        bsc_core.EnvironMtd.set_add(
            'PXR_AR_DEFAULT_SEARCH_PATH',
            bsc_core.StoragePathMtd.set_map_to_platform('/l/prod')
        )


class UsdArnoldSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(UsdArnoldSetup, self).__init__(root)

    def set_run(self):
        self._set_library_setup_('{}/lib'.format(self._root), '{}/bin'.format(self._root))
