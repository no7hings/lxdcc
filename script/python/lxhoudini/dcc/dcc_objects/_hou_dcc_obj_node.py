# coding:utf-8
# noinspection PyUnresolvedReferences
import hou

from lxutil import commands

from .. import hou_dcc_obj_abs

from ...dcc.dcc_objects import _hou_dcc_obj_os

import lxutil.commands as utl_cmds


class Port(hou_dcc_obj_abs.AbsHouPort):
    def __init__(self, node, name, port_assign):
        super(Port, self).__init__(node, name, port_assign)


class Node(hou_dcc_obj_abs.AbsHouObj):
    PORT_CLS = Port
    def __init__(self, path):
        super(Node, self).__init__(path)


class FileReference(hou_dcc_obj_abs.AbsHouFileReferenceObj):
    PORT_CLS = Port
    OS_FILE_CLS = _hou_dcc_obj_os.OsFile
    def __init__(self, path, file_path=None):
        super(FileReference, self).__init__(path)
        self._set_file_reference_def_init_(file_path)


class ImageReference(hou_dcc_obj_abs.AbsHouFileReferenceObj):
    PORT_CLS = Port
    OS_FILE_CLS = _hou_dcc_obj_os.OsTexture
    def __init__(self, path, file_path=None):
        super(ImageReference, self).__init__(path, file_path)

    def get_image_attribute_names(self):
        lis = []
        for parm in self.hou_obj.allParms():
            parm_template = parm.parmTemplate()
            if parm_template.type() == hou.parmTemplateType.String:
                file_type = parm_template.fileType()
                if file_type == hou.fileType.Image:
                    lis.append(parm.name())
        return lis

    def get_image_file_paths(self):
        lis = []
        for port_path in self.get_image_attribute_names():
            os_image_file_path = self.get_port(port_path).get()
            lis.append(os_image_file_path)
        return lis


class Geometry(Node):
    def __init__(self, path):
        super(Geometry, self).__init__(path)

    def set_transformations(self, transformations):
        port_names = [
            ('tx', 'ty', 'tz'),
            ('rx', 'ry', 'rz'),
            ('sx', 'sy', 'sz'),
            # ('prx', 'pry', 'prz'),
            # ('px', 'py', 'pz'),
        ]
        for a, channel_names in enumerate(port_names):
            for b, channel_name in enumerate(channel_names):
                port = self.get_port(channel_name)
                port.set(transformations[a][b])

    def set_matrix(self, matrix):
        hou_obj = self.hou_obj
        hou_matrix = hou.Matrix4(matrix)
        hou_obj.setWorldTransform(hou_matrix)


class Camera(hou_dcc_obj_abs.AbsHouObj):
    PORT_CLS = Port
    def __init__(self, path):
        super(Camera, self).__init__(path)

    def set_resolution(self, w, h):
        self.get_port('resx').set(w), self.get_port('resy').set(h)


class ArOperate(hou_dcc_obj_abs.AbsHouObj):
    PORT_CLS = Port
    def __init__(self, path):
        super(ArOperate, self).__init__(path)


class ArMaterial(hou_dcc_obj_abs.AbsHouFileReferenceObj):
    PORT_CLS = Port
    OS_FILE_CLS = _hou_dcc_obj_os.OsTexture
    def __init__(self, path):
        super(ArMaterial, self).__init__(path)


class AndMaterialx(hou_dcc_obj_abs.AbsHouFileReferenceObj):
    PORT_CLS = Port
    OS_FILE_CLS = _hou_dcc_obj_os.OsTexture
    def __init__(self, path):
        super(AndMaterialx, self).__init__(path)

    def get_geometry_paths(self):
        ports = self.get_file_ports()
        if ports:
            port = ports[0]
            file_path = port.get()
            return commands.MaterialxReader(file_path).geometry_paths
        return []

    def get_texture_paths(self):
        ports = self.get_file_ports()
        if ports:
            port = ports[0]
            file_path = port.get()
            return commands.MaterialxReader(file_path).texture_paths
        return []

    def get_textures(self):
        return [self.OS_FILE_CLS(i) for i in self.get_texture_paths()]

    def get_file_plf_objs(self):
        lis = []
        for port_dcc_path, file_plf_path in self._reference_raw.items():
            lis.append(
                self._set_file_create_(file_plf_path, port_dcc_path)
            )
            mtx_reader = utl_cmds.MaterialxReader(file_plf_path)
            for i in mtx_reader.texture_paths:
                lis.append(
                    self._set_file_create_(i)
                )
        return lis


class Alembic(hou_dcc_obj_abs.AbsHouFileReferenceObj):
    PORT_CLS = Port
    OS_FILE_CLS = _hou_dcc_obj_os.OsFile
    MATERIALX_CLS = AndMaterialx
    def __init__(self, path, file_path=None):
        super(Alembic, self).__init__(path, file_path)

    def get_materialx_geometry_paths(self):
        parent = self.get_parent()
        if parent is not None:
            if parent.type == 'Object/geo':
                ar_opt_obj_path = parent.get_port('ar_operator_graph').get()
                hou_node = hou.node(ar_opt_obj_path)
                if hou_node is not None:
                    opt_type = hou_node.type().nameWithCategory()
                    if opt_type == 'arnold::Driver/materialx':
                        materialx = self.MATERIALX_CLS(ar_opt_obj_path)
                        materialx.set_file_port_raw_add('filename')
                        return materialx.get_geometry_paths()
        return []

    def get_geometry_paths(self):
        lis = []
        hou_obj = self.hou_obj
        if hou_obj is not None:
            geo = hou_obj.geometry()
            prims = geo.prims()
            for prim in prims:
                path = prim.attribValue('path')
                lis.append(path)
        return lis


class AlembicArchive(hou_dcc_obj_abs.AbsHouFileReferenceObj):
    PORT_CLS = Port
    OS_FILE_CLS = _hou_dcc_obj_os.OsFile
    MATERIALX_CLS = AndMaterialx
    CAMERA_CLS = Camera
    def __init__(self, path, file_path=None):
        super(AlembicArchive, self).__init__(path, file_path)

    def get_camera_paths(self):
        def _rcs_fnc(obj_):
            _type = obj_.type().nameWithCategory()
            if _type == 'Object/cam':
                lis.append(obj_.path())
            _child_objs = obj_.children()
            if _child_objs:
                for _child_obj in _child_objs:
                    _rcs_fnc(_child_obj)
        lis = []
        hou_obj = self.hou_obj
        if hou_obj is not None:
            _rcs_fnc(hou_obj)
        return lis

    def get_cameras(self):
        return [self.CAMERA_CLS(i) for i in self.get_camera_paths()]
