# coding:utf-8
import collections

import copy

from random import choice

from lxbasic import bsc_core

from lxdatabase import dtb_core

import lxbasic.objects as bsc_objects


class DtbResourceLib(object):
    PATHSEP = '/'
    class DatabaseTypes(object):
        UnitGroup = 'unit_group'
        Unit = 'unit'

    class EntityTypes(object):
        ResourceType = 'resource_type'
        Category = 'category'
        Type = 'type'
        #
        TagType = 'tag_type'
        #
        TagKey = 'tag_key'
        Tag = 'tag'
        #
        Resource = 'resource'
        Version = 'version'
        #
        Unit = 'unit'
        #
        ResourceTag = 'resource_tag'
        #
        All = [
            ResourceType,
            Category, Type,
            Unit,
            TagType, TagKey, Tag,
            #
            Resource, Version,
        ]

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

        db_file_path = db_file_pattern.format(
            **self._dtb_kwargs
        )
        self._dtb_file_opt = bsc_core.StorageFileOpt(
            db_file_path
        )
        self._dtb_file_opt.set_directory_create()

        self._dtb_opt = dtb_core.DtbSqlConnectionOpt.create_from_database(
            self._dtb_file_opt.get_path()
        )

    def get_configure(self):
        return self._dtb_cfg

    configure = property(get_configure)

    def setup_entity_types(self):
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
        entity_types = self._dtb_cfg.get('option.entity_types')
        for i_entity_type, i_entity_kwargs in entity_types.items():
            i_basic_type = i_entity_kwargs['basic_type']
            # use copy
            i_entity_type_options = copy.copy(dtb_type_options_dict[i_basic_type])
            #
            i_entity_type_options.update(i_entity_kwargs.get('options_over') or {})
            i_entity_type_options.update(i_entity_kwargs.get('options_extra') or {})
            i_entity_type_options['basic_type'] = dict(type='string', args=['not null', 'default "{}"'.format(i_basic_type)])
            i_table_opt = self._dtb_opt.get_table_opt(name=i_entity_type)
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
                path=i_path,
                gui_name=i_gui_name,
                **i_options
            )
            i_children = i_kwargs.get('children')
            if i_children is not None:
                i_entity_type_extra = i_children.get('entity_type')
                if i_entity_type_extra is None:
                    continue
                #
                i_child_names = i_children.get('names') or []
                i_child_options = i_children.get('options') or {}
                for j_child_name in i_child_names:
                    j_child_gui_name = bsc_core.StrUnderlineOpt(j_child_name).to_prettify()
                    self.add_entity(
                        entity_type=i_entity_type_extra,
                        name=j_child_name,
                        gui_name=j_child_gui_name,
                        **i_child_options
                    )

    def accept(self):
        self._dtb_opt.accept()
    # utility
    def add_entity(self, **kwargs):
        entity_type = kwargs['entity_type']
        path = kwargs.get('path')
        if path is not None:
            path_opt = bsc_core.DccPathDagOpt(path)
            group = path_opt.get_parent_path()
            kwargs['group'] = group
            name = path_opt.get_name()
            kwargs['name'] = name
        else:
            group = kwargs['group']
            if group == '/':
                path = '/{name}'.format(**kwargs)
            else:
                path = '{group}/{name}'.format(**kwargs)
            kwargs['path'] = path
        #
        table_opt = self._dtb_opt.get_table_opt(entity_type)
        return table_opt.add(**kwargs)

    def update_entity_property(self, entity_type, entity_name, **kwargs):
        table_opt = self._dtb_opt.get_table_opt(entity_type)
        kwargs['entity_type'] = entity_type
        return table_opt.update(entity_name, **kwargs)

    def get_entity(self, entity_type, filters):
        table_opt = self._dtb_opt.get_table_opt(entity_type)
        return table_opt.get_one(
            filters=filters,
        )

    def get_entity_is_exists(self, entity_type, **kwargs):
        table_opt = self._dtb_opt.get_table_opt(entity_type)
        return table_opt.get_is_exists(
            **dict(path=kwargs['path'])
        )

    def get_entities(self, entity_type, filters=None):
        table_opt = self._dtb_opt.get_table_opt(entity_type)
        return table_opt.get_all(
            filters=filters,
        )

    def get_entity_index(self, entity_type, new_connection=True):
        table_opt = self._dtb_opt.get_table_opt('sqlite_sequence')
        _ = table_opt.get_one(
            filters=[('name', 'is', entity_type)],
            new_connection=new_connection
        )
        if _:
            return _['seq']
        return 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.accept()


if __name__ == '__main__':
    cfg_f = '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
    dtb = DtbResourceLib(cfg_f)

    dtb.setup_entity_types()
    dtb.setup_entities()

    dtb.accept()

    ks = [chr(i) for i in range(97, 97+5)]
    dtb.accept()

