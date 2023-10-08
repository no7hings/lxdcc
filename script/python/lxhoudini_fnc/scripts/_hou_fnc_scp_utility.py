# coding:utf-8


def set_geometry_unify_by_usd_file(option):
    import os
    #
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxhoudini.dcc.dcc_objects as hou_dcc_objects
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    temp_geo = hou_dcc_objects.Node('/obj/temp_geo')
    hou_temp_geo, _ = temp_geo.get_dcc_instance('geo')
    temp_hda = hou_dcc_objects.Node('/obj/temp_geo/temp_hda')
    hou_temp_hda, _ = temp_hda.get_dcc_instance('hashuv')
    input_file_path = option_opt.get('file')
    base, ext = os.path.splitext(input_file_path)
    output_scene_file_path = '{}.output.hip'.format(base)
    output_file_path = '{}.output{}'.format(base, ext)
    temp_hda.get_port('usdfile').set(input_file_path)
    temp_hda.get_port('outUsdFile').set(output_file_path)
    hou_dcc_objects.Scene.save_file_to(
        output_scene_file_path
    )
    temp_hda.get_port('execute').hou_port.pressButton()
    utl_core.Log.set_module_result_trace(
        'geometry-uv-map-unify',
        'file="{}"'.format(output_file_path)
    )


def set_geometry_uv_map_assign_by_usd_file(option):
    import os
    #
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxhoudini.dcc.dcc_objects as hou_dcc_objects
    #
    option_opt = bsc_core.ArgDictStringOpt(option)
    temp_geo = hou_dcc_objects.Node('/obj/temp_geo')
    hou_temp_geo, _ = temp_geo.get_dcc_instance('geo')
    temp_hda = hou_dcc_objects.Node('/obj/temp_geo/temp_hda')
    hou_temp_hda, _ = temp_hda.get_dcc_instance('hashUvAssign')
    input_file_path = option_opt.get('file')
    base, ext = os.path.splitext(input_file_path)
    output_scene_file_path = '{}.output.hip'.format(base)
    output_file_path = '{}.output{}'.format(base, ext)
    temp_hda.get_port('filepath1').set(input_file_path)
    temp_hda.get_port('lopoutput').set(output_file_path)
    hou_dcc_objects.Scene.save_file_to(
        output_scene_file_path
    )
    temp_hda.get_port('execute').hou_port.pressButton()
    utl_core.Log.set_module_result_trace(
        'geometry-uv-map-unify',
        'file="{}"'.format(output_file_path)
    )
