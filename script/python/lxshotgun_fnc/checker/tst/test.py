# coding:utf-8
from lxshotgun.dcc import stg_dcc_objects

from lxshotgun_fnc import stg_fnc_abstract


class Method(stg_fnc_abstract.AbsStgIsp):
    def __init__(self, *args):
        super(Method, self).__init__(*args)

    def _check_method_0(self, *args):
        # obj是DCC节点的抽象实例
        obj, check_index = args[:2]
        # 以下是常用的参数获取，可以调DCC的API自行处理
        print obj.type
        print obj.path
        print obj.name
        print obj
        # 以下保持默认的代码不用修改
        # start check exists
        is_error = not obj.get_is_exists()
        # error object
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_0(self, obj):
        # delete
        print obj.path
        print obj.name
        print obj.type
        print obj
        obj.set_delete()

    def set_check_run(self):
        self.set_restore()
        # dcc object paths
        paths = []
        # obj 是DCC节点的抽象实例，直接使用定义好的就行
        objs = [stg_dcc_objects.StgTask(i) for i in paths]
        #
        self._set_objs_check_(objs, include_indices=[0])
