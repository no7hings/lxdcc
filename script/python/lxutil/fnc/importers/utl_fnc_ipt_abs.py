# coding:utf-8
import lxbasic.objects as bsc_objects

from lxutil import utl_core
#
from lxutil.fnc import utl_fnc_obj_abs


class AbsDccLookYamlImporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        file='',
        root='',
        material_assign_force=True,
        look_pass='default',
        version='v000',
    )
    def __init__(self, option):
        super(AbsDccLookYamlImporter, self).__init__(option)
        utl_core.Log.set_module_result_trace(
            'look-yml-import',
            'file="{}"'.format(self._option['file'])
        )
        self._raw = bsc_objects.Content(
            value=self._option['file']
        )

    def get_pass_names(self):
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
    ).get_pass_names()
