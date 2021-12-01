# coding:utf-8
from LxGraphic import grhCfg, grhObjAbs

from lxarnold import and_configure

from lxarnold.dcc.dcc_objects import _ar_dcc_obj_callback


class AbsDccBasic(object):
    pass


# ******************************************************************************************************************** #
class AbsDccObjLoader(
    AbsDccBasic,
    grhObjAbs.AbsGrhObjLoader,
):
    # noinspection PyUnusedLocal
    def _initAbsDccObjLoader(self, *args):
        self._initAbsGrhObjLoader(*args)
    @classmethod
    def _obj_loader_cls__get_obj_scene_obj_(cls):
        return _ar_dcc_obj_callback.__dict__['SCENE'].universe
    @classmethod
    def _obj_loader_cls__get_obj_exist_(cls, *args):
        nodeStr = args[0]
        universe = cls._obj_loader_cls__get_obj_scene_obj_()
        return universe.get_obj_exists(nodeStr)
    @classmethod
    def _obj_loader_cls__get_typepath_str_(cls, *args):
        nodeStr = args[0]
        universe = cls.getScene()
        node = universe.get_obj(nodeStr)
        return node.type.path
    @classmethod
    def _obj_loader_cls__get_node_path_str_(cls, *args):
        nodeStr = args[0]
        if cls._obj_loader_cls__get_obj_exist_(nodeStr) is True:
            universe = cls._obj_loader_cls__get_obj_scene_obj_()
            node = universe.get_obj(nodeStr)
            return node.path
    @classmethod
    def _obj_loader_cls__get_definition_node_raw_(cls, *args):
        typepathStr = args[0]
        return {
            cls.DEF_grh__keyword_node_typepath: typepathStr,
            cls.DEF_grh__key_node_datatype: None,
            cls.DEF_grh__key_port: []
        }
    @classmethod
    def _obj_loader_cls__get_customize_port_raw_(cls, *args):
        port = args[0]
        portPathStr = port.port_token
        datatypeStr = port.type.path
        assignDict = {
            and_configure.PortAssign.INPUTS: grhCfg.GrhPortAssignQuery.inport,
            and_configure.PortAssign.OUTPUTS: grhCfg.GrhPortAssignQuery.otport,
        }
        assignStr = assignDict[port.port_assign]
        return cls._obj_loader_cls__get_port_raw_(
            portpath=portPathStr,
            porttype=datatypeStr,
            datatype=datatypeStr,
            assign=assignStr
        )
    @classmethod
    def _obj_loader_cls__get_customize_port_raw_list_(cls, *args, **kwargs):
        nodeStr = args[0]
        lis = []
        universe = cls.getScene()
        node = universe.get_obj(nodeStr)
        input_ports = node.get_input_ports()
        for input_port in input_ports:
            if input_port.get_is_element() is False:
                portRaw = cls._obj_loader_cls__get_customize_port_raw_(input_port)
                if portRaw:
                    lis.append(portRaw)
        output_ports = node.get_output_ports()
        for output_port in output_ports:
            if output_port.get_is_element() is False:
                portRaw = cls._obj_loader_cls__get_customize_port_raw_(output_port)
                if portRaw:
                    lis.append(portRaw)
        return lis
    @classmethod
    def _obj_loader_cls__get_node_parent_exist_(cls, *args):
        nodeStr = args[0]
        universe = cls.getScene()
        node = universe.get_obj(nodeStr)
        return node.get_parent_exists()
    # port
    @classmethod
    def _obj_loader_cls__get_port_obj_(cls, *args):
        nodeStr, portPathStr = args
        universe = cls.getScene()
        node = universe.get_obj(nodeStr)
        return node.get_port(portPathStr)
    @classmethod
    def _obj_loader_cls__get_port_portraw_(cls, *args, **kwargs):
        port = cls.getNodePort(*args)
        return port.get()
    @classmethod
    def _obj_loader_cls__get_port_source_exist_(cls, *args, **kwargs):
        port = cls.getNodePort(*args)
        return port.get_source_exists()
    @classmethod
    def _obj_loader_cls__get_port_source_path_(cls, *args, **kwargs):
        port = cls.getNodePort(*args)
        return port.get_source().token


# ******************************************************************************************************************** #
class AbsDccObjQueryrawCreator(grhObjAbs.AbsGrhObjQueryrawCreator):
    def _initAbsDccObjQueryrawCreator(self, *args):
        self._initAbsGrhObjQueryBuilder(*args)

    # **************************************************************************************************************** #
    def _queryraw_creator__get_node_raw_(self, *args):
        return self.CLS_grh__obj_query_creator__obj_loader.getDefinitionNodeRaw(*args)


# ******************************************************************************************************************** #
class AbsDccObjQueue(grhObjAbs.AbsGrhObjQueue):
    def _initAbsDccObjQueue(self, *args):
        self._initAbsGrhObjQueue(*args)


# ******************************************************************************************************************** #
class AbsDccConnector(grhObjAbs.AbsGrhConnector):
    def _initAbsDccConnector(self, *args):
        self._initAbsGrhConnector(*args)


# ******************************************************************************************************************** #
class AbsDccPort(grhObjAbs.AbsGrhPort):
    def _initAbsDccPort(self, *args):
        self._initAbsGrhPort(*args)

    # **************************************************************************************************************** #
    def _inport__get_source_exist_(self, *args):
        if grhCfg.GrhPortAssignQuery.isInport(self.assignString()):
            return AbsDccObjLoader.getPortSourceExists(
                self.path().nodepathString(), self.path().portpathString()
            )
        return False

    def _inport__get_source_port_obj_(self, *args):
        if self._inport__get_source_exist_() is True:
            attrPathStr = AbsDccObjLoader.getPortSourcePath(
                self.path().nodepathString(), self.path().portpathString()
            )
            # covert to attribute object
            _attrPathObj = self.CLS_grh__obj__path(attrPathStr)
            _nodepathStr, _portpathStr = _attrPathObj.nodepathString(), _attrPathObj.portpathString()

            portObj = self._grh__port__get_port_cache_obj_(
                (_nodepathStr,),
                # source: otport > target: inport
                (_portpathStr, grhCfg.GrhPortAssignQuery.otport)
            )
            return portObj

    # **************************************************************************************************************** #
    def _grh__port__get_portraw_(self, *args, **kwargs):
        if grhCfg.GrhPortAssignQuery.isInport(self.assignString()):
            return AbsDccObjLoader.getPortPortraw(
                self.path().nodepathString(), self.path().portpathString(),
                *args, **kwargs
            )


class AbsDccObj(grhObjAbs.AbsGrhNode):
    def _initAbsDccNode(self, *args, **kwargs):
        if args:
            # nodepath
            if len(args) == 1:
                _ = args[0]
                if AbsDccObjLoader.getNodeIsExist(_) is True:
                    typepathStr = AbsDccObjLoader.getNodeTypepath(_)
                    nodePathStr = AbsDccObjLoader.getNodePath(_)
                else:
                    raise TypeError(
                        '''Node: "{}" is Non-exists'''.format(_)
                    )
            # ( category, nodepath )
            elif len(args) == 2:
                typepathStr, nodePathStr = args
                self._initAbsGrhNode(*args)
            else:
                raise TypeError()
            # initialization
            self._initAbsGrhNode(typepathStr, nodePathStr, **kwargs)
            # add custom port
            portRawList = AbsDccObjLoader.getCustomizePortRaws(nodePathStr)
            [self._grh_node__set_customize_port_obj_create_(i) for i in portRawList]
        else:
            raise TypeError()
    # hierarchy ****************************************************************************************************** #
    def _obj__get_parent_exist_(self, *args):
        return AbsDccObjLoader.getNodeHasParent(
                self.pathString()
            )

    def _obj__get_parent_obj_(self, *args):
        if self._obj__get_parent_exist_() is True:
            _nodepathStr = AbsDccObjLoader.getNodeParentPath(
                self.pathString()
            )
            return self._node_cls__get_node_cache_obj_(_nodepathStr)

    def _obj__get_children_exist_(self, *args):
        return AbsDccObjLoader.getNodeHasChildren(
            self.pathString()
        )

    def _obj__get_child_obj_list_(self, *args, **kwargs):
        def getArgsFnc_(kwargs_):
            _asString = False
            if kwargs_:
                if u'asString' in kwargs_:
                    _asString = kwargs_[u'asString']

            return _asString

        asString = getArgsFnc_(kwargs)

        if self._obj__get_children_exist_() is True:
            _nodePathStrList = AbsDccObjLoader.getNodeChildPaths(
                self.pathString(), *args, **kwargs
            )
            if asString is True:
                return _nodePathStrList
            return [self._node_cls__get_node_cache_obj_(_i) for _i in _nodePathStrList]
        return []

    def _obj__get_all_child_obj_list_(self, *args, **kwargs):
        def getArgsFnc_(kwargs_):
            _asString = False
            if kwargs_:
                if u'asString' in kwargs_:
                    _asString = kwargs_[u'asString']

            return _asString

        asString = getArgsFnc_(kwargs)

        if self._obj__get_children_exist_() is True:
            _nodePathStrList = AbsDccObjLoader.getNodeAllChildPaths(
                self.pathString(), *args, **kwargs
            )
            if asString is True:
                return _nodePathStrList
            return [self._node_cls__get_node_cache_obj_(_i) for _i in _nodePathStrList]
        return []
