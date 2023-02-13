# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    utl_core.Log.TRACE_RESULT_ENABLE = False

    r = rsv_commands.get_resolver()
    for i_file_path in [
        # '/l/prod/cgm/work/assets/chr/ast_cg7_dad/mod/modeling/maya/scenes/ast_cg7_dad.mod.modeling.v001.ma',
        # '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/maya/scenes/modeling/td_test.mod.modeling.modeling.v000_001.ma',
        # '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/maya/scenes/modeling/td_test.mod.modeling.modeling.v000_001.ma',
        '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/katana/scenes/modeling/td_test.mod.modeling.modeling.v000_001.katana'
    ]:

        print r.get_rsv_step_by_any_file(i_file_path)

        i_rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(
            i_file_path
        )

        print i_rsv_scene_properties
