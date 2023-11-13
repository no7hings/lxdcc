# coding:utf-8
from lxusd.warp import *
#
from lxusd import usd_core
#
from lxutil.fnc import utl_fnc_obj_abs

import lxarnold.dcc.dcc_objects as and_dcc_objects


class LookPropertiesUsdExporter(utl_fnc_obj_abs.AbsDccExporter):
    OPTION = dict(
        ass_file=None,
        ignore_default=False
    )

    def __init__(self, file_path, root=None, option=None):
        super(LookPropertiesUsdExporter, self).__init__(file_path, root, option)
        #
        self._usd_stage = Usd.Stage.CreateInMemory()
        self._usd_stage_opt = usd_core.UsdStageOpt(self._usd_stage)
        self._usd_stage_opt.set_root_create(self._root, override=True)

    def set_run(self):
        ass_file_path = self._option['ass_file']
        ignore_default = self._option['ignore_default']
        root = self._root
        scene = and_dcc_objects.Scene()
        scene.load_from_dot_ass(
            ass_file_path,
            path_lstrip='/root/world/geo'
        )
        universe = scene.universe
        #
        dcc_root = universe.get_obj(root)
        if dcc_root:
            dcc_objs = dcc_root.get_descendants()
            for j_dcc_obj in dcc_objs:
                i_usd_prim = self._usd_stage_opt.set_obj_create_as_override(j_dcc_obj.path)
                if j_dcc_obj.type_name in ['mesh', 'xgen_description']:
                    i_usd_geometry_opt = usd_core.UsdGeometryOpt(i_usd_prim)
                    for j_dcc_port in j_dcc_obj.get_ports():
                        if j_dcc_port.name == 'material':
                            pass
                        else:
                            # ignore value changed
                            if ignore_default is True:
                                if j_dcc_port.get_is_value_changed() is False:
                                    continue
                            #
                            if j_dcc_port.get_is_element() is False and j_dcc_port.get_is_channel() is False:
                                j_port_path = 'arnold:{}'.format(j_dcc_port.name)
                                i_usd_geometry_opt.create_customize_port(
                                    j_port_path, j_dcc_port.type, j_dcc_port.get()
                                )
        #
        self._usd_stage_opt.set_flatten()
        self._usd_stage_opt.export_to(
            self._file_path
        )
