# coding:utf-8
import lxbasic.core as bsc_core

import lxcontent.core as ctt_core
#
from lxutil.fnc import utl_fnc_obj_abs


class AbsDccLookYamlImporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        root='',
        #
        material_assign_force=True,
        look_pass='default',
        version='v000',
        #
        auto_rename_node=True
    )

    def __init__(self, option):
        super(AbsDccLookYamlImporter, self).__init__(option)
        bsc_core.Log.trace_method_result(
            'look-yml-import',
            'file="{}"'.format(self._option['file'])
        )
        file_path = self.get('file')
        if bsc_core.StgPathMtd.get_is_exists(file_path) is True:
            self._time_tag = bsc_core.TimestampOpt(
                bsc_core.StgFileOpt(file_path).get_modify_timestamp()
                ).get_as_tag_36()
            self._raw = ctt_core.Content(
                value=self.get('file')
            )
        else:
            raise RuntimeError()

    def get_look_pass_names(self):
        _ = self._raw.get_keys(
            'root.*.properties.customize-attributes.pg_lookpass.enumerate-strings'
        )
        if _:
            key = _[0]
            return self._raw.get(key)
        return []


if __name__ == '__main__':
    print AbsDccLookYamlImporter(
        option=dict(
            file='/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v051/look/yml/td_test.yml',
            root='/master'
        )
    ).get_look_pass_names()
