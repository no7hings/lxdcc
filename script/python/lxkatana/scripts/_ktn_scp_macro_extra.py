# coding:utf-8
import six

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxkatana import ktn_core


class ScpMacro(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._cfg = bsc_objects.Configure(value=self._file_path)
        self._cfg.set('option.unique_name', bsc_core.TimeExtraMtd.get_time_tag_36_(multiply=100).lower())
        #
        color_hsv = self._cfg.get('option.color_hsv')
        if color_hsv:
            h, s, v = color_hsv['h'], color_hsv['s'], color_hsv['v']
            r, g, b = bsc_core.RawColorMtd.hsv2rgb(h, s, v, maximum=1.0)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        color_use_variant = self._cfg.get('option.color_use_variant', False)
        if color_use_variant is True:
            variant_key = self._cfg.get('option.variant_key')
            r, g, b = bsc_core.RawTextOpt(variant_key).to_rgb_(maximum=1.0, s_p=12.5, v_p=25)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        auto_color = self._cfg.get('option.auto_color', default_value=True)
        if auto_color is True:
            type_name = self._cfg.get('option.type')
            r, g, b = bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25)
            self._cfg.set(
                'option.color.r', r
            )
            self._cfg.set(
                'option.color.g', g
            )
            self._cfg.set(
                'option.color.b', b
            )
        #
        self._cfg.set_flatten()
    #
    @ktn_core.Modifier.undo_debug_run
    def build(self):
        self.build_main()
        self.build_nodes()
        self.gui_layout()
        #
        self.update_records()
        self.add_nodes()

    def build_main(self):
        data = self._cfg.get_content('main')
        ktn_obj, is_create = self._build_node_(data)
        self._obj_opt = ktn_core.NGObjOpt(ktn_obj)
        if is_create is False:
            clear_ports = data.get('clear_ports', default_value=True)
            if clear_ports is True:
                self._obj_opt.clear_ports(
                    data.get('clear_start')
                )
            #
            self._obj_opt.create_ports_by_data(
                data.get('ports') or {}
            )
        #
        if data.get('type') in ['Group']:
            clear_children = data.get('clear_children', default_value=True)
            if clear_children is True:
                self._obj_opt.clear_children()
        #
        self._extend_kwargs = {}
        record_p = self._obj_opt.get_port('record')
        if record_p is not None:
            main_path = self._obj_opt.get_path()
            for i in ktn_core.NGObjOpt(record_p).get_children():
                i_p_opt = ktn_core.NGPortOpt(i)
                i_key = i_p_opt.get_name()
                i_name = i_p_opt.get()
                i_path = '{}/{}'.format(main_path, i_name)
                self._extend_kwargs[i_key] = i_path

    def build_nodes(self):
        if self._cfg.get_key_is_exists('node') is False:
            return
        c = self._cfg.get_content('node')
        for i_key in c.get_top_keys():
            i_data = c.get_content(i_key)
            self._build_node_(i_data)
    @classmethod
    def _build_node_(cls, data, extend_kwargs=None):
        type_name = data['type']
        path = data['path']
        force_update = data.get('force_update', False)
        ktn_obj, is_create = ktn_core.NGObjOpt._get_create_args_(path, type_name)
        obj_opt = ktn_core.NGObjOpt(ktn_obj)
        if is_create is True or force_update is True:
            if not type_name.endswith('_Wsp'):
                obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.create_input_ports_by_data(
                data.get('input_ports') or []
            )
            #
            obj_opt.create_output_ports_by_data(
                data.get('output_ports') or []
            )
            #
            obj_opt.create_ports_by_data(
                data.get('ports') or {}
            )
            #
            obj_opt.set_port_hints_by_data(
                data.get('port_hints') or {},
                extend_kwargs=extend_kwargs
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {}
            )
            #
            if type_name in ['LiveGroup']:
                ktn_obj.reloadFromSource()
            #
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )
            #
            ktn_core.NGObjOpt._create_connections_by_data_(
                data.get('connections') or [],
                extend_kwargs=extend_kwargs
            )

            ktn_core.NGObjOpt._create_connections_by_data_(
                data.get('force_connections') or [],
                extend_kwargs=extend_kwargs, create_target=True
            )
            base_type_name = data.get('base_type', None)
            #
            if type_name in ['GroupStack', 'GroupMerge'] or base_type_name in ['GroupStack', 'GroupMerge']:
                child_type_name = data.get('child.type')
                if child_type_name is None:
                    raise RuntimeError()
                ktn_obj.setChildNodeType(child_type_name)
                child_nodes = data.get('child.nodes') or {}
                if child_nodes:
                    child_path_pattern = data.get('child.path_pattern')
                    if child_path_pattern is None:
                        raise RuntimeError()
                    #
                    for i_key, i_data in child_nodes.items():
                        i_var = dict(
                            parent=path,
                            key=i_key
                        )
                        i_data['type'] = child_type_name
                        i_data['path'] = child_path_pattern.format(**i_var)
                        cls._build_node_child_(i_data)
        #
        obj_opt.set_attributes(
            data.get('attributes') or {}
        )
        return ktn_obj, is_create
    @classmethod
    def _build_node_child_(cls, data, extend_kwargs=None):
        type_name = data['type']
        path = data['path']
        ktn_obj, is_create = ktn_core.NGObjOpt._get_group_stack_child_create_args_(path, type_name)
        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            #
            obj_opt.set_color(bsc_core.RawTextOpt(type_name).to_rgb_(maximum=1.0, s_p=25, v_p=25))
            #
            obj_opt.set_attributes(
                data.get('attributes') or {}
            )
            #
            obj_opt.set_parameters_by_data(
                data.get('parameters') or {},
            )
            obj_opt.set_arnold_geometry_properties_by_data(
                data.get('arnold_geometry_properties') or {}
            )
            #
            obj_opt.set_expressions_by_data(
                data.get('expressions') or {},
                extend_kwargs=extend_kwargs
            )

    def update_records(self):
        if self._cfg.get_key_is_exists('record_update') is False:
            return
        c = self._cfg.get_content('record_update')
        for i_key in c.get_top_keys():
            i_data = c.get_content(i_key)
            self._update_record_(i_key, i_data)

    def _update_record_(self, key, data, extend_kwargs=None):
        port_path = 'record.{}'.format(key)
        name = self._obj_opt.get(port_path)
        obj_opt = ktn_core.NGObjOpt(name)
        obj_opt.create_input_ports_by_data(
            data.get('input_ports') or []
        )
        #
        obj_opt.create_output_ports_by_data(
            data.get('output_ports') or []
        )
        #
        obj_opt.create_ports_by_data(
            data.get('ports') or {}
        )
        obj_opt.set_port_hints_by_data(
            data.get('port_hints') or {},
            extend_kwargs=extend_kwargs
        )
        #
        obj_opt.set_parameters_by_data(
            data.get('parameters') or {}
        )
        obj_opt.set_expressions_by_data(
            data.get('expressions') or {},
            extend_kwargs=extend_kwargs
        )
        #
        ktn_core.NGObjOpt._create_connections_by_data_(
            data.get('connections') or []
        )
        #
        obj_opt.set_attributes(
            data.get('attributes') or {}
        )

    def add_nodes(self):
        if self._cfg.get_key_is_exists('node_add') is False:
            return
        c = self._cfg.get_content('node_add')
        for i_key in c.get_top_keys():
            i_data = c.get_content(i_key)
            self._build_node_(i_data, extend_kwargs=self._extend_kwargs)

    def gui_layout(self):
        layout_gui = self._cfg.get('option.layout_gui', default_value=True)
        if layout_gui is True:
            self._obj_opt.gui_layout_node_graph(size=(240, 40))

    def save(self):
        file_opt = bsc_core.StgFileOpt(self._file_path)
        macro_file_path = '{}.macro'.format(file_opt.path_base)
        self._obj_opt.save_as_macro(
            macro_file_path
        )


class AbsWsp(object):
    PRESET_DICT = {}
    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            self._ktn_obj = ktn_core.NodegraphAPI.GetNode(
                ktn_obj
            )
        else:
            self._ktn_obj = ktn_obj
        self._obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

    def get_rsv_task(self):
        pass

    def load_preset(self):
        name = self._obj_opt.get('preset.name')
        if name in self.PRESET_DICT:
            for k, v in self.PRESET_DICT[name].items():
                self._obj_opt.set(
                    k.replace('/', '.'), v
                )


class ScpWspVariantRegister(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspVariantRegister, self).__init__(*args, **kwargs)

    def _get_key_(self):
        return self._obj_opt.get('variableName')

    def _get_values_(self):
        list_ = []
        ktn_port = self._obj_opt.get_port('patterns')
        for i in ktn_core.NGPortOpt(ktn_port).get_children():
            i_key = ktn_core.NGPortOpt(i).get_name()
            i_value = ktn_core.NGPortOpt(i).get()
            if self._obj_opt.get_input_port(i_key).getConnectedPorts():
                list_.append(i_value)
        return list_

    def register_variable(self):
        key = self._get_key_()
        values = self._get_values_()
        if values:
            ktn_core.VariablesSetting().set_register(
                key, values
            )


class ScpWspVariantSet(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspVariantSet, self).__init__(*args, **kwargs)

    def _get_key_(self):
        return self._obj_opt.get('variant.key')

    def refresh_value(self):
        key = self._get_key_()
        branches = ktn_core.VariablesSetting().get_branches(key)
        if branches:
            self._obj_opt.set_enumerate_strings(
                'option.branch', branches
            )


class ScpWspShaderChecker(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspShaderChecker, self).__init__(*args, **kwargs)

    def fit_to_camera(self):
        scale_percent = self._obj_opt.get(
            'extra.camera_fit.scale_percent'
        )
        margin_percent = self._obj_opt.get(
            'extra.camera_fit.margin_percent'
        )
        camera_fov = self._obj_opt.get(
            'extra.camera_fit.camera_fov'
        )
        camera_screen_mode = self._obj_opt.get(
            'extra.camera_fit.camera_screen_mode'
        )
        render_resolution = self._obj_opt.get(
            'extra.camera_fit.render_resolution'
        )
        r_w, r_h = ktn_core.ResolutionOpt(render_resolution).get()
        (t_x, t_y, t_z), (s_x, s_y, s_z) = bsc_core.CameraMtd.get_project_pos(
            1, scale_percent, margin_percent, camera_fov, camera_screen_mode, (r_w, r_h)
        )
        ass_opt = ktn_core.NGObjOpt(
            self._obj_opt.get('record.ass')
        )
        ass_opt.set(
            'transform.translate', [t_x, t_y, t_z]
        )
        ass_opt.set(
            'transform.scale', [s_x, s_y, s_z]
        )


class ScpWspGeometry(AbsWsp):
    # todo: use preset module
    PRESET_DICT = {
        'test_0': {
            'cache/asset_usd/enable': True,
            'cache/asset_usd/file': '/l/prod/cgm/work/assets/chr/nn_4y/srf/surfacing/set/scene/v037/nn_4y.usda'
        }
    }
    # todo: configure to resolver
    DEFAULT_VALUE_MAPPER = dict(
        modeling='model',
        groom='groom',
        rig='rig',
        effect='effect',
        surfacing='surface',
        animation='animation'
    )
    def __init__(self, *args, **kwargs):
        super(ScpWspGeometry, self).__init__(*args, **kwargs)

    def update_usd_variant(self):
        from lxusd import usd_core

        asset_usd_file_path = self._obj_opt.get('cache.asset_usd.file')

        usd_stage_opt = usd_core.UsdStageOpt(asset_usd_file_path)
        # todo: root use configure
        usd_prim_opt = usd_core.UsdPrimOpt(usd_stage_opt.get_obj('/master'))
        usd_variant_dict = usd_prim_opt.get_variant_dict()

        for k, v in usd_variant_dict.iteritems():
            if bsc_core.RawTextOpt(k).get_is_matched('*_main'):
                i_p = 'usd_variant.asset_version_main.{}'.format(k[:-len('_main')])
                i_default, i_values = v
                self._obj_opt.set_enumerate_strings(i_p, i_values)
                self._obj_opt.set(i_p, i_default)
            elif bsc_core.RawTextOpt(k).get_is_matched('*_override'):
                i_p = 'usd_variant.asset_version_override.{}'.format(k[:-len('_override')])
                i_default, i_values = v
                self._obj_opt.set_enumerate_strings(i_p, i_values)
                self._obj_opt.set(i_p, i_default)
        #
        for k, v in usd_variant_dict.iteritems():
            if k in self.DEFAULT_VALUE_MAPPER:
                i_default, i_values = v
                i_p = 'usd_variant.asset_version_main.{}'.format(self.DEFAULT_VALUE_MAPPER[k])
                self._obj_opt.set(i_p, i_default)


class ScpWspSpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'
    #
    def __init__(self, *args, **kwargs):
        super(ScpWspSpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        obj_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(obj_name).register_variable()
        ktn_core.NGObjOpt(obj_name).set_port_execute('variant.register')


class ScpWspGeometrySpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'
    #
    class Keys(object):
        node_name = 'record.variant_register'
        #
        default_name = 'extra.default_name'
        customize_name = 'extra.customize_name'
    #
    def __init__(self, *args, **kwargs):
        super(ScpWspGeometrySpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        node_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(node_name).register_variable()


class ScpWspCamera(AbsWsp):
    PRESET_DICT = {
        'test_0': {
            'cache/asset_abc/enable': True,
            'cache/asset_abc/file': '/l/prod/cgm/publish/assets/chr/nn_4y/cam/camera/nn_4y.cam.camera.v001/camera/abc/main.abc',
            'cache/asset_abc/camera_shape_from': '/root/world/cam/cam_fullbody/cam_fullbodyShape'
        }
    }
    def __init__(self, *args, **kwargs):
        super(ScpWspCamera, self).__init__(*args, **kwargs)


class ScpWspCameraSpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'

    class Keys(object):

        #
        default_name = 'extra.default_name'
        customize_name = 'extra.customize_name'
    #
    def __init__(self, *args, **kwargs):
        super(ScpWspCameraSpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        node_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(node_name).register_variable()


class ScpWspLookSpace(AbsWsp):
    class Records(object):
        variant_register = 'record.variant_register'

        #
        default_name = 'extra.default_name'
        customize_name = 'extra.customize_name'
    #
    def __init__(self, *args, **kwargs):
        super(ScpWspLookSpace, self).__init__(*args, **kwargs)

    def add_default(self):
        pass

    def add_customize(self):
        pass

    def _add_(self, key):
        pass

    def register_variable(self):
        node_name = self._obj_opt.get(
            self.Records.variant_register
        )
        ScpWspVariantRegister(node_name).register_variable()


class ScpWspLightRig(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspLightRig, self).__init__(*args, **kwargs)

    def _get_light_args_(self):
        import lxbasic.extra.methods as bsc_etr_methods

        import lxresolver.commands as rsv_commands

        import lxshotgun.rsv.objects as stg_rsv_objects

        project = self._obj_opt.get('option.project')
        if project == 'current':
            project = bsc_etr_methods.EtrBase.get_project()
        #
        resolver = rsv_commands.get_resolver()
        #
        rsv_project = resolver.get_rsv_project(project=project)
        if rsv_project is None:
            return
        #
        defaults, currents = stg_rsv_objects.RsvStgProjectOpt(
            rsv_project
        ).get_light_args()
        return defaults, currents

    def guess_option(self):
        args = self._get_light_args_()
        if args:
            defaults, currents = args
            #
            key_1 = 'option.resource'
            current_pre = self._obj_opt.get(key_1)
            if currents:
                self._obj_opt.set_enumerate_strings(key_1, currents)
                if current_pre != 'None':
                    self._obj_opt.set(key_1, current_pre)
                else:
                    if defaults:
                        self._obj_opt.set(key_1, defaults[0])
            else:
                self._obj_opt.set_enumerate_strings(
                    key_1, ['None']
                )

    def _get_live_group_results_(self):
        import lxbasic.extra.methods as bsc_etr_methods

        import lxresolver.commands as rsv_commands

        project = self._obj_opt.get('option.project')
        if project == 'current':
            project = bsc_etr_methods.EtrBase.get_project()
        #
        resolver = rsv_commands.get_resolver()
        #
        rsv_project = resolver.get_rsv_project(project=project)
        if rsv_project is None:
            return

        asset = self._obj_opt.get('option.resource')
        if asset == 'None':
            return
        #
        properties = rsv_project.properties
        role = properties.get('roles.light_rig')
        step = properties.get('asset_steps.light_rig')
        task = properties.get('asset_tasks.light_rig')
        rsv_task = rsv_project.get_rsv_task(
            role=role, asset=asset, step=step, task=task
        )
        if rsv_task is None:
            return
        #
        rsv_unit = rsv_task.get_rsv_unit(
            keyword='asset-live_group-file'
        )
        if rsv_unit is None:
            return
        #
        return rsv_unit.get_result(
            version='all'
        )

    def load_light_rig(self):
        results = self._get_live_group_results_()
        if results:
            key = 'option.live_group.current'
            current = results[-1]
            self._obj_opt.set_enumerate_strings(
                key, results
            )
            self._obj_opt.set(
                key, current
            )
            self.refresh_live_group()

    def refresh_live_group(self, ):
        current = self._obj_opt.get('option.live_group.current')
        name = self._obj_opt.get('record.live_group')
        obj_opt = ktn_core.NGObjOpt(
            name
        )

        obj_opt.set(
            'source', current
        )
        obj_opt.get_ktn_obj().reloadFromSource()


class ScpWspLight(AbsWsp):
    def __init__(self, *args, **kwargs):
        super(ScpWspLight, self).__init__(*args, **kwargs)

    def guess_light_rig_option(self):
        name = self._obj_opt.get('record.light_rig')
        args = ScpWspLightRig(name)._get_light_args_()
        if args:
            defaults, currents = args
            key_1 = 'cache.light_rig.resource'
            current_pre = self._obj_opt.get(key_1)
            if currents:
                self._obj_opt.set_enumerate_strings(key_1, currents)
                if current_pre != 'None':
                    self._obj_opt.set(key_1, current_pre)
                else:
                    if defaults:
                        self._obj_opt.set(key_1, defaults[0])
            else:
                self._obj_opt.set_enumerate_strings(
                    key_1, ['None']
                )

    def load_light_rig(self):
        name = self._obj_opt.get('record.light_rig')
        ScpWspLightRig(name).load_light_rig()


class ScpWspWorkspace(AbsWsp):
    CFG = bsc_core.CfgFileMtd.get_yaml(
        'katana/script/macro/workspace'
    )
    def __init__(self, *args, **kwargs):
        super(ScpWspWorkspace, self).__init__(*args, **kwargs)
        self._cfg = bsc_objects.Configure(value=self.CFG)

        self._cfg.set(
            'option.path', self._obj_opt.get_path(),
        )
        self._cfg.set(
            'option.root', self._obj_opt.get_parent_opt().get_path(),
        )
        exists_time_tag = self._obj_opt.get('build.time_tag')
        if not exists_time_tag:
            exists_time_tag = bsc_core.TimeExtraMtd.get_time_tag_36_(multiply=100)
            self._obj_opt.set('build.time_tag', exists_time_tag)
        #
        self._cfg.set(
            'option.time_tag', exists_time_tag
        )
        x, y = self._obj_opt.get_position()
        self._cfg.set(
            'option.position.x', x
        )
        self._cfg.set(
            'option.position.y', y
        )
        self._cfg.set_flatten()

        self.PRESET_DICT = self._cfg.get('preset')

    def guess_option(self):
        pass

    def register_variable(self):
        record_p = self._obj_opt.get_port('record')
        if record_p is not None:
            for i in ktn_core.NGObjOpt(record_p).get_children():
                i_p_opt = ktn_core.NGPortOpt(i)
                i_obj_name = i_p_opt.get()
                if i_obj_name:
                    ktn_core.NGObjOpt(i_obj_name).set_port_execute('variant.register')

    def build(self):
        keys = self._cfg.get('option.keys')
        for i_key in keys:
            i_enable = self._obj_opt.get('build.{}.enable'.format(i_key))
            i_scheme = self._obj_opt.get('build.{}.scheme'.format(i_key))
            if i_enable:
                i_cfg_key = 'build.{}.{}'.format(i_key, i_scheme)
                if self._cfg.get_key_is_exists(i_cfg_key):
                    i_data = self._cfg.get_content(i_cfg_key)
                    i_record = self._obj_opt.get('record.{}'.format(i_key))
                    if not i_record:
                        i_main_data = i_data.get_content('main')
                        self._build_element_(i_key, i_main_data)
        #
        self._record_dict = dict(
            workspace=self._obj_opt.get_name()
        )
        #
        exists_keys = []
        connections = []
        record_p = self._obj_opt.get_port('record')
        if record_p is not None:
            for i in ktn_core.NGObjOpt(record_p).get_children():
                i_p_opt = ktn_core.NGPortOpt(i)
                i_key = i_p_opt.get_name()
                i_obj_name = i_p_opt.get()
                if i_obj_name:
                    exists_keys.append(i_key)
                    self._record_dict[i_key] = i_obj_name
        c = len(exists_keys)
        for i_index, i_key_src in enumerate(exists_keys):
            i_obj_name_src = self._record_dict[i_key_src]
            i_obj_opt_src = ktn_core.NGObjOpt(i_obj_name_src)
            i_src = '{}.{}'.format(i_obj_name_src, i_obj_opt_src.get_output_port_names()[0])
            if i_index == c-1:
                i_obj_key_tgt = 'workspace'
            else:
                i_obj_key_tgt = exists_keys[i_index+1]
            i_obj_name_tgt = self._record_dict[i_obj_key_tgt]
            i_obj_opt_tgt = ktn_core.NGObjOpt(i_obj_name_tgt)
            i_tgt = '{}.{}'.format(i_obj_name_tgt, i_obj_opt_tgt.get_input_port_names()[0])
            connections.extend(
                [i_src, i_tgt]
            )

        ktn_core.NGObjOpt._create_connections_by_data_(connections)

    def _build_element_(self, key, data):
        ktn_obj, is_create = ScpMacro._build_node_(data)

        if is_create is True:
            obj_opt = ktn_core.NGObjOpt(ktn_obj)
            self._obj_opt.set_expression(
                'record.{}'.format(key),
                'getNode(\'{}\').getNodeName()'.format(
                    obj_opt.get_name()
                )
            )
