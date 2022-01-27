# coding:utf-8
# noinspection PyUnresolvedReferences
import hou

from lxutil import utl_core, utl_abstract

from lxhoudini import hou_configure


class AbsHouPort(utl_abstract.AbsDccPort):
    PATHSEP = hou_configure.Util.PORT_PATHSEP
    def __init__(self, node, name, port_assign):
        super(AbsHouPort, self).__init__(node, name, port_assign)
    @property
    def type(self):
        if self.get_is_exists() is True:
            return hou.parm(self.path).parmTemplate().type().name()
    @property
    def hou_port(self):
        return hou.parm(self.path)

    def get_is_exists(self):
        return hou.parm(self.path) is not None

    def set_create(self, *args):
        pass

    def get(self):
        if self.get_is_exists() is True:
            return hou.parm(self.path).eval()

    def set(self, value, expression=False):
        if expression is True:
            hou.parm(self.path).setExpression(unicode(value))
        else:
            hou.parm(self.path).set(value)


class AbsHouObj(utl_abstract.AbsDccObj):
    PATHSEP = '/'
    def __init__(self, path):
        super(AbsHouObj, self).__init__(path)
    @property
    def type(self):
        hou_node = hou.node(self.path)
        if hou_node is not None:
            return hou_node.type().nameWithCategory()
        return ''
    @property
    def icon(self):
        # noinspection PyBroadException
        try:
            hou_node = hou.node(self.path)
            if hou_node is not None:
                return hou.qt.Icon(hou_node.type().icon())
            return hou.qt.Icon('MISC_python')
        except:
            return hou.qt.Icon('MISC_python')
    @property
    def hou_obj(self):
        return hou.node(self.path)

    def _set_dag_create_(self, path):
        return self.__class__(path)

    def get_is_file_reference(self):
        return False

    def get_is_exists(self):
        return hou.node(self.path) is not None

    def set_create(self, obj_type):
        parent_path = self.get_parent_path()
        hou_parent = hou.node(parent_path)
        if hou_parent is not None:
            hou_obj = hou_parent.createNode(obj_type, self.name)
            utl_core.Log.set_module_result_trace(
                'obj create',
                'obj="{}", type="{}"'.format(self.path, self.type)
            )
            hou_obj.moveToGoodPosition()
            return hou_obj

    def get_dcc_instance(self, obj_type, obj_path=None, *args, **kwargs):
        hou_obj = hou.node(self.path)
        if hou_obj is None:
            hou_obj = self.set_create(obj_type)
            return hou_obj, True
        else:
            exists_obj_type = hou_obj.type().name()
            if exists_obj_type != obj_type:
                self.set_delete()
                hou_obj = self.set_create(obj_type)
                return hou_obj, True
        return hou_obj, False

    def get_all_input_obj_paths(self, port_path):
        def _rcs_fnc(hou_obj_, index_):
            cs = hou_obj_.outputConnectors()[index_]
            for c in cs:
                _hou_obj = c.outputNode()
                _rcs_fnc(_hou_obj, index_)
                #
                lis.append(_hou_obj.path())
        #
        lis = []
        hou_obj = self.hou_obj
        if hou_obj is not None:
            index = hou_obj.outputIndex(port_path)
            _rcs_fnc(hou_obj, index)
        return lis

    def get_child_paths(self):
        hou_obj = self.hou_obj
        if hou_obj is not None:
            return [i.path() for i in hou_obj.children()]
        return []

    def _set_child_create_(self, path):
        return self.__class__(path)

    def set_delete(self):
        hou_obj = self.hou_obj
        if hou_obj is not None:
            hou_obj.destroy()
            utl_core.Log.set_result_trace(
                'delete node: "{}"'.format(self.path)
            )

    def get_is_display_enable(self):
        hou_obj = self.hou_obj
        if hou_obj is not None:
            return hou_obj.isGenericFlagSet(hou.nodeFlag.Display)
        return False

    def get_is_render_enable(self):
        hou_obj = self.hou_obj
        if hou_obj is not None:
            return hou_obj.isGenericFlagSet(hou.nodeFlag.Render)
        return False

    def set_display_enable(self, boolean):
        hou_obj = self.hou_obj
        if hou_obj is not None:
            hou_obj.setGenericFlag(hou.nodeFlag.Display, boolean)

    def set_render_enable(self, boolean):
        hou_obj = self.hou_obj
        if hou_obj is not None:
            hou_obj.setGenericFlag(hou.nodeFlag.Render, boolean)


class AbsHouFileReferenceObj(
    AbsHouObj,
    utl_abstract.AbsFileReferenceDef
):
    def __init__(self, path, file_path=None):
        super(AbsHouFileReferenceObj, self).__init__(path)
        # init file reference
        self._set_file_reference_def_init_(file_path)

    def get_is_file_reference(self):
        return True

    def get_is_multiply_reference(self):
        return False


class AbsHouObjs(utl_abstract.AbsDccObjs):
    FILE_REFERENCE_FILE_PORT_PATHS_DICT = {}
    def __init__(self, *args):
        super(AbsHouObjs, self).__init__(*args)
    @classmethod
    def get_paths(cls, exclude_paths=None):
        lis = []
        hou_node_types = [hou.nodeType(i) for i in cls.INCLUDE_DCC_TYPES]
        for hou_node_type in hou_node_types:
            for hou_node in hou_node_type.instances():
                lis.append(hou_node.path())
        return lis
    @classmethod
    def get_objs(cls, **kwargs):
        lis = []
        for obj_path in cls.get_paths():
            obj = cls.DCC_OBJ_CLASS(obj_path)
            obj_type = obj.type
            if obj_type in cls.FILE_REFERENCE_FILE_PORT_PATHS_DICT:
                port_paths = cls.FILE_REFERENCE_FILE_PORT_PATHS_DICT[obj_type]
                for port_path in port_paths:
                    file_path = obj.get_port(port_path).get()
                    obj.set_file_port_raw_add(
                        port_path, file_path
                    )
            lis.append(obj)
        return lis

