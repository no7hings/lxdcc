# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    resolver = rsv_commands.get_resolver()

    rsv_task = resolver.get_rsv_task(
        project='shl', asset='huotao', step='grm', task='groom'
    )

    rsv_unit = rsv_task.get_rsv_unit(keyword='asset-hair-xgen-file')

    print rsv_unit._pattern

    print rsv_unit

    print rsv_unit.get_result(version='latest')
