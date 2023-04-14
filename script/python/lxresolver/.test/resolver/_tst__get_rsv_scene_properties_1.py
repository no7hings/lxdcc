# coding:utf-8
if __name__ == '__main__':
    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    utl_core.Log.TRACE_RESULT_ENABLE = False

    r = rsv_commands.get_resolver()
    for i_file_path in [
        '/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/katana/scenes/surface/td_test.srf.surface.v000_002.katana',
    ]:

        i_rsv_scene_properties = r.get_rsv_scene_properties_by_any_scene_file_path(
            i_file_path
        )

        print i_rsv_scene_properties

