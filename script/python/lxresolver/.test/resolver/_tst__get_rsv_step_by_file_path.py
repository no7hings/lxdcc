# coding:utf-8
if __name__ == '__main__':
    from lxbasic import bsc_core

    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    bsc_core.Log.RESULT_ENABLE = False

    r = rsv_commands.get_resolver()
    for i_file_path in [
        '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/surface/set/scene/v001/td_test.usda'
    ]:
        print r.get_rsv_project_by_any_file_path(i_file_path)
