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
        # '/production/shows/nsa_dev/assets/env/neighborhood/shared/srf/surface/neighborhood.srf.surface.v002/preview/house_test.srf.surfacing.v003.mov',
        # '/production/shows/nsa_dev/assets/chr/momo/user/work.slash/maya/scenes/modeling/momo.mod.modeling.modeling.v000_001.ma',
        # '/production/shows/nsa_dev/assets/chr/td_test/shared/set/registry/td_test.set.registry.v002/cache/usd/td_test.usda',
        '/production/shows/nsa_dev/assets/chr/nikki/user/work.dongchangbao/maya/scenes/camera/nikki.cam.camera.camera.v000_001.ma'
    ]:
        print r.get_rsv_project_by_any_file_path(i_file_path)
        i_rsv_task = r.get_rsv_task_by_any_file_path(i_file_path)
        i_rsv_task.create_directory(workspace_key='release')
