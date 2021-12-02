# coding:utf-8
import lxmaya.fnc.importers as mya_fnc_importers
#
file_path = session.rsv_unit.get_result(
    version='latest'
)
if file_path:
    _properties = session.rsv_properties
    _branch = _properties.get('branch')
    _look_pass_name = _properties.get(_branch)
    mya_fnc_importers.LookAssImporter(
        file_path=file_path,
        root='/master',
        option=dict(
            look_pass=_look_pass_name,
            assign_selection=True
        )
    ).set_run()

