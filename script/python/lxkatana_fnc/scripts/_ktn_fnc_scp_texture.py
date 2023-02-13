# coding:utf-8


def set_asset_texture_tx_export(task_properties, force=False):
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxkatana.fnc.exporters as ktn_fnc_exporters
    #
    workspace = task_properties.get('workspace')
    task = task_properties.get('task')
    version = task_properties.get('version')
    if workspace in ['publish'] or force is True:
        # create and repath to texture-tx
        # utl_dcc_operators.DccTexturesOpt(
        #     ktn_dcc_objects.TextureReferences(
        #         option=dict(
        #             with_reference=False
        #         )
        #     )
        # ).set_tx_create_and_repath()
        # texture-src
        texture_src_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_src_directory(
            task=task,
            version=version
        )
        # TODO remove orig directory
        # texture-tgt
        texture_tgt_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_tgt_directory(
            task=task,
            version=version
        )
        #
        ktn_fnc_exporters.TextureExporter(
            option=dict(
                directory_base=texture_src_directory_path,
                directory=texture_tgt_directory_path,
                #
                fix_name_blank=True,
                use_tx=True,
                with_reference=False,
                use_environ_map=True,
                #
                ignore_missing_texture=False
            )
        ).set_run()


def set_asset_texture_export(task_properties, force=False):
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_operators as utl_dcc_operators
    #
    import lxkatana.dcc.dcc_objects as ktn_dcc_objects
    #
    import lxkatana.fnc.exporters as ktn_fnc_exporters
    #
    workspace = task_properties.get('workspace')
    task = task_properties.get('task')
    version = task_properties.get('version')
    if workspace in ['publish'] or force is True:
        utl_dcc_operators.DccTexturesOpt(
            ktn_dcc_objects.TextureReferences(
                option=dict(
                    with_reference=False
                )
            )
        ).set_tx_repath_to_orig()
        # texture-src
        texture_src_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_src_directory(
            task=task,
            version=version
        )
        # TODO remove orig directory
        # texture-tgt
        texture_tgt_directory_path = rsv_operators.RsvAssetTextureQuery(task_properties).get_tgt_directory(
            task=task,
            version=version
        )
        #
        ktn_fnc_exporters.TextureExporter(
            option=dict(
                directory_base=texture_src_directory_path,
                directory=texture_tgt_directory_path,
                #
                fix_name_blank=True,
                use_tx=False,
                with_reference=False,
                use_environ_map=True,
            )
        ).set_run()