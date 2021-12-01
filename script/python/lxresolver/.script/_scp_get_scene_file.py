# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    resolver = rsv_commands.get_resolver()

    rsv_task = resolver.get_rsv_task(
        project='shl', asset='shuitao', step='srf', task='surfacing'
    )

    rsv_unit = rsv_task.get_rsv_unit(keyword='asset-katana-scene-src-file')

    print rsv_unit.get_result(version='latest')
