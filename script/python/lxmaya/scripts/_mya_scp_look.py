# coding:utf-8


def set_look_shader_lib_workspace_create():
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxmaya.dcc.dcc_operators as mya_dcc_operators
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    #
    root = mya_dcc_objects.Group(
        '|master|hi|base_higrp'
    )
    root.set_dag_components_create()
    #
    mesh = mya_dcc_objects.Mesh('{}|box_hi|box_hiShape'.format(root.path))
    mesh.set_box_create(12)
    #
    if mesh.get_is_exists() is True:
        mesh_opt = mya_dcc_operators.MeshLookOpt(mesh)
        surface_shaders = mya_dcc_objects.Nodes('aiStandardSurface').get_objs()
        if surface_shaders:
            surface_shader = surface_shaders[-1]
            mesh_opt.set_surface_shader(surface_shader.path)
        displacement_shaders = mya_dcc_objects.Nodes('displacementShader').get_objs()
        if displacement_shaders:
            displacement_shader = displacement_shaders[-1]
            mesh_opt.set_displacement_shader(displacement_shader.path)
    #
    utl_dcc_operators.DccTexturesOpt(
        mya_dcc_objects.TextureReferences(
            option=dict(
                with_reference=False
            )
        )
    ).set_search_from(
        [
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/01_WOOD',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/02-METALS',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/03-PLASTICS',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/04-CONCRET',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/05-GLASSES',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/06-STONES',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/07-FABRICS',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/08-EVERYDAY',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/09-ADVANCED',
            u'/l/temp/td/dongchangbao/Arnold_Shader_Suite_for_MAYA_v2.0/10-TECH'
        ]
    )
