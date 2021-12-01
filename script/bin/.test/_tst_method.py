# coding:utf-8


if __name__ == '__main__':
    from lxutil import utl_core

    utl_core.SubProcessRunner.set_run_with_result(
        'rez-env lxdcc -c "lxmethod -m texture-tx-create -o \\\"texture=/data/f/texture-tx-test/v001/NN_gongshifu.eye_clr.1001.tiff\\\""'
    )
