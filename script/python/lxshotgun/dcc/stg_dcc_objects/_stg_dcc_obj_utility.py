# coding:utf-8
from .. import stg_dcc_abstract


class StgTask(stg_dcc_abstract.AbsStgNode):
    PATHSEP = '/'
    def __init__(self, path):
        super(StgTask, self).__init__(path)

    @property
    def type(self):
        return 'task'
