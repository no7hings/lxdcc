# coding:utf-8
if __name__ == '__main__':
    import lxresolver.commands as rsv_commands

    r = rsv_commands.get_resolver()

    # print r.get_asset_step_directory_paths(
    #     project='lib', role='flg', asset='shl__cao_a', step='srf'
    # )
    #
    # print r.get_asset_task_directory_paths(
    #     project='lib', role='flg', asset='shl__cao_a', step='srf', task='surfacing'
    # )

    rsv_task = r.get_rsv_task(
        project='cjd', asset='qunzhongnv_b', task='surfacing'
    )

    print rsv_task

    rsv_unit = rsv_task.get_rsv_unit(keyword='{branch}-render-katana-output-sub-dir')

    for i in rsv_unit.get_results(
        version='v014', check_exists=False
    ):
        print i
