# coding:utf-8
import collections

import copy

import os

from lxbasic import bsc_core

from lxdatabase import dtb_core

import lxbasic.objects as bsc_objects


class DtbBaseOpt(object):
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
        CategoryRoot = 'category_root'
        CategoryGroup = 'category_group'
        Category = 'category'
        Type = 'type'
        # tag
        TagGroup = 'tag_group'
        Tag = 'tag'
        # node
        ResourceGroup = 'resource_group'
        Resource = 'resource'
        Version = 'version'
        Storage = 'storage'
        #
        Attribute = 'attribute'
        Connection = 'connection'
        #
        Assign = 'assign'
        #
        Types = 'types'
        Tags = 'tags'

    class Kinds(object):
        # type, use for "resource" classification, one "resource" can have one or more "type"
        ResourceCategoryRoot = 'resource-category-root'
        ResourceCategoryGroup = 'resource-category-group'
        ResourceCategory = 'resource-category'
        ResourceType = 'resource-type'
        # tag, use for "resource" filter, one "resource" can have one or more "tag"
        ResourceSemanticTagGroup = 'resource-semantic-tag-group'
        ResourceUserTagGroup = 'resource-user-tag-group'
        ResourcePropertyTagGroup = 'resource-property-tag-group'
        ResourceStorageTagGroup = 'resource-storage-tag-group'
        #
        ResourcePrimarySemanticTag = 'resource-primary-semantic-tag'
        ResourceSecondarySemanticTag = 'resource-secondary-semantic-tag'
        ResourcePropertyTag = 'resource-property-tag'
        ResourceUserTag = 'resource-user-tag'
        ResourceFileTag = 'resource-file-tag'
        ResourceFormatTag = 'resource-format-tag'
        # resource
        Resource = 'resource'
        Asset = 'asset'
        # version
        Version = 'version'
        # storage
        Directory = 'directory'
        File = 'file'
        All = [
            ResourceCategoryRoot,
            ResourceCategoryGroup,
            ResourceCategory,
            ResourceType,
            # tag, use for "resource" filter, one "resource" can have one or more "tag"
            ResourceSemanticTagGroup,
            ResourceUserTagGroup,
            ResourcePropertyTagGroup,
            ResourceStorageTagGroup,
            #
            ResourcePrimarySemanticTag,
            ResourceSecondarySemanticTag,
            ResourcePropertyTag,
            ResourceUserTag,
            ResourceFileTag,
            ResourceFormatTag,
            # resource
            Resource,
            Asset,
            # version
            Version,
            # storage
            Directory,
            File,
        ]

    EntityTypeCategoryMapper = {
        # type
        EntityTypes.CategoryRoot: EntityCategories.Type,
        EntityTypes.CategoryGroup: EntityCategories.Type,
        EntityTypes.Category: EntityCategories.Type,
        EntityTypes.Type: EntityCategories.Type,
        # tag
        EntityTypes.TagGroup: EntityCategories.Tag,
        EntityTypes.Tag: EntityCategories.Tag,
        # node
        EntityTypes.Resource: EntityCategories.Node,
        EntityTypes.Version: EntityCategories.Node,
        EntityTypes.Storage: EntityCategories.Node,
        # port
        EntityTypes.Attribute: EntityCategories.Port,
        # connection
        EntityTypes.Connection: EntityCategories.Connection,
        # assign
        EntityTypes.Assign: EntityCategories.Assign,
        EntityTypes.Types: EntityCategories.Assign,
        EntityTypes.Tags: EntityCategories.Assign,
    }

    def __init__(self, database):
        if not database:
            raise RuntimeError()

        # if os.path.isfile(database) is False:
        #     raise RuntimeError()

        bsc_core.LogMtd.trace_method_result(
            'database', 'setup from: {}'.format(database)
        )

        self._dtb_file_path = database
        self._dtb_file_opt = bsc_core.StgFileOpt(
            database
        )
        self._dtb_file_opt.create_directory()

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
                    if path == '/':
                        data['group'] = ''
                        data['name'] = ''
                    else:
                        #
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
        table_opt.add(**data)
        self.accept()
        return self.get_entity(
            entity_type=entity_type,
            filters=[
                ('path', 'is', path)
            ]
        )

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


class DtbResourceLibraryOpt(DtbBaseOpt):
    def __init__(self, configure_file, configure_file_extend=None):
        self._dtb_cfg_file_path = configure_file
        self._dtb_cfg_file_path_extend = configure_file_extend
        self._dtb_cfg_opt = bsc_objects.Configure(value=configure_file)
        if configure_file_extend is not None:
            if bsc_core.StgFileOpt(configure_file_extend).get_is_file() is False:
                raise RuntimeError()
            #
            self._dtb_cfg_opt.update_from(
                bsc_objects.Configure(value=configure_file_extend)
            )

        self._dtb_cfg_opt.set_flatten()

        self._dtb_pattern_kwargs = {}
        if bsc_core.SystemMtd.get_is_linux():
            self._dtb_stg_root = self._dtb_cfg_opt.get('option.variants.root-linux')
        elif bsc_core.SystemMtd.get_is_windows():
            self._dtb_stg_root = self._dtb_cfg_opt.get('option.variants.root-windows')
        else:
            raise NotImplementedError()
        #
        if not self._dtb_stg_root:
            raise RuntimeError()
        #
        self._dtb_pattern_kwargs['root'] = self._dtb_stg_root
        db_file_pattern = self._dtb_cfg_opt.get('database.file')
        if db_file_pattern is None:
            return
        #
        super(DtbResourceLibraryOpt, self).__init__(
            db_file_pattern.format(
                **self._dtb_pattern_kwargs
            )
        )

    def get_database_configure(self):
        return self._dtb_cfg_file_path
    database_configure = property(get_database_configure)

    def get_database_configure_opt(self):
        return self._dtb_cfg_opt
    database_configure_opt = property(get_database_configure_opt)

    def get_database_configure_extend(self):
        return self._dtb_cfg_file_path_extend
    database_configure_extend = property(get_database_configure_extend)

    def get_stg_root(self):
        return self._dtb_stg_root
    stg_root = property(get_stg_root)

    def get_pattern(self, keyword):
        return self._dtb_cfg_opt.get(
            'patterns.{}'.format(keyword)
        )

    def get_pattern_opt(self, keyword):
        p = self.get_pattern(keyword)
        p_opt = bsc_core.PtnParseOpt(p)
        return p_opt.set_update_to(
            **self._dtb_pattern_kwargs
        )

    def get_pattern_kwargs(self):
        return self._dtb_pattern_kwargs

    def setup_entity_categories(self):
        dtb_type_options_dict = {}
        basic_dtb_type_options = self._dtb_cfg_opt.get('option.basic.default_basic_entity_type_options')
        basic_types = self._dtb_cfg_opt.get('option.basic_types')
        for i_basic_type, i_basic_kwargs in basic_types.items():
            i_dtb_type_options = collections.OrderedDict()
            i_dtb_type_options.update(basic_dtb_type_options)
            i_dtb_type_options.update(i_basic_kwargs.get('options') or {})
            i_dtb_type_options.update(i_basic_kwargs.get('options_extra') or {})
            dtb_type_options_dict[i_basic_type] = i_dtb_type_options
        #
        entity_categories = self._dtb_cfg_opt.get('option.entity_categories')
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
        entities = self._dtb_cfg_opt.get('option.entities')
        for i_path, i_kwargs in entities.items():
            i_entity_type = i_kwargs['entity_type']
            i_options = i_kwargs.get('options') or {}
            i_path_opt = bsc_core.DccPathDagOpt(i_path)
            i_name = i_path_opt.name

            if 'gui_name' in i_kwargs:
                i_gui_name = i_kwargs['gui_name']
            else:
                i_gui_name = bsc_core.RawStrUnderlineOpt(i_name).to_prettify()

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
                    j_child_gui_name = bsc_core.RawStrUnderlineOpt(j_child_name).to_prettify()
                    self.add_entity(
                        entity_type=i_child_entity_type,
                        data=dict(
                            name=j_child_name,
                            gui_name=j_child_gui_name,
                            **i_child_options
                        )
                    )

    def create_category_root(self, path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.CategoryRoot,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        gui_name = 'All'
        options = dict(kind=self.Kinds.ResourceCategoryRoot, gui_icon_name='database/all')
        return True, self.add_entity(
            entity_type=self.EntityTypes.CategoryRoot,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def create_category_group(self, path):
        path_opt = bsc_core.DccPathDagOpt(path)
        if not self.get_entity(
            entity_type=self.EntityTypes.CategoryRoot,
            filters=[
                ('path', 'is', path_opt.get_parent_path()),
            ]
        ):
            raise RuntimeError()
        #
        _ = self.get_entity(
            entity_type=self.EntityTypes.CategoryGroup,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.ResourceCategoryGroup, gui_icon_name='database/groups')
        return True, self.add_entity(
            entity_type=self.EntityTypes.CategoryGroup,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def create_category(self, path):
        path_opt = bsc_core.DccPathDagOpt(path)
        if not self.get_entity(
            entity_type=self.EntityTypes.CategoryGroup,
            filters=[
                ('path', 'is', path_opt.get_parent_path()),
            ]
        ):
            raise RuntimeError()
        #

        _ = self.get_entity(
            entity_type=self.EntityTypes.Category,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.ResourceCategory, gui_icon_name='database/group')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Category,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def get_categories(self, category_group):
        return self.get_entities(
            entity_type=self.EntityTypes.Category,
            filters=[
                ('group', 'is', '/{}'.format(category_group)),
            ]
        )

    def create_type(self, path):
        path_opt = bsc_core.DccPathDagOpt(path)
        if not self.get_entity(
            entity_type=self.EntityTypes.Category,
            filters=[
                ('path', 'is', path_opt.get_parent_path()),
            ]
        ):
            raise RuntimeError()
        #
        _ = self.get_entity(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.ResourceType, gui_icon_name='database/object')
        options['gui_name'] = gui_name
        return True, self.add_entity(
            entity_type=self.EntityTypes.Type,
            data=dict(
                path=path,
                **options
            )
        )

    def get_types(self, category_group, category):
        return self.get_entities(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('group', 'is', '/{}/{}'.format(category_group, category)),
            ]
        )

    def create_type_assign(self, node_path, value, kind):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Types,
            filters=[
                ('path', 'is', '{}->{}'.format(node_path, value)),
            ]
        )
        if _:
            return False, _
        return True, self.add_entity(
            entity_type=self.EntityTypes.Types,
            data=dict(
                kind=kind,
                #
                node=node_path,
                value=value
            )
        )

    def get_type_force(self, path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('path', 'is', path),
                ('kind', 'is', self.Kinds.ResourceType)
            ]
        )
        if _:
            return False, _
        #
        method_args = [
            self.create_category_root,
            self.create_category_group,
            self.create_category,
            self.create_type,
        ]
        path_opt = bsc_core.DccPathDagOpt(path)
        components = path_opt.get_components()
        components.reverse()
        results = []
        for seq, i in enumerate(components):
            i_kwargs = dict(path=i.get_path())
            i_method = method_args[seq]
            results.append(i_method(**i_kwargs))
        #
        return results[-1]

    def create_resource(self, path, **kwargs):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Resource,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        path_opt = bsc_core.DccPathDagOpt(path)
        name = path_opt.get_name()
        gui_name = bsc_core.RawStrUnderlineOpt(name).to_prettify()
        options = dict(kind=self.Kinds.Resource, gui_icon_name='database/object')
        options['gui_name'] = gui_name
        options.update(kwargs)
        return True, self.add_entity(
            entity_type=self.EntityTypes.Resource,
            data=dict(
                path=path,
                **options
            )
        )

    def create_version(self, path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Version,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        path_opt = bsc_core.DccPathDagOpt(path)
        name = path_opt.get_name()
        gui_name = name
        options = dict(kind=self.Kinds.Version, gui_icon_name='database/object')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Version,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def create_property(self, node_path, port_path, value, kind):
        atr_path = '.'.join([node_path, port_path])
        _ = self.get_entity(
            entity_type=self.EntityTypes.Attribute,
            filters=[
                ('path', 'is', atr_path),
            ]
        )
        if _:
            return False, _
        #
        return True, self.add_entity(
            entity_type=self.EntityTypes.Attribute,
            data=dict(
                kind=kind,
                node=node_path,
                port=port_path,
                value=value
            )
        )

    def create_storage(self, path, kind):
        if kind not in self.Kinds.All:
            raise RuntimeError()
        #
        _ = self.get_entity(
            entity_type=self.EntityTypes.Storage,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        #
        path_opt = bsc_core.DccPathDagOpt(path)
        name = path_opt.get_name()
        gui_name = name
        options = dict(kind=kind, gui_icon_name='database/object')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Storage,
            data=dict(
                path=path,
                gui_name=gui_name,
                **options
            )
        )

    def get_property(self, node_path, port_path):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Attribute,
            filters=[
                ('path', 'is', '{}.{}'.format(node_path, port_path)),
            ]
        )
        if _:
            return _.value

    def create_tag(self, path, kind):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Tag,
            filters=[
                ('path', 'is', path),
            ]
        )
        if _:
            return False, _
        options = dict(kind=kind, gui_icon_name='database/object')
        return True, self.add_entity(
            entity_type=self.EntityTypes.Tag,
            data=dict(
                path=path,
                **options
            )
        )

    def create_tag_assign(self, node_path, value, kind):
        _ = self.get_entity(
            entity_type=self.EntityTypes.Tags,
            filters=[
                ('path', 'is', '{}->{}'.format(node_path, value)),
            ]
        )
        if _:
            return False, _
        return True, self.add_entity(
            entity_type=self.EntityTypes.Tags,
            data=dict(
                kind=kind,
                #
                node=node_path,
                value=value
            )
        )
    @classmethod
    def guess_type_args(cls, keys):
        c_max = 4
        c = len(keys)
        if c < 3:
            keys += ['other']*(c_max-c-1)
        elif c > 3:
            keys = keys[:2]+['_'.join(keys[2:])]
        #
        return keys


class DtbNodeOpt(object):
    def __init__(self, dtb_opt, dtb_entity):
        self._dtb_opt = dtb_opt
        self._dtb_entity = dtb_entity

    def get(self, key):
        return self._dtb_opt.get_entity(
            entity_type=self._dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', self._dtb_entity.path),
                ('port', 'is', key),
            ],
            new_connection=False
        ).value

    def get_as_node(self, key):
        return self._dtb_opt.get_entity(
            entity_type=key,
            filters=[
                ('path', 'is', self.get(key)),
            ],
            new_connection=False
        )


if __name__ == '__main__':
    for _i_key in [
        # 'surface',
        # 'atlas',
        # 'displacement',
        # '3d_asset',
        # '3d_plant',
        # 'imperfection',
        # 'texture'
        # 'test'
        '3d_proxy',
    ]:
        dtb_opt_ = DtbResourceLibraryOpt(
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-basic'),
            bsc_core.CfgFileMtd.get_yaml('database/library/resource-{}'.format(_i_key)),
        )
        #
        dtb_opt_.setup_entity_categories()
        dtb_opt_.setup_entities()
        dtb_opt_.accept()
    # dtb_opt_.create_category_group('atlas')
    # dtb_opt_.create_category('fern', '/atlas')
    # dtb_opt_.create_type('other', '/atlas/fern')
    # dtb_opt_.create_category_root()
    # print dtb_opt_.get_type_force('/atlas/fern/other')
    # print dtb_opt_.create_resource('/atlas/sword_fern_pjvef2')
    # print dtb_opt_.create_resource_property('/atlas/sword_fern_pjvef2.version', '/atlas/sword_fern_pjvef2/v0001')
    # print dtb_opt_.create_version('/atlas/sword_fern_pjvef2/v0001')
