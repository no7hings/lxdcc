# coding:utf-8
import copy

import glob

from random import choice

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxdatabase.objects as dtb_objects

p_ = '{key}_{size}_{tag}.{ext}'


cfg_f = '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
dtb = dtb_objects.DtbResourceLib(cfg_f)

d = '/l/resource/srf/tex_lib/surfaces'

# d = '/depts/lookdev/ld_qiuhua/texture/megascans/surfaces'

fs = bsc_core.StorageDirectoryOpt(
    d
).get_all_file_paths(
    include_exts=['.json']
)


resource_dir_pattern = '/l/resource/library/texture/all/{resource_group}/{resource_name}'
d_vsn_p = resource_dir_pattern + '/{version_name}'

f_prv_p = d_vsn_p + '/image/preview.png'

f_cfg_p = d_vsn_p + '/metadata/quixel.json'

quixel_directory_p = d_vsn_p + '/quixel'

quixel_json_file_p = quixel_directory_p + '/main.json'

quixel_file_directory_p = quixel_directory_p + '/src'

texture_src_directory_p = d_vsn_p + '/texture/src'

texture_dile_p = texture_src_directory_p + '/{resource_name}.{tag}.{ext}'

semantic_tag_groups = dtb.get_entities(
    entity_type=dtb.EntityTypes.TagGroup,
    filters=[
        ('kind', 'is', dtb.Kinds.ResourceSemanticTagGroup)
    ],
    new_connection=False
)

file_tag_groups = dtb.get_entities(
    entity_type=dtb.EntityTypes.TagGroup,
    filters=[
        ('kind', 'is', dtb.Kinds.ResourceStorageTagGroup)
    ],
    new_connection=False
)

resource_dict = dict()

file_tags = set()

for i_cfg_file_path_src in fs:
    i_cfg_file_opt_src = bsc_core.StorageFileOpt(i_cfg_file_path_src)
    i_c = bsc_objects.Configure(
        value=i_cfg_file_path_src
    )
    i_directory_path_src = i_cfg_file_opt_src.directory_path
    i_d_opt_src = bsc_core.StorageDirectoryOpt(i_directory_path_src)

    i_resource_type = i_c.get('semanticTags.asset_type')

    i_key = i_cfg_file_opt_src.name_base
    i_name_ = i_c.get('name').strip()
    i_id = i_c.get('id')
    i_name = bsc_core.TextMtd.set_clear_up_to(i_name_).lower()
    i_gui_name = bsc_core.StrUnderlineOpt(i_name).to_prettify()

    i_stg_keys = i_c.get('categories')

    i_resource_name = '{}_{}'.format(i_name, i_key)
    i_version_name = 'v0001'

    i_kwargs = dict(
        resource_group=i_resource_type,
        resource_name=i_resource_name,
        version_name=i_version_name
    )

    i_resource_directory_path = resource_dir_pattern.format(**i_kwargs)

    i_stg_d_opt_tgt = bsc_core.StorageDirectoryOpt(i_resource_directory_path)

    i_stg_d_opt_tgt.set_create()

    i_version_directory_path = d_vsn_p.format(**i_kwargs)

    d_vsn_d_opt_tgt = bsc_core.StorageDirectoryOpt(i_version_directory_path)

    d_vsn_d_opt_tgt.set_create()

    i_json_file_path_tgt = quixel_json_file_p.format(**i_kwargs)

    i_cfg_file_opt_src.set_copy_to_file(i_json_file_path_tgt)

    i_prv_file_path_src = '{}/*_Preview.png'.format(i_directory_path_src)

    i_image_preview_file_path = f_prv_p.format(**i_kwargs)

    i_prv_file_paths_src = glob.glob(i_prv_file_path_src)
    if i_prv_file_paths_src:
        i_prv_file_path_src = i_prv_file_paths_src[0]
        i_prv_file_opt_src = bsc_core.StorageFileOpt(i_prv_file_path_src)
        i_prv_file_opt_src.set_copy_to_file(
            i_image_preview_file_path
        )

    i_resource_path = '/{}/{}'.format(i_resource_type, i_resource_name)
    i_version_path = '{}/{}'.format(i_resource_path, i_version_name)
    i_latest_version_path = '{}/{}'.format(i_resource_path, 'latest')

    if i_resource_path in resource_dict:
        # print resource_dict[i_resource_path], i_cfg_file_path_src
        continue
    else:
        resource_dict[i_resource_path] = i_cfg_file_path_src
    # add resource
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Resource,
        data=dict(
            kind=dtb.Kinds.Resource,
            path=i_resource_path,
            gui_name=i_gui_name
        )
    )
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Version,
        data=dict(
            kind=dtb.Kinds.ResourceVersion,
            path=i_version_path,
            gui_name=i_gui_name
        )
    )
    # add version property
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Attribute,
        data=dict(
            kind=dtb.Kinds.Resource,
            node=i_resource_path,
            port='version',
            value=i_version_path
        )
    )
    # add storages
    # version
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Attribute,
        data=dict(
            kind=dtb.Kinds.ResourceVersion,
            node=i_version_path,
            port='version-dir',
            value=i_version_directory_path
        )
    )
    #
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Attribute,
        data=dict(
            kind=dtb.Kinds.ResourceVersion,
            node=i_version_path,
            port='image-preview-png-file',
            value=i_image_preview_file_path
        )
    )
    #
    dtb.add_entity(
        entity_type=dtb.EntityTypes.Attribute,
        data=dict(
            kind=dtb.Kinds.ResourceVersion,
            node=i_version_path,
            port='image-preview-png-file',
            value=i_image_preview_file_path
        )
    )
    # resource-semantic-tag
    for i in semantic_tag_groups:
        j_tag_group_name = i.name
        j_ = i_c.get('semanticTags.{}'.format(j_tag_group_name)) or ['other']
        if j_:
            if isinstance(j_, list):
                j_tags = map(lambda x: bsc_core.TextMtd.set_clear_up_to(x.strip()).lower(), j_)
                for k_tag in j_tags:
                    if k_tag:
                        if j_tag_group_name in ['color', 'environment', 'state']:
                            k_kind = dtb.Kinds.ResourcePrimarySemanticTag
                        else:
                            k_kind = dtb.Kinds.ResourceSecondarySemanticTag
                        #
                        k_tag_path = '/{}/{}'.format(j_tag_group_name, k_tag)
                        dtb.add_entity(
                            entity_type=dtb.EntityTypes.Tags,
                            data=dict(
                                kind=k_kind,
                                #
                                node=i_resource_path,
                                value=k_tag_path
                            )
                        )
            else:
                pass
    # resource-file-tag
    i_source_directory_path_tgt = quixel_file_directory_p.format(**i_kwargs)
    p = bsc_core.ParsePatternOpt(
        '{}/{}'.format(i_directory_path_src, p_), key_format=dict(key='*', size='[0-9]K')
    )
    # p.set_update(**dict(key=i_key))
    i_matches = p.get_matches()
    if i_matches:
        i_sizes = set()
        for j in p.get_matches():
            j_kwargs = copy.copy(i_kwargs)
            j_file_path_src = j['result']
            j_file_tag = j['tag']
            j_file_tag = bsc_core.TextMtd.set_clear_up_to(j_file_tag).strip().lower()
            j['tag'] = j_file_tag
            file_tags.add(j_file_tag)

            j_kwargs.update(j)

            bsc_core.StorageFileOpt(j_file_path_src).set_copy_to_directory(
                i_source_directory_path_tgt
            )
            j_file_path_tgt = texture_dile_p.format(**j_kwargs)
            bsc_core.StorageFileOpt(j_file_path_src).set_copy_to_file(
                j_file_path_tgt
            )

            j_file_tag_path = '/texture/{}'.format(j_file_tag)

            j_size = bsc_core.OiioImageOpt(j_file_path_tgt).get_size()
            i_sizes.add(j_size)
            dtb.add_entity(
                entity_type=dtb.EntityTypes.Tags,
                data=dict(
                    kind=dtb.Kinds.ResourceFileTag,
                    #
                    node=i_resource_path,
                    value=j_file_tag_path
                )
            )

        for j_size in i_sizes:
            j_resolution = '{}x{}'.format(*j_size)
            j_tag_path = '/resolution/{}'.format(j_resolution)
            dtb.add_entity(
                entity_type=dtb.EntityTypes.Tags,
                data=dict(
                    kind=dtb.Kinds.ResourcePropertyTag,
                    #
                    node=i_resource_path,
                    value=j_tag_path
                )
            )
    else:
        print i_cfg_file_path_src
    # resource-type
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
            ],
            new_connection=False
        )
        if j_dtb_type is not None:
            # resource property
            j_unit_name = 'resource_{}_{}'.format(i_key, j_seq)
            j_unit_path = '/{}'.format(j_unit_name)
            #
            dtb.add_entity(
                entity_type=dtb.EntityTypes.Types,
                data=dict(
                    kind=dtb.Kinds.ResourceType,
                    #
                    node=i_resource_path,
                    value=j_type_path
                )
            )
        else:
            print j_type_path, 'AAAA'

dtb.accept()

