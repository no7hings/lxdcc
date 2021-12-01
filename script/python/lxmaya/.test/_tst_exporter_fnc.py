# coding:utf-8
from lxmaya.fnc import exporters

exporters.LookAssExporter(
    file_path='/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v005/all.ass',
    root='|master'
).set_run()

exporters.LookMtlxExporter(
    file_path='/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v005/all.mtlx',
    ass_file_path='/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v005/all.ass',
    root='|master',
    root_lstrip='/master'
).set_run()

exporters.LookAssignExporter(
    file_path='/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/look/scene/v005/all.assign.yml',
    root='|master',
    root_lstrip='/master'
).set_run()
