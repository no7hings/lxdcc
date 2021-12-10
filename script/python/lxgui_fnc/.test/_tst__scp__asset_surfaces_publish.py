# coding:utf-8
import cProfile


def test():
    import lxgui.fnc.methods as gui_fnc_methods
    #
    gui_fnc_methods.AssetBatcher(
        project='lib',
        assets=['ast_shl_grass_1d'],
        option=dict(
            surface_publish=True
        )
    ).set_run()


cProfile.run("test()")
