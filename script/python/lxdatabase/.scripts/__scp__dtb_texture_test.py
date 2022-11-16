# coding:utf-8
import glob

from random import choice

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxdatabase.objects as dtb_objects

cfg_f = '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
dtb = dtb_objects.DtbResourceLib(cfg_f)

fs = bsc_core.StorageDirectoryOpt(
    '/depts/lookdev/ld_qiuhua/texture/megascans/surfaces'
).get_all_file_paths(
    include_exts=['.json']
)

d_stg_p = '/l/resource/library/texture/all/{resource_type}/{resource_name}'
d_vsn_p = d_stg_p + '/{version_name}'

d_prv_p = d_vsn_p + '/preview/default.png'

d_cfg_p = d_vsn_p + '/metadata/quixel.json'

for i_cfg_file_path_src in fs:
    i_cfg_file_opt_src = bsc_core.StorageFileOpt(i_cfg_file_path_src)
    i_c = bsc_objects.Configure(
        value=i_cfg_file_path_src
    )
    i_d_path_src = i_cfg_file_opt_src.directory_path
    i_d_opt_src = bsc_core.StorageDirectoryOpt(i_d_path_src)

    i_resource_type = i_c.get('semanticTags.asset_type')

    i_key = i_cfg_file_opt_src.name_base
    i_gui_name = i_c.get('name').strip()
    i_id = i_c.get('id')
    i_name = bsc_core.TextMtd.set_clear_up_to(i_gui_name).lower()
    i_gui_name = bsc_core.StrUnderlineOpt(i_name).to_prettify()

    i_stg_keys = i_c.get('categories')

    i_resource_name = i_name
    i_version_name = 'v0001'

    i_kwargs = dict(
        resource_type=i_resource_type,
        resource_name=i_resource_name,
        version_name=i_version_name
    )

    i_stg_d_path_tgt = d_stg_p.format(**i_kwargs)

    i_stg_d_opt_tgt = bsc_core.StorageDirectoryOpt(i_stg_d_path_tgt)

    i_stg_d_opt_tgt.set_create()

    i_vsn_d_path_tgt = d_vsn_p.format(**i_kwargs)

    d_vsn_d_opt_tgt = bsc_core.StorageDirectoryOpt(i_vsn_d_path_tgt)

    d_vsn_d_opt_tgt.set_create()

    i_cfg_file_path_tgt = d_cfg_p.format(**i_kwargs)

    i_cfg_file_opt_src.set_copy_to_file(i_cfg_file_path_tgt)

    i_prv_file_path_src = '{}/*_Preview.png'.format(i_d_path_src)

    i_prv_file_path_tgt = d_prv_p.format(**i_kwargs)

    i_resource_path = '/{}'.format(i_resource_name)
    i_version_path = '/{}/{}'.format(i_resource_name, i_version_name)
    # add resource
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Resource,
        #
        path=i_resource_path,
        version=i_version_path,
        #
        gui_name=i_gui_name
    )
    # add version
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Version,
        #
        path=i_version_path,
        resource=i_resource_path,
        #
        image=i_prv_file_path_tgt,
        location=i_vsn_d_path_tgt
    )
    # add tag
    key = 'state'
    i_tags = i_c.get('semanticTags.state') or []
    i_tags = map(lambda x: bsc_core.TextMtd.set_clear_up_to(x.strip()).lower(), i_tags)
    for j_tag in i_tags:
        j_tag_path = '/{}/{}'.format(key, j_tag)
        dtb.add_entity(
            entity_type=dtb.EntityTypes.ResourceTag,
            #
            path=i_resource_path + j_tag_path,
            #
            resource=i_resource_path,
            #
            tag=j_tag_path
        )

    key = 'color'
    i_tags = i_c.get('semanticTags.color') or []
    i_tags = map(lambda x: bsc_core.TextMtd.set_clear_up_to(x.strip()).lower(), i_tags)
    for j_tag in i_tags:
        j_tag_path = '/{}/{}'.format(key, j_tag)
        dtb.add_entity(
            entity_type=dtb.EntityTypes.ResourceTag,
            #
            path=i_resource_path + j_tag_path,
            #
            resource=i_resource_path,
            #
            tag=j_tag_path
        )

    key = 'environment'
    i_tags = i_c.get('semanticTags.environment') or []
    i_tags = map(lambda x: bsc_core.TextMtd.set_clear_up_to(x.strip()).lower(), i_tags)
    for j_tag in i_tags:
        j_tag_path = '/{}/{}'.format(key, j_tag)
        dtb.add_entity(
            entity_type=dtb.EntityTypes.ResourceTag,
            #
            path=i_resource_path + j_tag_path,
            #
            resource=i_resource_path,
            #
            tag=j_tag_path
        )

    key = 'theme'
    i_tags = i_c.get('semanticTags.theme') or []
    i_tags = map(lambda x: bsc_core.TextMtd.set_clear_up_to(x.strip()).lower(), i_tags)
    for j_tag in i_tags:
        j_tag_path = '/{}/{}'.format(key, j_tag)
        dtb.add_entity(
            entity_type=dtb.EntityTypes.ResourceTag,
            #
            path=i_resource_path + j_tag_path,
            #
            resource=i_resource_path,
            #
            tag=j_tag_path
        )

    i_prv_file_paths_src = glob.glob(i_prv_file_path_src)
    if i_prv_file_paths_src:
        i_prv_file_path_src = i_prv_file_paths_src[0]
        i_prv_file_opt_src = bsc_core.StorageFileOpt(i_prv_file_path_src)
        i_prv_file_opt_src.set_copy_to_file(
            i_prv_file_path_tgt
        )

    i_keys = i_c.get_keys('assetCategories.*.*.*')
    for j_seq, j_key in enumerate(i_keys):
        j_ = j_key.split('.')
        j_ = [bsc_core.TextMtd.set_clear_up_to(i).lower() for i in j_]

        j_type_keys = j_[1:]

        j_type_path = '/' + '/'.join(j_type_keys)

        j_dtb_type = dtb.get_entity(
            entity_type=dtb.EntityTypes.Type,
            filters=[
                ('path', 'is', j_type_path)
            ]
        )

        j_resource_index = dtb.get_entity_index(
            entity_type=dtb.EntityTypes.Unit,
            new_connection=False
        )

        j_resource_name = 'resource_{}_{}'.format(i_key, j_seq)
        j_resource_path = '/{}'.format(j_resource_name)

        dtb.add_entity(
            entity_type=dtb.EntityTypes.Unit,
            #
            path=j_resource_path,
            #
            type=j_type_path,
            #
            gui_name=j_resource_name,
            #
            resource=i_resource_path,
        )

    dtb.accept()



