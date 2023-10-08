# coding:utf-8
from lxbasic import bsc_core

from lxusd import usd_core

from lxutil import utl_core


class ClarisseUsdCleanup(object):
    KEY = 'clarisse USD cleanup'

    def __init__(self, file_path):
        self._file_path = file_path
        f_o = bsc_core.StgFileOpt(self._file_path)
        self._file_path_out = '{}.fix{}'.format(
            f_o.path_base, f_o.ext
        )
        self._file_path_out_usd = '{}.fix.usd'.format(
            f_o.path_base
        )
        self._file_path_out_usda = '{}.fix.usda'.format(
            f_o.path_base
        )
        self._stage_opt = usd_core.UsdStageOpt(self._file_path)

    def __fix_process(self):
        instance_prims = self._stage_opt.get_all_instance_prims()
        proto_prims = []
        with utl_core.GuiProgressesRunner.create(maximum=len(instance_prims), label='instance process') as g_p:
            for i_prim in instance_prims:
                i_instancer_opt = usd_core.UsdInstancerOpt(i_prim)
                i_group_prim = self.__fix_instance_process(i_prim)
                if i_group_prim is not None:
                    i_proto_prims_new = []
                    for j_prim in i_instancer_opt.get_proto_prims():
                        j_proto_prim = self.__fix_proto_process(i_group_prim, j_prim)
                        proto_prims.append(j_prim)
                        i_proto_prims_new.append(j_proto_prim)

                    i_instancer_opt.clear_proto()
                    i_instancer_opt.set_proto_prims(i_proto_prims_new)

                    self.__fix_proxy_process(i_prim)
                else:
                    i_instancer_opt.delete()

                g_p.set_update()

        [self._stage_opt.delete_obj(i) for i in proto_prims]

        self.__fix_clear_process()

    @classmethod
    def __fix_instance_process(cls, prim):
        opt = usd_core.UsdGeometryOpt(prim)
        proto_indices = opt.get('protoIndices')
        if proto_indices:
            c = len(proto_indices)
            # translate
            translates = opt.get('positions')
            if not translates:
                translates = usd_core.Vt.QuathArray([usd_core.Gf.Vec3f((0, 0, 0))]*c)
            opt.create_primvar_as_point('ist_translate', translates)

            # rotate
            orientations = opt.get('orientations')
            if not orientations:
                orientations = usd_core.Vt.QuathArray([usd_core.Gf.Quath(1, (0, 0, 0))]*c)
            opt.create_primvar_as_point(
                'ist_rotate', map(lambda x: tuple(usd_core.UsdQuaternion(x).to_rotate()), orientations)
            )
            opt.create_primvar_as_point(
                'ist_axis', map(lambda x: tuple(usd_core.UsdQuaternion(x).to_axis()), orientations)
            )
            opt.create_primvar_as_float(
                'ist_angle', map(lambda x: usd_core.UsdQuaternion(x).to_angle(), orientations)
            )
            # scale
            scales = opt.get('scales')
            if not scales:
                scales = usd_core.Vt.Vec3fArray([usd_core.Gf.Vec3f((1, 1, 1))]*c)
            opt.create_primvar_as_point('ist_scale', scales)
            # id
            proto_indices = opt.get('protoIndices')
            opt.create_primvar_as_integer('ist_id', range(len(proto_indices)))
            return opt.create_child('protos', 'Xform')
        else:
            bsc_core.LogMtd.trace_method_warning(
                cls.KEY, 'instance error: proto is not found for "{}"'.format(opt.get_path())
            )

    @classmethod
    def __fix_proto_process(cls, group_prim, prim):
        group_opt = usd_core.UsdPrimOpt(group_prim)
        opt = usd_core.UsdPrimOpt(prim)
        children = opt.get_children()
        reference_file_path = None
        if children:
            child = children[0]
            child_opt = usd_core.UsdPrimOpt(child)
            child_references = child_opt.get_references()
            if len(child_references) > 1:
                reference_file_path = child_references[-1][1]
                reference_file_path = reference_file_path.\
                    replace('/geometry/abc', '/geometry/usd').\
                    replace('.abc', '.usd')

        name = opt.get_name()
        prim_new = group_opt.create_child(name, 'Xform')
        prim_new_opt = usd_core.UsdTransformOpt(prim_new)
        if reference_file_path is not None:
            prim_new_opt.create_customize_attribute('usd_file', reference_file_path)
            prim_new_opt.add_reference(reference_file_path)
        else:
            bsc_core.LogMtd.trace_method_warning(
                cls.KEY, 'reference error: file is not found for "{}"'.format(opt.get_path())
            )
        return prim_new

    @classmethod
    def __fix_proxy_process(cls, prim):
        c_widths = []
        c_points = []
        c_counts = []
        c_colors = []

        geometries = []
        opt = usd_core.UsdInstancerOpt(prim)
        for i_prim in opt.get_proto_prims():
            i_opt = usd_core.UsdTransformOpt(i_prim)
            i_usd_file_path = i_opt.get_customize_attribute('usd_file')
            if i_usd_file_path is not None:
                geometries.append(i_opt.compute_geometry_args())
            else:
                geometries.append(None)

        proto_indices = opt.get('protoIndices')
        if proto_indices:
            c = len(proto_indices)
            translates = opt.get('positions')
            if not translates:
                translates = usd_core.Vt.QuathArray([usd_core.Gf.Vec3f((0, 0, 0))]*c)
            orientations = opt.get('orientations')
            if not orientations:
                orientations = usd_core.Vt.QuathArray([usd_core.Gf.Quath(1, (0, 0, 0))]*c)
            scales = opt.get('scales')
            if not scales:
                scales = usd_core.Vt.Vec3fArray([usd_core.Gf.Vec3f((1, 1, 1))]*c)

            c_r = bsc_core.RgbRange(c)

            for i_index, i_center in enumerate(translates):
                i_proto_index = proto_indices[i_index]
                i_geometry = geometries[i_proto_index]
                if i_geometry is None:
                    continue

                i_orientation = orientations[i_index]
                i_scale = scales[i_index]
                i_size = i_geometry[2]
                i_rgb = c_r.get_rgb(i_index, maximum=1.0)
                i_x, i_y, i_z = i_center
                i_w, i_h, i_d = i_size
                i_w, i_h, i_d = i_w, i_h, i_d
                i_transformation_matrix = usd_core.UsdTransformation(
                    i_center, i_orientation, i_scale
                ).to_matrix()
                # y line
                i_p_y_o = usd_core.Gf.Vec3f(i_x, i_y+i_h, i_z)
                i_p_y = i_transformation_matrix.Transform(i_p_y_o)
                i_points_y = [i_center, i_center, i_p_y, i_p_y]
                c_points.extend(i_points_y)
                c_counts.append(len(i_points_y))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # z line
                i_p_z_o = usd_core.Gf.Vec3f(i_x, i_y, i_z+i_d/2)
                i_p_z = i_transformation_matrix.Transform(i_p_z_o)
                i_points_z = [i_center, i_center, i_p_z, i_p_z]
                c_points.extend(i_points_z)
                c_counts.append(len(i_points_z))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # cross line
                i_p_cross_p_0_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y, i_z-i_d/2)
                i_p_cross_p_0_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y, i_z+i_d/2)
                i_p_cross_p_0_0 = i_transformation_matrix.Transform(i_p_cross_p_0_0_o)
                i_p_cross_p_0_1 = i_transformation_matrix.Transform(i_p_cross_p_0_1_o)
                i_points_cross_0 = [i_p_cross_p_0_0, i_p_cross_p_0_0, i_p_cross_p_0_1, i_p_cross_p_0_1]
                c_points.extend(i_points_cross_0)
                c_counts.append(len(i_points_cross_0))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

                i_p_cross_p_1_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y, i_z+i_d/2)
                i_p_cross_p_1_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y, i_z-i_d/2)
                i_p_cross_p_1_0 = i_transformation_matrix.Transform(i_p_cross_p_1_0_o)
                i_p_cross_p_1_1 = i_transformation_matrix.Transform(i_p_cross_p_1_1_o)
                i_points_cross_1 = [i_p_cross_p_1_0, i_p_cross_p_1_0, i_p_cross_p_1_1, i_p_cross_p_1_1]
                c_points.extend(i_points_cross_1)
                c_counts.append(len(i_points_cross_1))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # arrow line
                i_p_arrow_p_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y+i_h/2, i_z)
                i_p_arrow_p_0 = i_transformation_matrix.Transform(i_p_arrow_p_0_o)
                i_points_arrow_0 = [i_p_arrow_p_0, i_p_arrow_p_0, i_p_y, i_p_y]
                c_points.extend(i_points_arrow_0)
                c_counts.append(len(i_points_arrow_0))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

                i_p_arrow_p_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y+i_h/2, i_z)
                i_p_arrow_p_1 = i_transformation_matrix.Transform(i_p_arrow_p_1_o)
                i_points_arrow_1 = [i_p_arrow_p_1, i_p_arrow_p_1, i_p_y, i_p_y]
                c_points.extend(i_points_arrow_1)
                c_counts.append(len(i_points_arrow_1))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

            proxy_prim = opt.create_sibling('{}_proxy'.format(opt.get_name()), 'BasisCurves')
            proxy_opt = usd_core.UsdGeometryOpt(proxy_prim)
            proxy_opt.set_purpose_as_proxy()

            basis_curves_opt = usd_core.UsdBasisCurvesOpt(proxy_prim)
            basis_curves_opt.create(
                c_counts, c_points, c_widths
            )
            basis_curves_opt.set_display_colors_as_uniform(c_colors)

    def __fix_clear_process(self):
        for i in self._stage_opt.get_all_points_prims():
            self._stage_opt.delete_obj(i)

    def fix(self):
        self.__fix_process()

    def build(self):
        pass

    def save(self):
        self._stage_opt.usd_instance.GetRootLayer().Export(self._file_path_out)

    def save_as_usd(self):
        self._stage_opt.usd_instance.GetRootLayer().Export(self._file_path_out_usd)

    def save_as_usda(self):
        self._stage_opt.usd_instance.GetRootLayer().Export(self._file_path_out_usda)

    def extract_points_to(self, file_path):
        output_stage_opt = usd_core.UsdStageOpt()
        instance_prims = self._stage_opt.get_all_instance_prims()
        output_stage_opt.copy_one_from(self._stage_opt.get_default_prim())
        c = len(instance_prims)

        c_r = bsc_core.RgbRange(c)
        with utl_core.GuiProgressesRunner.create(maximum=len(instance_prims), label='instance process') as g_p:
            for i_seq, i_prim in enumerate(instance_prims):
                g_p.set_update()
                i_instancer_opt = usd_core.UsdInstancerOpt(i_prim)
                i_prim_parent = i_instancer_opt.get_parent()
                output_stage_opt.copy_many_from(i_prim_parent)
                i_positions = i_instancer_opt.get_positions()
                i_scales = i_instancer_opt.get_scales()
                i_proto_indices = i_instancer_opt.get_proto_indices()
                s_r = bsc_core.SVRange(max(i_proto_indices)+1)
                i_point_prim = output_stage_opt.create_one(
                    i_instancer_opt.get_path(), 'Points'
                )
                i_point_prim_opt = usd_core.UsdPointsOpt(i_point_prim)
                i_point_prim_opt.set_points(i_positions)
                if i_scales:
                    i_point_prim_opt.set_width_as_vertex(map(lambda _x: _x[1], i_scales))
                else:
                    i_point_prim_opt.set_width_as_vertex([1]*len(i_positions))
                i_point_prim_opt.set_display_colors_as_vertex(
                    map(lambda _x: c_r.get_rgb(i_seq, maximum=1, s_p=s_r.get(_x), v_p=100), i_proto_indices)
                )

        output_stage_opt.export_to(
            file_path
        )


class ClarisseUsdCleanupNew(object):
    KEY = 'clarisse USD transfer'

    def __init__(self, file_path):
        self._file_path = file_path
        f_o = bsc_core.StgFileOpt(self._file_path)
        self._file_path_out = '{}.fix{}'.format(
            f_o.path_base, f_o.ext
        )
        self._file_path_out_usd = '{}.fix.usd'.format(
            f_o.path_base
        )
        self._file_path_out_usda = '{}.fix.usda'.format(
            f_o.path_base
        )
        self._stage_opt = usd_core.UsdStageOpt(self._file_path)
        self._stage_opt_new = usd_core.UsdStageOpt()

    def transfer(self):
        instance_prims = self._stage_opt.get_all_instance_prims()
        with utl_core.GuiProgressesRunner.create(maximum=len(instance_prims), label='instance process') as g_p:
            for i_instance_prim in instance_prims:
                i_instancer_opt = usd_core.UsdInstancerOpt(i_instance_prim)
                i_proto_indices = i_instancer_opt.get_proto_indices()
                if i_proto_indices:
                    i_ps = i_instancer_opt.find_ancestors(['PointInstancer'])
                    if i_ps:
                        if len(i_ps) == 1:
                            i_instance_parent_path = usd_core.UsdPrimOpt(i_ps[0]).get_path()
                            i_instance_parent_prim_new = self._stage_opt_new.get_obj(i_instance_parent_path)
                            if i_instance_parent_prim_new.IsValid() is False:
                                raise RuntimeError()

                            i_instance_parent_opt_new = usd_core.UsdInstancerOpt(i_instance_parent_prim_new)
                            i_instance_group_prim_new = i_instance_parent_opt_new.create_child('protos', 'Xform')
                            i_instance_group_opt_new = usd_core.UsdPrimOpt(i_instance_group_prim_new)
                            i_instance_group_opt_new.set_kind_as_subcomponent()
                            i_instance_prim_new = i_instance_group_opt_new.create_child(
                                i_instancer_opt.get_name(), 'PointInstancer'
                            )
                            i_instance_parent_opt_new.set_proto_prims([i_instance_prim_new])
                            self.create_proxy(i_instance_parent_prim_new)
                        elif len(i_ps) > 1:
                            bsc_core.LogMtd.trace_method_error(
                                self.KEY, 'instance nested depth is more then 1: "{}"'.format(i_instancer_opt.get_path())
                            )
                            continue
                    else:
                        i_instance_parent_prim = i_instancer_opt.get_parent()
                        i_instance_parent_prim_new = self._stage_opt_new.copy_many_from(i_instance_parent_prim)
                        i_instance_parent_opt_new = usd_core.UsdPrimOpt(i_instance_parent_prim_new)

                        i_instance_prim_new = i_instance_parent_opt_new.create_child(
                            i_instancer_opt.get_name(), 'PointInstancer'
                        )

                    i_instance_opt_new = usd_core.UsdInstancerOpt(i_instance_prim_new)

                    self.transfer_protos(i_instancer_opt, i_instance_opt_new)

                    i_instance_opt_new.set_proto_indices(
                        i_instancer_opt.get_proto_indices()
                    )
                    i_instance_opt_new.set_positions(
                        i_instancer_opt.get_positions()
                    )
                    i_instance_opt_new.set_orientations(
                        i_instancer_opt.get_orientations()
                    )
                    i_instance_opt_new.set_scales(
                        i_instancer_opt.get_scales()
                    )
                    # bottom level
                    if not i_instancer_opt.find_descendants(['PointInstancer']):
                        self.create_properties(i_instance_prim_new)
                        # top level
                        if not i_ps:
                            self.create_proxy(i_instance_prim_new)

                else:
                    bsc_core.LogMtd.trace_method_warning(
                        self.KEY, 'instance error: proto is not found for "{}"'.format(i_instancer_opt.get_path())
                    )

                g_p.set_update()

    def transfer_protos(self, instancer_opt, instance_opt_new):
        i_proto_prims_new = []
        for i_proto_prim in instancer_opt.get_proto_prims():
            i_proto_opt = usd_core.UsdPrimOpt(i_proto_prim)

            i_proto_group_prim_new = instance_opt_new.create_child('protos', 'Xform')
            i_proto_group_opt_new = usd_core.UsdPrimOpt(i_proto_group_prim_new)

            i_is_create, i_reference_file_path = self.find_reference(i_proto_prim)
            if i_reference_file_path is not None:
                i_proto_prim_new = i_proto_group_opt_new.create_child(i_proto_opt.get_name(), 'Xform')
                i_proto_prims_new.append(i_proto_prim_new)
                i_proto_opt_new = usd_core.UsdTransformOpt(i_proto_prim_new)

                i_reference_file_path = i_reference_file_path.\
                    replace('/geometry/abc', '/geometry/usd').\
                    replace('.abc', '.usd')

                i_proto_opt_new.create_customize_attribute('usd_file', i_reference_file_path)
                i_proto_opt_new.add_reference(i_reference_file_path)
            else:
                if i_is_create is True:
                    i_proto_path_new = '{}/{}'.format(i_proto_group_opt_new.get_path(), i_proto_opt.get_name())
                    if not self._stage_opt_new.get_exists_obj(i_proto_path_new):
                        i_proto_prim_new = i_proto_group_opt_new.create_child(i_proto_opt.get_name(), 'Xform')
                        i_proto_prims_new.append(i_proto_prim_new)

        instance_opt_new.set_proto_prims(i_proto_prims_new)

    def find_reference(self, proto_prim):
        proto_opt = usd_core.UsdPrimOpt(proto_prim)
        children = proto_opt.get_children()
        if children:
            child = children[0]
            child_opt = usd_core.UsdPrimOpt(child)
            if child_opt.get_type_name() == 'Mesh':
                child_references = child_opt.get_references()
                for i_child_reference in child_references:
                    i_path, i_file_path = i_child_reference
                    if i_file_path != self._file_path:
                        return True, i_file_path
            elif child_opt.get_type_name() == 'PointInstancer':
                return False, None
        else:
            return True, None

    def create_properties(self, instance_prim_new):
        opt = usd_core.UsdGeometryOpt(instance_prim_new)

        proto_indices = opt.get('protoIndices')
        if proto_indices:
            c = len(proto_indices)
            # translate
            translates = opt.get('positions')
            if not translates:
                translates = usd_core.Vt.QuathArray([usd_core.Gf.Vec3f((0, 0, 0))]*c)
            opt.create_primvar_as_point('ist_translate', translates)

            # rotate
            orientations = opt.get('orientations')
            if not orientations:
                orientations = usd_core.Vt.QuathArray([usd_core.Gf.Quath(1, (0, 0, 0))]*c)
            opt.create_primvar_as_point(
                'ist_rotate', map(lambda x: tuple(usd_core.UsdQuaternion(x).to_rotate()), orientations)
            )
            opt.create_primvar_as_point(
                'ist_axis', map(lambda x: tuple(usd_core.UsdQuaternion(x).to_axis()), orientations)
            )
            opt.create_primvar_as_float(
                'ist_angle', map(lambda x: usd_core.UsdQuaternion(x).to_angle(), orientations)
            )
            # scale
            scales = opt.get('scales')
            if not scales:
                scales = usd_core.Vt.Vec3fArray([usd_core.Gf.Vec3f((1, 1, 1))]*c)
            opt.create_primvar_as_point('ist_scale', scales)
            # id
            proto_indices = opt.get('protoIndices')
            opt.create_primvar_as_integer('ist_id', range(len(proto_indices)))
            return opt.create_child('protos', 'Xform')
        else:
            bsc_core.LogMtd.trace_method_warning(
                self.KEY, 'instance error: proto is not found for "{}"'.format(opt.get_path())
            )

    def create_proxy(self, instance_prim_new):
        opt = usd_core.UsdInstancerOpt(instance_prim_new)

        c_widths = []
        c_points = []
        c_counts = []
        c_colors = []

        geometries = []
        for i_prim in opt.get_proto_prims():
            i_opt = usd_core.UsdTransformOpt(i_prim)
            i_usd_file_path = i_opt.get_customize_attribute('usd_file')
            if i_usd_file_path is not None:
                geometries.append(i_opt.compute_geometry_args())
            else:
                geometries.append(None)

        proto_indices = opt.get('protoIndices')
        if proto_indices:
            c = len(proto_indices)
            translates = opt.get('positions')
            if not translates:
                translates = usd_core.Vt.QuathArray([usd_core.Gf.Vec3f((0, 0, 0))]*c)
            orientations = opt.get('orientations')
            if not orientations:
                orientations = usd_core.Vt.QuathArray([usd_core.Gf.Quath(1, (0, 0, 0))]*c)
            scales = opt.get('scales')
            if not scales:
                scales = usd_core.Vt.Vec3fArray([usd_core.Gf.Vec3f((1, 1, 1))]*c)

            c_r = bsc_core.RgbRange(c)

            for i_index, i_center in enumerate(translates):
                i_proto_index = proto_indices[i_index]
                i_geometry = geometries[i_proto_index]
                if i_geometry is None:
                    continue

                i_orientation = orientations[i_index]
                i_scale = scales[i_index]
                i_size = i_geometry[2]
                i_rgb = c_r.get_rgb(i_index, maximum=1.0)
                i_x, i_y, i_z = i_center
                i_w, i_h, i_d = i_size
                i_w, i_h, i_d = i_w, i_h, i_d
                i_transformation_matrix = usd_core.UsdTransformation(
                    i_center, i_orientation, i_scale
                ).to_matrix()
                # y line
                i_p_y_o = usd_core.Gf.Vec3f(i_x, i_y+i_h, i_z)
                i_p_y = i_transformation_matrix.Transform(i_p_y_o)
                i_points_y = [i_center, i_center, i_p_y, i_p_y]
                c_points.extend(i_points_y)
                c_counts.append(len(i_points_y))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # z line
                i_p_z_o = usd_core.Gf.Vec3f(i_x, i_y, i_z+i_d/2)
                i_p_z = i_transformation_matrix.Transform(i_p_z_o)
                i_points_z = [i_center, i_center, i_p_z, i_p_z]
                c_points.extend(i_points_z)
                c_counts.append(len(i_points_z))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # cross line
                i_p_cross_p_0_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y, i_z-i_d/2)
                i_p_cross_p_0_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y, i_z+i_d/2)
                i_p_cross_p_0_0 = i_transformation_matrix.Transform(i_p_cross_p_0_0_o)
                i_p_cross_p_0_1 = i_transformation_matrix.Transform(i_p_cross_p_0_1_o)
                i_points_cross_0 = [i_p_cross_p_0_0, i_p_cross_p_0_0, i_p_cross_p_0_1, i_p_cross_p_0_1]
                c_points.extend(i_points_cross_0)
                c_counts.append(len(i_points_cross_0))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

                i_p_cross_p_1_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y, i_z+i_d/2)
                i_p_cross_p_1_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y, i_z-i_d/2)
                i_p_cross_p_1_0 = i_transformation_matrix.Transform(i_p_cross_p_1_0_o)
                i_p_cross_p_1_1 = i_transformation_matrix.Transform(i_p_cross_p_1_1_o)
                i_points_cross_1 = [i_p_cross_p_1_0, i_p_cross_p_1_0, i_p_cross_p_1_1, i_p_cross_p_1_1]
                c_points.extend(i_points_cross_1)
                c_counts.append(len(i_points_cross_1))
                c_widths.append(0.003)
                c_colors.append(i_rgb)
                # arrow line
                i_p_arrow_p_0_o = usd_core.Gf.Vec3f(i_x-i_w/2, i_y+i_h/2, i_z)
                i_p_arrow_p_0 = i_transformation_matrix.Transform(i_p_arrow_p_0_o)
                i_points_arrow_0 = [i_p_arrow_p_0, i_p_arrow_p_0, i_p_y, i_p_y]
                c_points.extend(i_points_arrow_0)
                c_counts.append(len(i_points_arrow_0))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

                i_p_arrow_p_1_o = usd_core.Gf.Vec3f(i_x+i_w/2, i_y+i_h/2, i_z)
                i_p_arrow_p_1 = i_transformation_matrix.Transform(i_p_arrow_p_1_o)
                i_points_arrow_1 = [i_p_arrow_p_1, i_p_arrow_p_1, i_p_y, i_p_y]
                c_points.extend(i_points_arrow_1)
                c_counts.append(len(i_points_arrow_1))
                c_widths.append(0.003)
                c_colors.append(i_rgb)

            proxy_prim = opt.create_sibling('{}_proxy'.format(opt.get_name()), 'BasisCurves')
            proxy_opt = usd_core.UsdGeometryOpt(proxy_prim)
            proxy_opt.set_purpose_as_proxy()

            basis_curves_opt = usd_core.UsdBasisCurvesOpt(proxy_prim)
            basis_curves_opt.create(
                c_counts, c_points, c_widths
            )
            basis_curves_opt.set_display_colors_as_uniform(c_colors)

    def save_as_usd(self):
        self._stage_opt_new.usd_instance.GetRootLayer().Export(self._file_path_out_usd)

    def save_as_usda(self):
        self._stage_opt_new.usd_instance.GetRootLayer().Export(self._file_path_out_usda)


if __name__ == '__main__':
    cc = ClarisseUsdCleanupNew(
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/clarisse/plants_039.usd'
    )
    cc.transfer()
    cc.save_as_usda()
