# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxresolver.commands as rsv_commands

f = '/l/prod/cgm/work/assets/chr/nn_14y_test/srf/surfacing/katana/nn_14y_test.srf.surfacing.v004.katana'

rsv_task = rsv_commands.get_resolver().get_rsv_task_by_any_file_path(f)
if rsv_task:
    rsv_unit = rsv_task.get_rsv_unit(
        keyword='asset-camera-main-abc-file',
    )
    print rsv_unit.get_result(version='latest')
