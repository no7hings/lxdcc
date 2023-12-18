# coding:utf-8
from lxutil.dcc import utl_dcc_obj_abs

from lxutil.dcc.dcc_objects import _utl_dcc_obj_storage


class OsFile(utl_dcc_obj_abs.AbsStgFile):
    OS_DIRECTORY_CLS = _utl_dcc_obj_storage.StgDirectory
    # sequence
    RE_SEQUENCE_PATTERN = r'.*?(\$F.*?)[\.]'
    def __init__(self, path):
        super(OsFile, self).__init__(path)


class OsTexture(utl_dcc_obj_abs.AbsOsTexture):
    OS_DIRECTORY_CLS = _utl_dcc_obj_storage.StgDirectory
    OS_FILE_CLS = OsFile
    # sequence
    RE_SEQUENCE_PATTERN = r'.*?(\$F.*?)[\.]'
    # arnold
    TX_EXT = '.tx'
    def __init__(self, path):
        super(OsTexture, self).__init__(path)
