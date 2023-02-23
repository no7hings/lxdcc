# coding:utf-8
import copy

import glob

from lxbasic import bsc_core

from lxutil import utl_core

import lxbasic.objects as bsc_objects


class ScpTextureResourcesAddByQuixel(object):
    TEXTURE_PATTERN = '{texture_key}_{texture_size_tag}_{texture_type_tag}.{texture_format}'
    def __init__(self, database_opt):
        self._dtb_opt = database_opt
        self._dtb_cfg_opt = self._dtb_opt.get_database_configure_opt()

        self._resource_dict = dict()
        self._file_tags = set()

    def add_resources_from(self, directory_path_src):
        json_files = bsc_core.StgDirectoryOpt(
            directory_path_src
        ).get_all_file_paths(
            include_exts=['.json']
        )

        self._resource_dict = dict()
        self._file_tags = set()

        with utl_core.LogProgressRunner.create_as_bar(maximum=len(json_files), label='add resource') as l_p:
            for i_json_file_path in json_files:
                l_p.set_update()
                #
                self.add_resource_by_quixel_json(i_json_file_path)

        self._dtb_opt.accept()

    def accept(self):
        self._dtb_opt.accept()

    def add_resource_by_quixel_json(self, quixel_json_file_path):
        """
        :param quixel_json_file_path: <file-path>
        :return: None
        """
        quixel_json_file_opt = bsc_core.StgFileOpt(quixel_json_file_path)
        quixel_json_content = bsc_objects.Configure(
            value=quixel_json_file_path
        )
        directory_path_src = quixel_json_file_opt.directory_path

        category_group = quixel_json_content.get('semanticTags.asset_type')

        resource_id = quixel_json_file_opt.name_base
        resource_key = bsc_core.RawTextMtd.set_clear_up_to(quixel_json_content.get('name').strip()).lower()
        resource_gui_name = bsc_core.RawStringUnderlineOpt(resource_key).to_prettify()

        resource_name = '{}_{}'.format(resource_key, resource_id)
        version_name = 'v0001'
        version_gui_name = version_name

        pattern_kwargs = dict(
            category_group=category_group,
            resource=resource_name,
            version=version_name
        )
        # create resource directory
        resource_directory_path = self.__stg_add_resource_(pattern_kwargs)
        # create version directory
        version_directory_path = self.__stg_add_version_(pattern_kwargs)
        # copy json file
        quixel_json_file_path_tgt = self.__stg_add_quixel_metadata_json_file_(pattern_kwargs, quixel_json_file_opt)
        # copy preview file
        image_preview_file_path_tgt = self.__stg_add_image_preview_file_(pattern_kwargs, directory_path_src)
        #
        resource_path = '/{}/{}'.format(category_group, resource_name)
        version_path = '{}/{}'.format(resource_path, version_name)
        #
        if resource_path in self._resource_dict:
            utl_core.Log.set_module_warning_trace(
                'add resource', '"{}" is same to "{}", ignore add'.format(
                    quixel_json_file_path, self._resource_dict[resource_path]
                )
            )
            return
        else:
            self._resource_dict[resource_path] = quixel_json_file_path
        # add resource
        # add resource to database
        self.__dtb_add_resource_(
            resource_path, resource_gui_name,
            # properties
            version_path,
            # storage properties
            resource_directory_path,
        )
        # add resource types to database
        self.__dtb_add_resource_types_(
            resource_path,
            quixel_json_content
        )
        # add resource tags to database
        self.__dtb_add_resource_tags_(
            resource_path,
            quixel_json_content
        )
        # add version
        # add version to database
        self.__dtb_add_resource_version_(
            resource_path, version_path,
            # storage properties
            version_directory_path, quixel_json_file_path_tgt, image_preview_file_path_tgt,
        )
        self.__stg_add_version_directories_(
            pattern_kwargs,
            version_path
        )
        self.__dtb_add_version_storage_properties_(
            pattern_kwargs,
            version_path,
        )
        # add version textures to storage and database
        self.__stg_and_dtb_add_version_textures_(
            pattern_kwargs,
            resource_path, version_path,
            directory_path_src
        )
    # add resource
    def __stg_add_resource_(self, pattern_kwargs):
        pattern_opt = self._dtb_opt.get_pattern_opt('resource-dir')
        path = pattern_opt.set_update_to(**pattern_kwargs).get_value()
        path_opt = bsc_core.StgDirectoryOpt(path)
        path_opt.set_create()
        return path

    def __dtb_add_resource_(self, resource_path, resource_gui_name, version_path, resource_directory_path):
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Resource,
            data=dict(
                kind=self._dtb_opt.Kinds.Resource,
                path=resource_path,
                gui_name=resource_gui_name
            )
        )
        # add properties
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            data=dict(
                kind=self._dtb_opt.Kinds.Resource,
                node=resource_path,
                port='version',
                value=version_path
            )
        )
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            data=dict(
                kind=self._dtb_opt.Kinds.Resource,
                node=resource_path,
                port='location',
                value=resource_directory_path
            )
        )

    def __dtb_add_resource_types_(self, resource_path, quixel_json_content):
        keys = quixel_json_content.get_keys('assetCategories.*.*.*')
        for i_key in keys:
            i_args = i_key.split('.')
            i_args = [bsc_core.RawTextMtd.set_clear_up_to(i).lower() for i in i_args]

            i_types = i_args[1:]

            i_type_path = '/' + '/'.join(i_types)

            i_dtb_type = self._dtb_opt.get_entity(
                entity_type=self._dtb_opt.EntityTypes.Type,
                filters=[
                    ('path', 'is', i_type_path)
                ],
                new_connection=False
            )
            if i_dtb_type is not None:
                # resource property
                self._dtb_opt.add_entity(
                    entity_type=self._dtb_opt.EntityTypes.Types,
                    data=dict(
                        kind=self._dtb_opt.Kinds.ResourceType,
                        #
                        node=resource_path,
                        value=i_type_path
                    )
                )
            else:
                utl_core.Log.set_module_warning_trace(
                    'add resource', 'type="{}" is not register in database'.format(i_type_path)
                )

    def __dtb_add_resource_tags_(self, resource_path, quixel_json_content):
        # add semantic tags
        semantic_tag_groups = self._dtb_opt.get_entities(
            entity_type=self._dtb_opt.EntityTypes.TagGroup,
            filters=[
                ('kind', 'is', self._dtb_opt.Kinds.ResourceSemanticTagGroup)
            ],
            new_connection=False
        )
        for i in semantic_tag_groups:
            j_tag_group_name = i.name
            j_ = quixel_json_content.get('semanticTags.{}'.format(j_tag_group_name)) or ['other']
            if j_:
                if isinstance(j_, list):
                    j_tags = map(lambda x: bsc_core.RawTextMtd.set_clear_up_to(x.strip()).lower(), j_)
                    for k_tag in j_tags:
                        if k_tag:
                            if j_tag_group_name in ['color', 'environment', 'state']:
                                k_kind = self._dtb_opt.Kinds.ResourcePrimarySemanticTag
                            else:
                                k_kind = self._dtb_opt.Kinds.ResourceSecondarySemanticTag
                            #
                            k_tag_path = '/{}/{}'.format(j_tag_group_name, k_tag)
                            self._dtb_opt.add_entity(
                                entity_type=self._dtb_opt.EntityTypes.Tags,
                                data=dict(
                                    kind=k_kind,
                                    #
                                    node=resource_path,
                                    value=k_tag_path
                                )
                            )
                else:
                    pass
        # add other tags
    # add version
    def __stg_add_version_(self, pattern_kwargs):
        pattern_opt = self._dtb_opt.get_pattern_opt('version-dir')
        path = pattern_opt.set_update_to(**pattern_kwargs).get_value()
        path_opt = bsc_core.StgDirectoryOpt(path)
        path_opt.set_create()
        return path

    def __dtb_add_resource_version_(self, resource_path, version_path, version_directory_path, quixel_json_file_path_tgt, image_preview_file_path_tgt):
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Version,
            data=dict(
                kind=self._dtb_opt.Kinds.Version,
                path=version_path
            )
        )
        # add properties
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            data=dict(
                kind=self._dtb_opt.Kinds.Version,
                node=version_path,
                port='location',
                value=version_directory_path
            )
        )
        #
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            data=dict(
                kind=self._dtb_opt.Kinds.Version,
                node=version_path,
                port='resource',
                value=resource_path
            )
        )
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            data=dict(
                kind=self._dtb_opt.Kinds.Version,
                node=version_path,
                port='quixel_json_file',
                value=quixel_json_file_path_tgt
            )
        )
        #
        self._dtb_opt.add_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            data=dict(
                kind=self._dtb_opt.Kinds.Version,
                node=version_path,
                port='image_preview_file',
                value=image_preview_file_path_tgt
            )
        )

    def __dtb_add_version_storage_properties_(self, pattern_kwargs, version_path):
        add_args = [
            ('image_directory', 'image-dir'),
            ('image_preview_file', 'image-preview-png-file'),
            #
            ('quixel_directory', 'quixel-dir'),
            ('quixel_json_file', 'quixel-metadata-json-file'),
            #
            ('texture_directory', 'texture-dir'),
        ]
        for i_port, i_keyword in add_args:
            i_pattern_opt = self._dtb_opt.get_pattern_opt(i_keyword)
            i_path = i_pattern_opt.set_update_to(**pattern_kwargs).get_value()
            self._dtb_opt.add_entity(
                entity_type=self._dtb_opt.EntityTypes.Attribute,
                data=dict(
                    kind=self._dtb_opt.Kinds.Version,
                    node=version_path,
                    port=i_port,
                    value=i_path
                )
            )

    def __stg_add_quixel_metadata_json_file_(self, pattern_kwargs, file_opt_src):
        pattern_opt = self._dtb_opt.get_pattern_opt('quixel-metadata-json-file')
        path = pattern_opt.set_update_to(**pattern_kwargs).get_value()
        file_opt_src.set_copy_to_file(path)
        return path

    def __stg_add_image_preview_file_(self, pattern_kwargs, directory_path_src):
        quixel_image_png_file_pattern_opt = self._dtb_opt.get_pattern_opt('quixel-image-png-file')
        quixel_image_png_file_path = quixel_image_png_file_pattern_opt.set_update_to(**pattern_kwargs).get_value()
        image_preview_png_file_pattern_opt = self._dtb_opt.get_pattern_opt('image-preview-png-file')
        image_preview_png_file_path = image_preview_png_file_pattern_opt.set_update_to(**pattern_kwargs).get_value()
        file_path_glog_pattern_src = '{}/*_Preview.png'.format(directory_path_src)
        file_paths_src = glob.glob(file_path_glog_pattern_src)
        if file_paths_src:
            file_path_src = file_paths_src[0]
            file_opt_src = bsc_core.StgFileOpt(file_path_src)
            file_opt_src.set_copy_to_file(quixel_image_png_file_path)
            file_opt_src.set_copy_to_file(image_preview_png_file_path)
        return image_preview_png_file_path

    def __stg_and_dtb_add_version_textures_(self, pattern_kwargs, resource_path, version_path, directory_path_src):
        quixel_texture_directory_p_opt = self._dtb_opt.get_pattern_opt('quixel-texture-dir')
        texture_original_src_file_p_opt = self._dtb_opt.get_pattern_opt('texture-original-src-file')
        #
        quixel_texture_directory_path = quixel_texture_directory_p_opt.set_update_to(**pattern_kwargs).get_value()
        texture_pattern = bsc_core.PtnParseOpt(
            '{}/{}'.format(directory_path_src, self.TEXTURE_PATTERN),
            key_format=dict(texture_key='*', texture_size_tag='[0-9]K')
        )
        texture_matches = texture_pattern.get_matches()
        if texture_matches:
            texture_sizes = set()
            for i_texture_variants in texture_pattern.get_matches():
                i_pattern_kwargs = copy.copy(pattern_kwargs)
                j_file_path_src = i_texture_variants['result']
                # fix texture tag
                i_texture_type_tag = i_texture_variants['texture_type_tag']
                i_texture_type_tag = bsc_core.RawTextMtd.set_clear_up_to(i_texture_type_tag).strip().lower()
                i_texture_variants['texture_type_tag'] = i_texture_type_tag
                self._file_tags.add(i_texture_type_tag)

                i_pattern_kwargs.update(i_texture_variants)

                bsc_core.StgFileOpt(j_file_path_src).set_copy_to_directory(
                    quixel_texture_directory_path
                )
                #
                texture_original_src_file_path = texture_original_src_file_p_opt.set_update_to(**i_pattern_kwargs).get_value()
                bsc_core.StgFileOpt(j_file_path_src).set_copy_to_file(
                    texture_original_src_file_path
                )

                i_texture_type_tag_path = '/texture/{}'.format(i_texture_type_tag)

                # self.__stg_add_version_file_(i_pattern_kwargs, version_path)

                i_texture_size = bsc_core.ImgFileOiioOpt(texture_original_src_file_path).get_size()
                texture_sizes.add(i_texture_size)
                self._dtb_opt.add_entity(
                    entity_type=self._dtb_opt.EntityTypes.Tags,
                    data=dict(
                        kind=self._dtb_opt.Kinds.ResourceFileTag,
                        #
                        node=resource_path,
                        value=i_texture_type_tag_path
                    )
                )
            # property tag
            for i_texture_size in texture_sizes:
                i_resource_tag = '{}x{}'.format(*i_texture_size)
                i_resource_tag_path = '/resolution/{}'.format(i_resource_tag)
                self._dtb_opt.add_entity(
                    entity_type=self._dtb_opt.EntityTypes.Tags,
                    data=dict(
                        kind=self._dtb_opt.Kinds.ResourcePropertyTag,
                        #
                        node=resource_path,
                        value=i_resource_tag_path
                    )
                )
        else:
            utl_core.Log.set_module_warning_trace(
                'add resource', 'resource="{}" has no texture found'.format(resource_path)
            )
    # add directory
    def __stg_add_version_directories_(self, pattern_kwargs, version_path):
        add_mapper = self._dtb_cfg_opt.get('version-storage.directory')
        kind = self._dtb_opt.Kinds.Directory
        for k, v in add_mapper.items():
            i_storage_path = '{}{}'.format(version_path, k)
            self._dtb_opt.add_entity(
                entity_type=self._dtb_opt.EntityTypes.Storage,
                data=dict(
                    kind=kind,
                    path=i_storage_path,
                )
            )
            #
            i_keyword = v
            i_pattern_opt = self._dtb_opt.get_pattern_opt(i_keyword)
            i_directory_path = i_pattern_opt.set_update_to(**pattern_kwargs).get_value()
            #
            self._dtb_opt.add_entity(
                entity_type=self._dtb_opt.EntityTypes.Attribute,
                data=dict(
                    kind=kind,
                    node=i_storage_path,
                    port='location',
                    value=i_directory_path
                )
            )
            self._dtb_opt.add_entity(
                entity_type=self._dtb_opt.EntityTypes.Attribute,
                data=dict(
                    kind=kind,
                    node=i_storage_path,
                    port='version',
                    value=version_path
                )
            )

    def __stg_add_version_file_(self, pattern_kwargs, version_path):
        storage_path = version_path + '/texture/original/src/{texture_type_tag}'.format(
            **pattern_kwargs
        )
        print storage_path
        file_path = ''
        # kind = self._dtb_opt.Kinds.File
        # self._dtb_opt.add_entity(
        #     entity_type=self._dtb_opt.EntityTypes.Storage,
        #     data=dict(
        #         kind=kind,
        #         path=storage_path,
        #     )
        # )
        # self._dtb_opt.add_entity(
        #     entity_type=self._dtb_opt.EntityTypes.Attribute,
        #     data=dict(
        #         kind=kind,
        #         node=storage_path,
        #         port='location',
        #         value=file_path
        #     )
        # )
        # self._dtb_opt.add_entity(
        #     entity_type=self._dtb_opt.EntityTypes.Attribute,
        #     data=dict(
        #         kind=kind,
        #         node=storage_path,
        #         port='version',
        #         value=version_path
        #     )
        # )

    def _test_(self):
        pass


class ScpTextureResourceData(object):
    def __init__(self, directory_path):
        self._directory_path = directory_path

    def get_data(self):
        dict_ = {}
        directory_opt = bsc_core.StgDirectoryOpt(self._directory_path)

        texture_paths = directory_opt.get_all_file_paths(include_exts=['.tx'])

        p = bsc_core.PtnParseOpt(
            '{name}.{key}'
        )

        for i_texture_path in texture_paths:
            i_texture_opt = bsc_core.StgFileOpt(i_texture_path)
            i_name_base = i_texture_opt.name_base

            i_variants = p.get_variants(i_name_base)
            if i_variants:
                i_key = i_variants['key']
                dict_[i_key] = i_texture_opt.get_path()

        return dict_


if __name__ == '__main__':
    import lxdatabase.objects as dtb_objects
    scp = ScpTextureResourcesAddByQuixel(
        database_opt=dtb_objects.DtbResourceLibraryOpt(
            '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/dtb-library-basic.yml'
        )
    )
    scp.add_resources_from(
        '/l/resource/srf/tex_lib/surfaces'
    )

    # scp = ScpTextureResourceData(
    #     '/l/resource/library/texture/all/surface/concrete_damaged_pkngj0/v0001/texture/acescg/tx'
    # )
    #
    # print scp.get_data()
