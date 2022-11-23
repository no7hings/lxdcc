# coding:utf-8
import collections

import copy

import os

from lxbasic import bsc_core

from lxdatabase import dtb_core

import lxbasic.objects as bsc_objects


class DtbBase(object):
    PATHSEP = '/'

    class EntityCategories(object):
        Type = 'dtb_type'
        #
        Tag = 'dtb_tag'
        #
        Node = 'dtb_node'
        #
        Port = 'dtb_port'
        Assign = 'dtb_assign'
        Connection = 'dtb_connection'
        #
        All = [
            Type, Tag,
            #
            Node,
            #
            Port, Assign, Connection
        ]

    class EntityTypes(object):
        # type
        CategoryGroup = 'category_group'
        Category = 'category'
        Type = 'type'
        # tag
        TagGroup = 'tag_group'
        Tag = 'tag'
        # node
        Resource = 'resource'
        Version = 'version'
        #
        Attribute = 'attribute'
        Connection = 'connection'
        #
        Assign = 'assign'
        #
        Types = 'types'
        Tags = 'tags'

    class Kinds(object):
        # category
        ResourceCategoryGroup = 'resource-category-group'
        ResourceCategory = 'resource-category'
        ResourceType = 'resource-type'
        # tag group
        ResourceSemanticTagGroup = 'resource-semantic-tag-group'
        ResourceUserTagGroup = 'resource-user-tag-group'
        ResourcePropertyTagGroup = 'resource-property-tag-group'
        ResourceStorageTagGroup = 'resource-storage-tag-group'
        # tag
        ResourcePrimarySemanticTag = 'resource-primary-semantic-tag'
        ResourceSecondarySemanticTag = 'resource-secondary-semantic-tag'
        ResourcePropertyTag = 'resource-property-tag'
        ResourceUserTag = 'resource-user-tag'
        ResourceFileTag = 'resource-file-tag'
        # resource
        Resource = 'resource'
        ResourceVersion = 'resource-version'

    EntityTypeCategoryMapper = {
        EntityTypes.CategoryGroup: EntityCategories.Type,
        EntityTypes.Category: EntityCategories.Type,
        EntityTypes.Type: EntityCategories.Type,
        #
        EntityTypes.TagGroup: EntityCategories.Tag,
        EntityTypes.Tag: EntityCategories.Tag,
        #
        EntityTypes.Resource: EntityCategories.Node,
        EntityTypes.Version: EntityCategories.Node,
        #
        EntityTypes.Attribute: EntityCategories.Port,
        EntityTypes.Connection: EntityCategories.Connection,
        #
        EntityTypes.Assign: EntityCategories.Assign,
        EntityTypes.Types: EntityCategories.Assign,
        EntityTypes.Tags: EntityCategories.Assign,
    }

    def __init__(self, database):
        if not database:
            raise RuntimeError()

        # if os.path.isfile(database) is False:
        #     raise RuntimeError()

        self._dtb_file_path = database
        self._dtb_file_opt = bsc_core.StorageFileOpt(
            database
        )
        self._dtb_file_opt.set_directory_create()

        self._dtb_opt = dtb_core.DtbSqlConnectionOpt.create_from_database(
            self._dtb_file_opt.get_path()
        )

    def get_database(self):
        return self._dtb_file_path

    database = property(get_database)

    def accept(self):
        self._dtb_opt.accept()
    # utility
    def add_entity(self, entity_type, data):
        entity_category = self.EntityTypeCategoryMapper[entity_type]
        if entity_category in [self.EntityCategories.Assign]:
            value = data['value']
            node = data['node']
            path = '{}->{}'.format(node, value)
            data['path'] = path
        #
        elif entity_category in [self.EntityCategories.Port]:
            node = data['node']
            port = data['port']
            path = '{}.{}'.format(node, port)
            data['path'] = path
        else:
            if 'path' in data:
                path = data.get('path')
                if path.startswith('/'):
                    path_opt = bsc_core.DccPathDagOpt(path)
                    group = path_opt.get_parent_path()
                    data['group'] = group
                    name = path_opt.get_name()
                    data['name'] = name
                else:
                    data['name'] = path
            else:
                group = data['group']
                if group == '/':
                    path = '/{name}'.format(**data)
                else:
                    path = '{group}/{name}'.format(**data)
                data['path'] = path
        #
        data['entity_category'] = entity_category
        data['entity_type'] = entity_type
        table_opt = self._dtb_opt.get_table_opt(entity_category)
        return table_opt.add(**data)

    def get_entity(self, entity_type, filters, new_connection=True):
        entity_category = self.EntityTypeCategoryMapper[entity_type]
        table_opt = self._dtb_opt.get_table_opt(entity_category)
        if isinstance(filters, list):
            filters.append(
                ('entity_type', 'is', entity_type)
            )
        return table_opt.get_one(
            filters=filters,
            new_connection=new_connection,
        )

    def get_entities(self, entity_type, filters=None, new_connection=True):
        entity_category = self.EntityTypeCategoryMapper[entity_type]
        table_opt = self._dtb_opt.get_table_opt(entity_category)
        if isinstance(filters, list):
            filters.append(
                ('entity_type', 'is', entity_type)
            )
        return table_opt.get_all(
            filters=filters,
            new_connection=new_connection
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.accept()


class DtbResourceLib(DtbBase):
    def __init__(self, configure_file_path):
        self._dtb_cfg = bsc_objects.Configure(value=configure_file_path)

        self._dtb_cfg.set_flatten()

        self._dtb_kwargs = {}
        if bsc_core.SystemMtd.get_is_linux():
            self._dtb_kwargs['root'] = self._dtb_cfg.get(
                'option.variants.root-linux'
            )
        elif bsc_core.SystemMtd.get_is_windows():
            self._dtb_kwargs['root'] = self._dtb_cfg.get(
                'option.variants.root-windows'
            )
        else:
            raise NotImplementedError()
        #
        db_file_pattern = self._dtb_cfg.get('patterns.database-file')
        if db_file_pattern is None:
            return

        super(DtbResourceLib, self).__init__(
            db_file_pattern.format(
                **self._dtb_kwargs
            )
        )

    def get_configure(self):
        return self._dtb_cfg

    configure = property(get_configure)

    def setup_entity_categories(self):
        dtb_type_options_dict = {}
        basic_dtb_type_options = self._dtb_cfg.get('option.basic.default_basic_entity_type_options')
        basic_types = self._dtb_cfg.get('option.basic_types')
        for i_basic_type, i_basic_kwargs in basic_types.items():
            i_dtb_type_options = collections.OrderedDict()
            i_dtb_type_options.update(basic_dtb_type_options)
            i_dtb_type_options.update(i_basic_kwargs.get('options') or {})
            i_dtb_type_options.update(i_basic_kwargs.get('options_extra') or {})
            dtb_type_options_dict[i_basic_type] = i_dtb_type_options
        #
        entity_categories = self._dtb_cfg.get('option.entity_categories')
        for i_entity_category, i_entity_kwargs in entity_categories.items():
            i_basic_type = i_entity_kwargs['basic_type']
            # use copy
            i_entity_type_options = copy.copy(dtb_type_options_dict[i_basic_type])
            #
            i_entity_type_options.update(i_entity_kwargs.get('options_over') or {})
            i_entity_type_options.update(i_entity_kwargs.get('options_extra') or {})
            i_table_opt = self._dtb_opt.get_table_opt(name=i_entity_category)
            i_table_opt.create(i_entity_type_options)

    def setup_entities(self):
        entities = self._dtb_cfg.get('option.entities')
        for i_path, i_kwargs in entities.items():
            i_entity_type = i_kwargs['entity_type']
            i_options = i_kwargs.get('options') or {}
            i_path_opt = bsc_core.DccPathDagOpt(i_path)
            i_name = i_path_opt.name

            if 'gui_name' in i_kwargs:
                i_gui_name = i_kwargs['gui_name']
            else:
                i_gui_name = bsc_core.StrUnderlineOpt(i_name).to_prettify()

            self.add_entity(
                entity_type=i_entity_type,
                data=dict(
                    path=i_path,
                    gui_name=i_gui_name,
                    **i_options
                )
            )
            i_children = i_kwargs.get('children')
            if i_children is not None:
                i_child_entity_type = i_children.get('entity_type')
                if i_child_entity_type is None:
                    continue
                #
                i_child_names = i_children.get('names') or []
                i_child_options = i_children.get('options') or {}
                for j_child_name in i_child_names:
                    j_child_gui_name = bsc_core.StrUnderlineOpt(j_child_name).to_prettify()
                    self.add_entity(
                        entity_type=i_child_entity_type,
                        data=dict(
                            name=j_child_name,
                            gui_name=j_child_gui_name,
                            **i_child_options
                        )
                    )


if __name__ == '__main__':
    cfg_f = '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
    dtb = DtbResourceLib(cfg_f)

    dtb.setup_entity_categories()
    dtb.setup_entities()

    dtb.accept()

    ks = [chr(i) for i in range(97, 97+5)]
    dtb.accept()
