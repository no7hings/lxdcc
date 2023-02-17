# coding:utf-8


def set_asset_texture_tx_export(task_properties, force=False):
    from lxbasic import bsc_core
    #
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    #
    workspace = task_properties.get('workspace')
    step = task_properties.get('step')
    task = task_properties.get('task')
    version = task_properties.get('version')
    if workspace in ['publish'] or force is True:
        # clear-unused-shader
        mya_dcc_objects.Scene.set_unused_shaders_clear()
        #
        root = task_properties.get('dcc.root')
        #
        sub_root = '{}/hi'.format(root)
        #
        sub_root_dag_path = bsc_core.DccPathDagOpt(sub_root)
        sub_root_mya_dag_path = sub_root_dag_path.set_translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        #
        sub_root_mya_obj = mya_dcc_objects.Node(sub_root_mya_dag_path.path)
        if sub_root_mya_obj.get_is_exists() is True:
            # create and repath to texture-tx
            # utl_dcc_operators.DccTexturesOpt(
            #     mya_dcc_objects.TextureReferences(
            #         option=dict(
            #             with_reference=False
            #         )
            #     )
            # ).set_tx_create_and_repath()
            # texture
            texture_src_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_src_directory(
                task=task,
                version=version
            )
            texture_tgt_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_tgt_directory(
                task=task,
                version=version
            )
            #
            mya_fnc_exporters.TextureExporter(
                option=dict(
                    directory_base=texture_src_directory_path,
                    directory=texture_tgt_directory_path,
                    #
                    location=sub_root,
                    fix_name_blank=True,
                    use_tx=True,
                    with_reference=False,
                    use_environ_map=True,
                )
            ).set_run()


def set_asset_texture_export(task_properties, force=False):
    from lxbasic import bsc_core
    #
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    from lxmaya import ma_configure
    #
    workspace = task_properties.get('workspace')
    step = task_properties.get('step')
    task = task_properties.get('task')
    version = task_properties.get('version')
    if workspace in ['publish'] or force is True:
        # clear-unused-shader
        mya_dcc_objects.Scene.set_unused_shaders_clear()
        #
        root = task_properties.get('dcc.root')
        #
        sub_root = '{}/hi'.format(root)
        #
        sub_root_dag_path = bsc_core.DccPathDagOpt(sub_root)
        sub_root_mya_dag_path = sub_root_dag_path.set_translate_to(
            pathsep=ma_configure.Util.OBJ_PATHSEP
        )
        #
        sub_root_mya_obj = mya_dcc_objects.Node(sub_root_mya_dag_path.path)
        if sub_root_mya_obj.get_is_exists() is True:
            # texture-tx repath to orig
            utl_dcc_operators.DccTexturesOpt(
                mya_dcc_objects.TextureReferences(
                    option=dict(
                        with_reference=False
                    )
                )
            ).set_tx_repath_to_orig()
            # texture
            texture_src_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_src_directory(
                task=task,
                version=version
            )
            texture_tgt_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_tgt_directory(
                task=task,
                version=version
            )
            #
            mya_fnc_exporters.TextureExporter(
                option=dict(
                    directory_base=texture_src_directory_path,
                    directory=texture_tgt_directory_path,
                    #
                    location=sub_root,
                    fix_name_blank=True,
                    use_tx=False,
                    with_reference=False,
                    use_environ_map=True,
                )
            ).set_run()
