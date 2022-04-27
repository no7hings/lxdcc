# coding:utf-8
from lxbasic import bsc_core

import lxkatana.dcc.dcc_objects as ktn_dcc_objects

from lxkatana.dcc.dcc_operators import _ktn_dcc_opt_look

from lxkatana.modifiers import _ktn_mdf_utility


class AssetWorkspaceOpt(object):
    WHITE_DICT = {
        'base_color':  (1, .955, .905),
        #
        'specular': 0.75,
        'specular_roughness': 0.375,
        'specular_IOR': 1.33,
        #
        'sheen': 1,
        'sheen_color': (1, 0.985, 0.925),
        #
        'subsurface': 0.105,
        'subsurface_color': (1, 0.75, 0.25),
        'subsurface_radius': (0.8, 0.8, 0.8),
        'subsurface_scale': 0.125,
    }
    def __init__(self, workspace):
        self._workspace = workspace
    #
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_auto_ambocc_assign(self, pass_name='default'):
        configure = self._workspace.get_configure(pass_name)
        # geometry_root = configure.get('option.geometry_root')
        material_root = configure.get('option.material_root')
        geometries = self._workspace.get_sg_geometries(pass_name)
        for i_geometry in geometries:
            i_geometry_type_name = i_geometry.type_name
            i_dcc_material_assign, i_ktn_material_assign = self._workspace.get_ng_geometry_material_assign(
                name=i_geometry.name,
                pass_name=pass_name
            )
            if i_ktn_material_assign is None:
                i_dcc_material, i_ktn_material = self._workspace.set_ng_material_create(
                    name=i_geometry.name,
                    pass_name=pass_name
                )
                self._workspace.set_ng_geometry_material_assign_create(
                    name=i_geometry.name,
                    assign=(
                        i_geometry.path,
                        '{}/{}'.format(material_root, i_dcc_material.name)
                    ),
                    pass_name=pass_name
                )
                i_dcc_shader_name = '{}__surface__override'.format(i_dcc_material.name)
                i_dcc_shader_path = '{}/{}'.format(i_dcc_material.get_parent().path, i_dcc_shader_name)
                if i_geometry_type_name in ['renderer procedural']:
                    i_color = (0.37, 0.08, 0.37)
                    # h, s, v = bsc_core.ColorMtd.hsv2rgb(r, g, b, maximum=1)
                    self._set_ambocc_create_(
                        i_dcc_material,
                        i_dcc_shader_path,
                        i_color
                    )
                elif i_geometry_type_name in ['subdmesh']:
                    self._set_opacity_lambert_create_(
                        i_dcc_material,
                        i_dcc_shader_path,
                    )
            else:
                i_sg_material_path = i_dcc_material_assign.get_port(
                    'args.materialAssign.value'
                ).get()
                if i_sg_material_path:
                    i_material_name = bsc_core.DccPathDagOpt(i_sg_material_path).name
                    i_dcc_material = ktn_dcc_objects.Node(i_material_name)
                    i_dcc_shader_name = '{}__surface__override'.format(i_dcc_material.name)
                    i_dcc_shader_path = '{}/{}'.format(i_dcc_material.get_parent().path, i_dcc_shader_name)
                    self._set_convert_to_occ_(i_dcc_material, i_dcc_shader_path)
    #
    @classmethod
    def _set_convert_to_occ_(cls, dcc_material, dcc_shader_path):
        dcc_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_shader:
            dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(dcc_shader)
            shader_type_name = dcc_shader_opt.get_type_name()
            if shader_type_name == 'lambert':
                cls._set_lambert_convert_to_occ_(dcc_shader_opt, dcc_shader_path)
            elif shader_type_name == 'standard_surface':
                cls._set_standard_surface_convert_to_occ_(dcc_shader_opt, dcc_shader_path)
    @classmethod
    def _set_lambert_convert_to_occ_(cls, dcc_shader_opt, dcc_shader_path):
        opacity_value = dcc_shader_opt.get_port_value('opacity')
        opacity_source = dcc_shader_opt.get_port_source('opacity')
        if opacity_source is None:
            if opacity_value == [1.0, 1.0, 1.0]:
                value = dcc_shader_opt.get_port_value('Kd_color')
                dcc_source = dcc_shader_opt.get_port_source('Kd_color')
                dcc_targets = dcc_shader_opt.get_port_targets('out')
                #
                dcc_occ = ktn_dcc_objects.Node(dcc_shader_path)
                dcc_occ_opt = _ktn_dcc_opt_look.AndShaderOpt(dcc_occ)
                dcc_occ_opt.set_create('ambient_occlusion')
                dcc_occ_opt.set('white', value)
                if dcc_source is not None:
                    dcc_occ_opt.set_port_source('white', dcc_source, validation=True)
                if dcc_targets:
                    for i_dcc_target in dcc_targets:
                        dcc_occ_opt.set_port_target('out', i_dcc_target, validation=True)
    @classmethod
    def _set_standard_surface_convert_to_occ_(cls, dcc_shader_opt, dcc_shader_path):
        opacity_value = dcc_shader_opt.get_port_value('opacity')
        opacity_source = dcc_shader_opt.get_port_source('opacity')
        if opacity_source is None:
            if opacity_value == [1.0, 1.0, 1.0]:
                value = dcc_shader_opt.get_port_value('base_color')
                dcc_source = dcc_shader_opt.get_port_source('base_color')
                dcc_targets = dcc_shader_opt.get_port_targets('out')
                #
                dcc_occ = ktn_dcc_objects.Node(dcc_shader_path)
                dcc_occ_opt = _ktn_dcc_opt_look.AndShaderOpt(dcc_occ)
                dcc_occ_opt.set_create('ambient_occlusion')
                dcc_occ_opt.set('white', value)
                if dcc_source is not None:
                    dcc_occ_opt.set_port_source('white', dcc_source, validation=True)
                if dcc_targets:
                    for i_dcc_target in dcc_targets:
                        dcc_occ_opt.set_port_target('out', i_dcc_target, validation=True)
    @classmethod
    def _set_occ_create_(cls, dcc_material, dcc_path, color):
        dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_objects.Node(dcc_path)
        )
        dcc_shader_opt.set_create('ambient_occlusion')
        dcc_shader_opt.set_port_target(
            'out', dcc_material.get_input_port('arnoldSurface'),
            validation=True
        )
        dcc_shader_opt.set('white', color)
    @classmethod
    def _set_opacity_lambert_create_(cls, dcc_material, dcc_path):
        dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_objects.Node(dcc_path)
        )
        dcc_shader_opt.set_create('lambert')
        dcc_shader_opt.set_port_target(
            'out', dcc_material.get_input_port('arnoldSurface'),
            validation=True
        )
        dcc_shader_opt.set('opacity', [0.0, 0.0, 0.0])
    #
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_auto_white_disp_assign(self, pass_name='default'):
        configure = self._workspace.get_configure(pass_name)
        # geometry_root = configure.get('option.geometry_root')
        material_root = configure.get('option.material_root')
        geometries = self._workspace.get_sg_geometries(pass_name)
        for i_geometry in geometries:
            i_geometry_type_name = i_geometry.type_name
            i_dcc_material_assign, i_ktn_material_assign = self._workspace.get_ng_geometry_material_assign(
                name=i_geometry.name,
                pass_name=pass_name
            )
            if i_ktn_material_assign is None:
                i_dcc_material, i_ktn_material = self._workspace.set_ng_material_create(
                    name=i_geometry.name,
                    pass_name=pass_name
                )
                self._workspace.set_ng_geometry_material_assign_create(
                    name=i_geometry.name,
                    assign=(
                        i_geometry.path,
                        '{}/{}'.format(material_root, i_dcc_material.name)
                    ),
                    pass_name=pass_name
                )
                i_dcc_shader_name = '{}__surface__override'.format(i_dcc_material.name)
                i_dcc_shader_path = '{}/{}'.format(i_dcc_material.get_parent().path, i_dcc_shader_name)
                if i_geometry_type_name in ['renderer procedural']:
                    i_color = (1,  0.955,  0.905)
                    self._set_plastic_create_(
                        i_dcc_material,
                        i_dcc_shader_path,
                        i_color
                    )
                elif i_geometry_type_name in ['subdmesh']:
                    self._set_white_create_(
                        i_dcc_material,
                        i_dcc_shader_path,
                    )
            else:
                i_material_path = i_dcc_material_assign.get_port(
                    'args.materialAssign.value'
                ).get()
                if i_material_path:
                    i_material_name = bsc_core.DccPathDagOpt(i_material_path).name
                    i_dcc_material = ktn_dcc_objects.Node(i_material_name)
                    i_dcc_shader_name = '{}__surface__override'.format(i_dcc_material.name)
                    i_dcc_shader_path = '{}/{}'.format(i_dcc_material.get_parent().path, i_dcc_shader_name)
                    if i_geometry_type_name in ['renderer procedural']:
                        self._set_convert_to_plastic_(i_dcc_material, i_dcc_shader_path, (1,  0.955,  0.905))
                    elif i_geometry_type_name in ['subdmesh']:
                        self._set_convert_to_white_(i_dcc_material, i_dcc_shader_path)

        dcc_look_pass, ktn_look_pass = self._workspace.get_ng_look_pass(pass_name)
        if ktn_look_pass is not None:
            dcc_look_pass.set(
                'look_pass.scheme', pass_name
            )
    @classmethod
    def _set_plastic_create_(cls, dcc_material, dcc_path, color):
        dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_objects.Node(dcc_path)
        )
        is_create = dcc_shader_opt.set_create('utility')
        if is_create is True:
            dcc_shader_opt.set_port_target(
                'out', dcc_material.get_input_port('arnoldSurface'),
                validation=True
            )
            dcc_shader_opt.set('shade_mode', '4')
            dcc_shader_opt.set('color', color)
        return dcc_shader_opt
    @classmethod
    def _set_convert_to_plastic_(cls, dcc_material, dcc_shader_path, color):
        dcc_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_shader:
            dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(dcc_shader)
            dcc_targets = dcc_shader_opt.get_port_targets('out')
            #
            dcc_plastic_opt = cls._set_plastic_create_(
                dcc_material, dcc_shader_path, color
            )
    @classmethod
    def _set_ambocc_create_(cls, dcc_material, dcc_path, color):
        dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_objects.Node(dcc_path)
        )
        dcc_shader_opt.set_create('utility')
        dcc_shader_opt.set_port_target(
            'out', dcc_material.get_input_port('arnoldSurface'),
            validation=True
        )
        dcc_shader_opt.set('shade_mode', '3')
        dcc_shader_opt.set('color', color)
    @classmethod
    def _set_white_create_(cls, dcc_material, dcc_path):
        dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_objects.Node(dcc_path)
        )
        is_create = dcc_shader_opt.set_create('standard_surface')
        if is_create is True:
            dcc_shader_opt.set_port_target(
                'out', dcc_material.get_input_port('arnoldSurface'),
                validation=True
            )
            for k, v in cls.WHITE_DICT.items():
                dcc_shader_opt.set(k, v)
        return dcc_shader_opt
    @classmethod
    def _set_displacement_fix_(cls, dcc_material, dcc_path):
        dcc_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(
            ktn_dcc_objects.Node(dcc_path)
        )
        output_min, output_max = dcc_shader_opt.get_port_value('output_min'), dcc_shader_opt.get_port_value('output_max')
        min_value, max_value = min(output_min, output_max), max(output_min, output_max)
        dcc_shader_opt.set_port_value('output_min', max_value), dcc_shader_opt.set_port_value('output_max', min_value)
        return dcc_shader_opt
    @classmethod
    def _set_convert_to_white_(cls, dcc_material, dcc_shader_path):
        dcc_surface_shader = dcc_material.get_input_port('arnoldSurface').get_source_obj()
        if dcc_surface_shader:
            dcc_surface_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(dcc_surface_shader)
            dcc_surface_targets = dcc_surface_shader_opt.get_port_targets('out')
            dcc_surface_white_opt = cls._set_white_create_(dcc_material, dcc_shader_path)
        #
        dcc_displacement_shader = dcc_material.get_input_port('arnoldDisplacement').get_source_obj()
        if dcc_displacement_shader:
            dcc_displacement_shader_opt = _ktn_dcc_opt_look.AndShaderOpt(dcc_displacement_shader)
            dcc_displacement_targets = dcc_displacement_shader_opt.get_port_targets('out')
            # dcc_displacement_white_opt = cls._set_displacement_fix_(dcc_material, dcc_shader_path)
    #
    @_ktn_mdf_utility.set_undo_mark_mdf
    def set_auto_geometry_properties_assign(self, pass_name='default'):
        geometries = self._workspace.get_sg_geometries(pass_name)
        for i_geometry in geometries:
            i_geometry_type_name = i_geometry.type_name
            i_dcc_material_assign, i_ktn_material_assign = self._workspace.get_ng_geometry_property_assign(
                name=i_geometry.name,
                pass_name=pass_name
            )
            if i_ktn_material_assign is not None:
                if i_geometry_type_name in ['subdmesh']:
                    self._workspace._set_arnold_geometry_properties_(
                        i_dcc_material_assign,
                        dict(
                            smoothing=True,
                            subdiv_type='catclark',
                            subdiv_iterations=2,
                            subdiv_smooth_derivs=True,
                        )
                    )
