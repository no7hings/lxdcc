# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs


class DotMaSceneInfoExporter(utl_fnc_obj_abs.AbsExporter):
    OPTION = dict(
        file_path=None,
        root=None
    )
    def __init__(self, option):
        super(DotMaSceneInfoExporter, self).__init__(option)

    def set_run(self):
        import os
        #
        import lxutil.scripts as utl_scripts
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        file_path = self._option.get('file_path')
        root = self._option.get('root')
        #
        base, ext = os.path.splitext(file_path)
        r = utl_scripts.DotMaFileReader(file_path)
        _info = r.get_mesh_info(root=root)
        #
        utl_dcc_objects.OsYamlFile('{}.info.yml'.format(base)).set_write(_info)
