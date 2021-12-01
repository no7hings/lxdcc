# coding:utf-8
from lxmaya.fnc import importers

importers.LookAssignImporter(
    file_path='/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v005/all.assign.yml',
    root='|master',
    root_lstrip='/master'
).set_run()


importers.GeometryUsdImporter_(
    file_path='/l/prod/shl/publish/assets/chr/nn_gongshifu/mod/modeling/nn_gongshifu.mod.modeling.v004/cache/abc/hi.abc',
    root='/master',
).set_run()
