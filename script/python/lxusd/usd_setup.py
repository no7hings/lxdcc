# coding:utf-8
from lxutil import utl_abstract


class UsdSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(UsdSetup, self).__init__(root)

    def set_run(self):
        self._set_bin_setup_('{}/bin'.format(self._root))
        self._set_library_setup_('{}/lib'.format(self._root), '{}/bin'.format(self._root), '{}/lib64'.format(self._root))
        self._set_python_setup_('{}/lib/python'.format(self._root))


class UsdArnoldSetup(utl_abstract.AbsSetup):
    def __init__(self, root):
        super(UsdArnoldSetup, self).__init__(root)

    def set_run(self):
        self._set_library_setup_('{}/lib'.format(self._root), '{}/bin'.format(self._root))
