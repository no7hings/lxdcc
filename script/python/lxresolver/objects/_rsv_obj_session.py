# coding:utf-8
from lxresolver.objects import rsv_obj_session_abs


class RsvObjActionSession(rsv_obj_session_abs.AbsRsvObjActionSession):
    def __init__(self, *args, **kwargs):
        super(RsvObjActionSession, self).__init__(*args, **kwargs)


class RsvUnitActionSession(rsv_obj_session_abs.AbsRsvUnitActionSession):
    def __init__(self, *args, **kwargs):
        super(RsvUnitActionSession, self).__init__(*args, **kwargs)
