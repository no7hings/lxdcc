# coding:utf-8
from lxshotgun.dcc import stg_dcc_objects

from lxshotgun_fnc import stg_fnc_abstract


class Method(stg_fnc_abstract.AbsStgIsp):
    def __init__(self, *args):
        super(Method, self).__init__(*args)

    def _check_method_0(self, *args):
        # obj: instance [继承自"util_abstract.AbsDccObj"]
        # check_index: int [错误的索引]
        obj, check_index = args
        # 以下是常用的参数获取，可以调DCC的API自行处理
        # start check exists
        is_error = not obj.get_is_exists()
        # end
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
        pass
