# coding:utf-8
from lxshotgun import stg_configure


class ShotgunMtd(object):
    @classmethod
    def set_shotgun_instance_create(cls):
        # noinspection PyUnresolvedReferences
        from shotgun_api3 import shotgun

        _ = shotgun.Shotgun(
            stg_configure.Util.URL,
            stg_configure.Util.SCRIPT,
            stg_configure.Util.CODE
        )
        return _
    @classmethod
    def set_shotgun_engine_setup(cls):
        pass
