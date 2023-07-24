# coding:utf-8
from lxutil import utl_core

from lxshotgun import stg_configure


class ShotgunMtd(object):
    @classmethod
    def create_shotgun_instance(cls):
        # noinspection PyUnresolvedReferences
        from shotgun_api3 import shotgun
        #
        _ = shotgun.Shotgun(
            stg_configure.Util.URL,
            stg_configure.Util.SCRIPT,
            stg_configure.Util.CODE,
            ca_certs=utl_core.Path.map_to_current(
                stg_configure.Util.CA_CERTS
            )
        )
        return _

