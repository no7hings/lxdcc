# coding:utf-8
from lxbasic import bsc_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

from lxutil import utl_core


def setup_fnc_():
    from lxutil import utl_setup
    utl_setup.OcioSetup(
        bsc_core.StgPathMapMtd.map_to_current(
            '/l/packages/pg/third_party/ocio/aces/1.2'
        )
    ).set_run()

    from lxarnold import and_setup
    and_setup.MtoaSetup(
        '/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019'
    ).set_run()


setup_fnc_()

d = utl_dcc_objects.OsDirectory_('/l/temp/td/dongchangbao/tx_convert_test/exr_1')

output_directory_path = '/l/temp/td/dongchangbao/tx_convert_test/tx_17'

file_paths = d.get_all_file_paths(include_exts=['.exr'])

if output_directory_path:
    utl_dcc_objects.OsDirectory_(
        output_directory_path
    ).set_create()


def finished_fnc_(index, status, results):
    print index, status


def status_changed_fnc_(index, status):
    print index, status


with utl_core.LogProgressRunner.create_as_bar(maximum=len(file_paths), label='test') as l_p:
    for i_index, i_file_path in enumerate(file_paths):
        l_p.set_update()
        i_cmd = utl_dcc_objects.OsTexture._get_unit_tx_create_cmd_by_src_(
            i_file_path,
            search_directory_path=output_directory_path,
        )
        if i_cmd:
            bsc_core.TrdCmdProcess.set_wait()
            i_t = bsc_core.TrdCmdProcess.set_start(i_cmd, index=i_index)
            i_t.finished.set_connect_to(
                finished_fnc_
            )
            i_t.status_changed.set_connect_to(
                status_changed_fnc_
            )
