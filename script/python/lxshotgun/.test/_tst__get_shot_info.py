# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    import lxutil.dcc.dcc_objects as utl_dcc_objects

    import lxutil.scripts as utl_scripts

    import lxshotgun.objects as stg_objects

    r = rsv_commands.get_resolver()

    rsv_task = r.get_rsv_task(
        project='cjd', shot='e10020', task='effect'
    )

    c = stg_objects.StgConnector()

    q = c.get_stg_task_query(
        **rsv_task.properties.value
    )

    print q
