# coding:utf-8
import copy

import glob

from lxbasic import bsc_core

from lxutil import utl_core

import lxbasic.objects as bsc_objects

import lxdatabase.objects as dtb_objects

p_ = '{key}_{size}_{texture_tag}.{texture_format}'

dtb = dtb_objects.DtbResourceLibraryOpt('/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/dtb-library-basic.yml')


class _AddByQuixelScript(object):
    def __init__(self, database):
        self._dtb = database

    def add_resources_from(self, directory_path_src):
        json_files = bsc_core.StorageDirectoryOpt(
            directory_path_src
        ).get_all_file_paths(
            include_exts=['.json']
        )

        resource_directory_p = '/l/resource/library/texture/all/{category_group}/{resource}'
        version_directory_p = resource_directory_p + '/{version}'
        image_preview_png_file_p = version_directory_p + '/image/preview.png'
        quixel_directory_p = version_directory_p + '/quixel'
        quixel_json_file_p = quixel_directory_p + '/main.json'
        quixel_texture_directory_p = quixel_directory_p + '/src'

        texture_original_src_dir_p = version_directory_p + '/texture/src'

        texture_dile_p = texture_original_src_dir_p + '/{resource}.{texture_tag}.{texture_format}'

        semantic_tag_groups = self._dtb.get_entities(
            entity_type=self._dtb.EntityTypes.TagGroup,
            filters=[
                ('kind', 'is', self._dtb.Kinds.ResourceSemanticTagGroup)
            ],
            new_connection=False
        )

        resource_dict = dict()
        file_tags = set()

        with utl_core.log_progress_bar(maximum=len(json_files), label='add resource from quixel') as l_p:
            for i_cfg_file_path_src in json_files:
                l_p.set_update()
                #
                i_cfg_file_opt_src = bsc_core.StorageFileOpt(i_cfg_file_path_src)
                i_c_src = bsc_objects.Configure(
                    value=i_cfg_file_path_src
                )
                i_directory_path_src = i_cfg_file_opt_src.directory_path

                i_resource_type = i_c_src.get('semanticTags.asset_type')

                i_key = i_cfg_file_opt_src.name_base
                i_name_ = i_c_src.get('name').strip()

                i_name = bsc_core.TextMtd.set_clear_up_to(i_name_).lower()
                i_gui_name = bsc_core.StrUnderlineOpt(i_name).to_prettify()

                i_resource_name = '{}_{}'.format(i_name, i_key)
                i_version_name = 'v0001'

                i_resource_kwargs = dict(
                    category_group=i_resource_type,
                    resource=i_resource_name,
                    version=i_version_name
                )

                i_resource_directory_path_tgt = resource_directory_p.format(**i_resource_kwargs)

                i_resource_directory_path_opt_tgt = bsc_core.StorageDirectoryOpt(i_resource_directory_path_tgt)

                i_resource_directory_path_opt_tgt.set_create()

                i_version_directory_path = version_directory_p.format(**i_resource_kwargs)

                d_vsn_d_opt_tgt = bsc_core.StorageDirectoryOpt(i_version_directory_path)

                d_vsn_d_opt_tgt.set_create()

                i_json_file_path_tgt = quixel_json_file_p.format(**i_resource_kwargs)

                i_cfg_file_opt_src.set_copy_to_file(i_json_file_path_tgt)

                i_prv_file_path_src = '{}/*_Preview.png'.format(i_directory_path_src)

                i_image_preview_png_file_path_tgt = image_preview_png_file_p.format(**i_resource_kwargs)

                i_prv_file_paths_src = glob.glob(i_prv_file_path_src)
                if i_prv_file_paths_src:
                    i_prv_file_path_src = i_prv_file_paths_src[0]
                    i_prv_file_opt_src = bsc_core.StorageFileOpt(i_prv_file_path_src)
                    i_prv_file_opt_src.set_copy_to_file(
                        i_image_preview_png_file_path_tgt
                    )

                i_resource_path = '/{}/{}'.format(i_resource_type, i_resource_name)
                i_version_path = '{}/{}'.format(i_resource_path, i_version_name)

                if i_resource_path in resource_dict:
                    # print resource_dict[i_resource_path], i_cfg_file_path_src
                    continue
                else:
                    resource_dict[i_resource_path] = i_cfg_file_path_src
                # add resource
                self._dtb.add_entity(
                    entity_type=self._dtb.EntityTypes.Resource,
                    data=dict(
                        kind=self._dtb.Kinds.Resource,
                        path=i_resource_path,
                        gui_name=i_gui_name
                    )
                )
                self._dtb.add_entity(
                    entity_type=self._dtb.EntityTypes.Version,
                    data=dict(
                        kind=self._dtb.Kinds.ResourceVersion,
                        path=i_version_path,
                        gui_name=i_gui_name
                    )
                )
                # add version property
                self._dtb.add_entity(
                    entity_type=self._dtb.EntityTypes.Attribute,
                    data=dict(
                        kind=self._dtb.Kinds.Resource,
                        node=i_resource_path,
                        port='version',
                        value=i_version_path
                    )
                )
                # add storages
                # version
                self._dtb.add_entity(
                    entity_type=self._dtb.EntityTypes.Attribute,
                    data=dict(
                        kind=self._dtb.Kinds.ResourceVersion,
                        node=i_version_path,
                        port='version-dir',
                        value=i_version_directory_path
                    )
                )
                #
                self._dtb.add_entity(
                    entity_type=self._dtb.EntityTypes.Attribute,
                    data=dict(
                        kind=self._dtb.Kinds.ResourceVersion,
                        node=i_version_path,
                        port='image-preview-png-file',
                        value=i_image_preview_png_file_path_tgt
                    )
                )
                #
                self._dtb.add_entity(
                    entity_type=self._dtb.EntityTypes.Attribute,
                    data=dict(
                        kind=self._dtb.Kinds.ResourceVersion,
                        node=i_version_path,
                        port='image-preview-png-file',
                        value=i_image_preview_png_file_path_tgt
                    )
                )
                # resource-semantic-tag
                for i in semantic_tag_groups:
                    j_tag_group_name = i.name
                    j_ = i_c_src.get('semanticTags.{}'.format(j_tag_group_name)) or ['other']
                    if j_:
                        if isinstance(j_, list):
                            j_tags = map(lambda x: bsc_core.TextMtd.set_clear_up_to(x.strip()).lower(), j_)
                            for k_tag in j_tags:
                                if k_tag:
                                    if j_tag_group_name in ['color', 'environment', 'state']:
                                        k_kind = self._dtb.Kinds.ResourcePrimarySemanticTag
                                    else:
                                        k_kind = self._dtb.Kinds.ResourceSecondarySemanticTag
                                    #
                                    k_tag_path = '/{}/{}'.format(j_tag_group_name, k_tag)
                                    self._dtb.add_entity(
                                        entity_type=self._dtb.EntityTypes.Tags,
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
                i_source_directory_path_tgt = quixel_texture_directory_p.format(**i_resource_kwargs)
                p = bsc_core.ParsePatternOpt(
                    '{}/{}'.format(i_directory_path_src, p_), key_format=dict(key='*', size='[0-9]K')
                )
                # p.set_update(**dict(key=i_key))
                i_matches = p.get_matches()
                if i_matches:
                    i_sizes = set()
                    for j in p.get_matches():
                        j_kwargs = copy.copy(i_resource_kwargs)
                        j_file_path_src = j['result']
                        j_file_tag = j['texture_tag']
                        j_file_tag = bsc_core.TextMtd.set_clear_up_to(j_file_tag).strip().lower()
                        j['texture_tag'] = j_file_tag
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
                        self._dtb.add_entity(
                            entity_type=self._dtb.EntityTypes.Tags,
                            data=dict(
                                kind=self._dtb.Kinds.ResourceFileTag,
                                #
                                node=i_resource_path,
                                value=j_file_tag_path
                            )
                        )

                    for j_size in i_sizes:
                        j_resolution = '{}x{}'.format(*j_size)
                        j_tag_path = '/resolution/{}'.format(j_resolution)
                        self._dtb.add_entity(
                            entity_type=self._dtb.EntityTypes.Tags,
                            data=dict(
                                kind=self._dtb.Kinds.ResourcePropertyTag,
                                #
                                node=i_resource_path,
                                value=j_tag_path
                            )
                        )
                else:
                    print i_cfg_file_path_src
                # resource-type
                i_keys = i_c_src.get_keys('assetCategories.*.*.*')
                for j_seq, j_key in enumerate(i_keys):
                    j_ = j_key.split('.')
                    j_ = [bsc_core.TextMtd.set_clear_up_to(i).lower() for i in j_]

                    j_type_keys = j_[1:]

                    j_type_path = '/' + '/'.join(j_type_keys)

                    j_dtb_type = self._dtb.get_entity(
                        entity_type=self._dtb.EntityTypes.Type,
                        filters=[
                            ('path', 'is', j_type_path)
                        ],
                        new_connection=False
                    )
                    if j_dtb_type is not None:
                        # resource property
                        self._dtb.add_entity(
                            entity_type=self._dtb.EntityTypes.Types,
                            data=dict(
                                kind=self._dtb.Kinds.ResourceType,
                                #
                                node=i_resource_path,
                                value=j_type_path
                            )
                        )
                    else:
                        print j_type_path, 'AAAA'

        self._dtb.accept()


if __name__ == '__main__':
    _AddByQuixelScript(dtb).add_resources_from(
        directory_path_src='/l/resource/srf/tex_lib/surfaces'
    )

