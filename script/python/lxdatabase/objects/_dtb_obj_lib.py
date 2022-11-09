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
        PropertyGroup = 'property_group'
        Property = 'property'
        #
        UnitProperties = 'unit_properties'

    class EntityTypes(object):
        TypeGroup = 'type_group'
        Type = 'type'
        Resource = 'resource'
        #
        AttributeGroup = 'attribute_group'
        Attributes = 'attributes'

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
            i_entity_type_options.update(i_entity_kwargs.get('options_extra') or {})
            i_entity_type_options['basic_type'] = dict(type='string', args=['not null', 'default "{}"'.format(i_basic_type)])
            i_table_opt = self._dtb_opt.get_table_opt(name=i_entity_type)
            i_table_opt.create(i_entity_type_options)

    def setup_entities(self):
        entities = self._dtb_cfg.get('option.entities')
        for i_entity_type, i_entity_kwargs in entities.items():
            print i_entity_type
            for j_path, j_kwargs in i_entity_kwargs.items():
                j_path_opt = bsc_core.DccPathDagOpt(j_path)
                j_group = j_path_opt.get_parent_path()
                j_name = j_path_opt.name
                if 'gui_name' in j_kwargs:
                    j_gui_name = j_kwargs['gui_name']
                else:
                    j_gui_name = bsc_core.StrUnderlineOpt(j_name).to_prettify()

                print j_group
                # self.add_entity(
                #     entity_type=i_entity_type,
                #     name=j_gui_name,
                #     gui_name=j_gui_name,
                #     group=j_group
                # )

    def accept(self):
        self._dtb_opt.accept()
    # utility
    def add_entity(self, **kwargs):
        entity_type = kwargs['entity_type']
        path_pattern = self._dtb_cfg.get('option.entity_types.{}.path_pattern'.format(entity_type))
        kwargs['path'] = path_pattern.format(**kwargs)
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.accept()


if __name__ == '__main__':
    cfg_f = '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
    dtb = DtbResourceLib(cfg_f)

    dtb.setup_entity_types()
    dtb.setup_entities()

    # ks = [chr(i) for i in range(97, 123)]

    ks = [chr(i) for i in range(97, 97+5)]

    states = ['old', 'new', 'damaged']
    resolutions = ['< 512', '512', '512 - 1024', '1024', '1024 - 2048', '2048', '2048 - 4096', '4096 - 8192', '> 8192']
    environments = ['ancient', 'desert', 'forest', 'freshwater', 'grassland', 'industrial', 'medieval']
    colors = ['black', 'brown', 'blue', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']
    # for i in ks:
    #     i_category_name = 'category_{}'.format(i)
    #     i_category_gui_name = bsc_core.StrUnderlineOpt(i_category_name).to_prettify()
    #     i_category_path = '/{}'.format(i_category_name)
    #     dtb.add_entity(
    #         entity_type=dtb.EntityTypes.TypeGroup,
    #         name=i_category_name,
    #         gui_name=i_category_gui_name,
    #         group=''
    #     )
    #     for j in ks:
    #         j_type_name = 'type_{}_{}'.format(i, j)
    #         j_type_gui_name = bsc_core.StrUnderlineOpt(j_type_name).to_prettify()
    #         j_type_path = '{}/{}'.format(i_category_path, j_type_name)
    #         dtb.add_entity(
    #             entity_type=dtb.EntityTypes.Type,
    #             name=j_type_name,
    #             gui_name=j_type_gui_name,
    #             group=i_category_path
    #         )
    #         for k in range(100):
    #             k_resource_name = 'resource_{}_{}_{}'.format(i, j, k)
    #             k_resource_gui_name = bsc_core.StrUnderlineOpt(k_resource_name).to_prettify()
    #             k_resource_path = '{}/{}'.format(j_type_path, k_resource_name)
    #             dtb.add_entity(
    #                 entity_type=dtb.EntityTypes.Resource,
    #                 name=k_resource_name,
    #                 gui_name=k_resource_gui_name,
    #                 #
    #                 group=j_type_path,
    #             )
    #             #
    #             dtb.add_entity(
    #                 entity_type=dtb.EntityTypes.Attributes,
    #                 name=k_resource_name,
    #                 #
    #                 resolution=choice(resolutions),
    #                 state=choice(states),
    #                 environment=choice(environments),
    #                 color=choice(colors),
    #                 #
    #                 unit=k_resource_path,
    #             )

    dtb.accept()

    # print dtb.get_entities(
    #     entity_type='type_group',
    #     filters=None
    # )
    # #
    # print dtb.get_entities(
    #     entity_type='type',
    #     filters=[
    #         ('group', 'is', '/category_a'),
    #     ]
    # )

    # print dtb.get_units(
    #     filters=[
    #         ('entity_type', 'is', 'resource'),
    #         ('group', 'startswith', '/category_a')
    #     ]
    # )

    # print len(
    #     dtb.get_units(
    #         filters=[
    #             ('state', 'is', 'new')
    #         ],
    #     )
    # )

    # print dtb.get_category(
    #     [('name', 'is', 'category_a')]
    # )
    #
    # print dtb.get_types(
    #     [('category', 'is', 'category_a')]
    # )
    # print dtb.get_units(
    #     filters=[
    #         ('name', 'in', ['resource_a_a_0'])
    #     ]
    # )
    # print dtb.get_resources_(
    #     type='type_a_a'
    # )
    # print dtb.get_resource_(
    #     name='resource_a_a_0'
    # )
    # print dtb.get_unit(
    #     filters=[('name', 'is', 'resource_a_a_0')]
    # )

