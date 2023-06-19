# coding:utf-8
from lxbasic import bsc_core

from lxarnold import and_setup

# s = and_setup.MtoaSetup('/l/packages/pg/prod/mtoa/4.2.1.1/platform-linux/maya-2019')
# s.set_run()
# # xgen lib
# s.add_environ_fnc('LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/plug-ins/xgen/lib')
# s.add_environ_fnc('LD_LIBRARY_PATH', '/l/packages/pg/prod/maya/2019.2/platform-linux/Application/lib')

bsc_core.EnvironMtd.set(
    'OCIO', '/l/packages/pg/third_party/ocio/aces/1.2/config.ocio'
)

if __name__ == '__main__':
    from lxarnold import and_core

    from lxbasic import bsc_core

    # i_cmd = and_core.AndTextureOpt_.get_format_convert_as_aces_command(
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/asset/library/lgt/stinson-beach.exr',
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/asset/library/lgt/acescg/src/stinson-beach.exr',
    #     'Utility - Linear - sRGB',
    #     'ACES - ACEScg'
    # )
    #
    # bsc_core.SubProcessMtd.execute_as_block(
    #     i_cmd
    # )

    # i_cmd = and_core.AndTextureOpt_.get_create_tx_as_acescg_command(
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/asset/library/lgt/acescg/src/stinson-beach.exr',
    #     '/data/e/myworkspace/td/lynxi/script/python/.resources/asset/library/lgt/acescg/tx/stinson-beach.tx',
    #     'ACES - ACEScg',
    #     'ACES - ACEScg'
    # )
    #
    # bsc_core.SubProcessMtd.execute_as_block(
    #     i_cmd
    # )

    i_cmd = and_core.AndTextureOpt_.get_format_convert_as_aces_command(
        '/data/e/myworkspace/td/lynxi/script/python/.resources/asset/library/txr/acescg/src/albedo.exr',
        '/data/e/myworkspace/td/lynxi/script/python/.resources/asset/library/txr/acescg/jpg/albedo.png',
        'ACES - ACEScg',
        'ACES - ACEScg'
    )

    bsc_core.SubProcessMtd.execute_as_block(
        i_cmd
    )


