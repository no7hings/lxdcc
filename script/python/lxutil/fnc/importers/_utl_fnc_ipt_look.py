# coding:utf-8
from lxutil.fnc.importers import utl_fnc_ipt_abs


class FncLookYamlImporter(utl_fnc_ipt_abs.AbsDccLookYamlImporter):
    def __init__(self, option):
        super(FncLookYamlImporter, self).__init__(option)
