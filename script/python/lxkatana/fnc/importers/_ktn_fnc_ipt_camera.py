# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class cameraAbcImporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        name=None
    )
    def __init__(self, file_path, root=None, option=None):
        super(cameraAbcImporter, self).__init__(file_path, root, option)

    def set_run(self):
        file_path = self._file_path
        root = self._root
        #
        name = self._option['name']
        node = ktn_dcc_objects.Node(
            '/rootNode/{}'.format(name)
        )
        if node.get_is_exists() is False:
            node.set_create('Alembic_In')
        #
        atr_dic = {
            'abcAsset': file_path,
            'name': root,
            'addToCameraList': 1.0
        }
        #
        for k, v in atr_dic.items():
            p = node.get_port(k)
            p.set(v)
            p.ktn_port.setUseNodeDefault(False)
