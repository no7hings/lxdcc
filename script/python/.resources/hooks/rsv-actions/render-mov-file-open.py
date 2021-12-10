# coding:utf-8
from lxutil import utl_core


def main(session):
    #
    file_path = session.rsv_unit.get_result(
        version='latest',
        extend_variants=session.rsv_unit_extend_variants
    )
    #
    if file_path:
        if session.platform == 'linux':
            # cmd = '/opt/rv/bin/rv "{}"'.format(file_path)
            # utl_core.SubProcessRunner.set_run(cmd)
            utl_core.RvLauncher().set_file_open(
                file_path
            )


# noinspection PyUnresolvedReferences
main(session)
