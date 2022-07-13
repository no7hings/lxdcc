# coding:utf-8
import inspect
#
import os.path
#
import re
#
import types
#
from contextlib import contextmanager
# noinspection PyUnresolvedReferences
import maya.mel as mel
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
from maya import OpenMayaUI
#
from PySide2 import QtCore, QtGui, QtWidgets

import functools
#
import shiboken2
#
_objectStore = {}


#
def pyToMelProc(pyObj, args=(), returnType=None, procName=None, useName=False, procPrefix='pyToMel_'):
    melParams = []
    pyParams = []
    melReturn = returnType if returnType else ''
    #
    for t, n in args:
        melParams.append('%s $%s' % (t, n))
        #
        if t == 'string':
            pyParams.append(r"""'"+$%s+"'""" % n)
        else:
            pyParams.append(r'"+$%s+"' % n)
    #
    objId = id(pyObj)
    #
    d = {}
    #
    if procName:
        d['procName'] = procName
    elif useName:
        d['procName'] = pyObj.__name__
    else:
        if isinstance(pyObj, types.LambdaType):
            procPrefix += '_lambda'
        elif isinstance(pyObj, (types.FunctionType, types.BuiltinFunctionType)):
            try:
                procPrefix += '_' + pyObj.__name__
            except (AttributeError, TypeError):
                pass
        elif isinstance(pyObj, types.MethodType):
            try:
                procPrefix += '_' + pyObj.im_class.__name__ + '_' + pyObj.__name__
            except (AttributeError, TypeError):
                pass
        d['procName'] = '%s%s' % (procPrefix, objId)
    #
    d['procName'] = d['procName'].replace('<', '_').replace('>', '_').replace('-', '_')
    d['melParams'] = ', '.join(melParams)
    d['pyParams'] = ', '.join(pyParams)
    d['melReturn'] = melReturn
    d['thisModule'] = __name__
    d['id'] = objId
    #
    contents = '''global proc %(melReturn)s %(procName)s(%(melParams)s){'''
    if melReturn:
        contents += 'return '
    contents += '''python("import %(thisModule)s;%(thisModule)s._objectStore[%(id)s](%(pyParams)s)");}'''
    mel.eval(contents % d)
    _objectStore[objId] = pyObj
    return d['procName']


def capitalize(s):
    return s[0].upper() + s[1:] if s else s


def get_name_prettify(s):
    return ' '.join([capitalize(x) for x in re.findall('[a-zA-Z][a-z]*[0-9]*', s)])


def toCamelCase(s):
    parts = s.split('_')
    return ''.join([parts[0]] + [capitalize(x) for x in parts[1:]])


def aeCallback(func):
    return pyToMelProc(func, [('string', 'nodeName')], procPrefix='AECallback')


def attrTextFieldGrp(*args, **kwargs):
    attribute = kwargs.pop('attribute', kwargs.pop('a', None))
    assert attribute is not None, "You Must Passed an Attribute"
    #
    changeCommand = kwargs.pop('changeCommand', kwargs.pop('cc', None))
    if changeCommand:
        # noinspection PyCallingNonCallable
        def cc(newVal):
            cmds.setAttr(attribute, newVal, type="string")
            changeCommand(newVal)
    else:
        def cc(newVal):
            cmds.setAttr(attribute, newVal, type="string")
    #
    if kwargs.pop('edit', kwargs.pop('e', False)):
        ctrl = args[0]
        cmds.textFieldGrp(
            ctrl,
            edit=True,
            text=cmds.getAttr(attribute),
            changeCommand=cc
        )
        cmds.scriptJob(
            parent=ctrl,
            replacePrevious=True,
            attributeChange=[attribute, lambda: cmds.textFieldGrp(ctrl, edit=True, text=cmds.getAttr(attribute))]
        )
    elif kwargs.pop('query', kwargs.pop('q', False)):
        pass
    else:
        labelText = kwargs.pop('label', None)
        if not labelText:
            labelText = mel.eval('interToUI(\"{}\")'.format(attribute.split('.')[-1]))
        #
        ctrl = None
        if len(args) > 0:
            ctrl = args[0]
            cmds.textFieldGrp(
                ctrl,
                label=labelText,
                text=cmds.getAttr(attribute),
                changeCommand=cc
            )
        else:
            ctrl = cmds.textFieldGrp(
                label=labelText,
                text=cmds.getAttr(attribute),
                changeCommand=cc
            )
        #
        cmds.scriptJob(
            parent=ctrl,
            attributeChange=[attribute, lambda: cmds.textFieldGrp(ctrl, edit=True, text=cmds.getAttr(attribute))]
        )
        return ctrl


def attrType(attr):
    t = cmds.getAttr(attr, type=True)
    if t == 'float3':
        node, at = attr.split('.', 1)
        if cmds.attributeQuery(at, node=node, usedAsColor=1):
            t = 'color'
    return t


def modeMethod(func):
    def wrapped(self, *args, **kwargs):
        modeFunc = getattr(self._mode, func.__name__)
        if self._record:
            self._actions.append((modeFunc, args, kwargs))
        else:
            modeFunc(*args, **kwargs)
    #
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    wrapped._orig = func
    return wrapped


def modeAttrMethod(func):
    def wrapped(self, attr, *args, **kwargs):
        assert isinstance(attr, basestring), "%r.%s: attr argument must be a string, got %s" % (self, func.__name__, type(attr).__name__)
        #
        modeFunc = getattr(self._mode, func.__name__)
        if self.convertToMayaStyle:
            attr = toCamelCase(attr)
        if self._record:
            self._actions.append((modeFunc, (attr,) + args, kwargs))
        else:
            modeFunc(attr, *args, **kwargs)
        #
        self._attributes.append(attr)
    #
    wrapped.__doc__ = func.__doc__
    wrapped.__name__ = func.__name__
    wrapped._orig = func
    return wrapped


def swatchLabel(nodeName):
    nodeType = cmds.nodeType(nodeName)
    classificationsList = cmds.getClassification(nodeType)
    for classification in classificationsList:
        allClassList = classification.split(':')
        for allClass in allClassList:
            classList = allClass.split('/')
            if 'swatch' == classList[0]:
                continue
            else:
                if classList:
                    if 'shader' != classList[-1]:
                        classList = filter(lambda x: x != 'shader', classList)
                    return "\n".join(map(lambda x: x.capitalize(), classList))
                else:
                    return "Sample"


def swatchDisplayNew(plugName):
    nodeAndAttrs = plugName.split(".")
    node = nodeAndAttrs[0]

    cmds.formLayout('swatchDisplayForm')
    cmds.text('swatchLabel', label=swatchLabel(node))
    cmds.swatchDisplayPort('swatchDisplay', wh=(64, 64), rs=64)
    #
    cmds.popupMenu('swatchPopup', button=3)
    cmds.menuItem('swatchSmall', label='Small')
    cmds.menuItem('swatchMedium', label='Medium')
    cmds.menuItem('swatchLarge', label='Large')
    #
    cmds.setParent(upLevel=True)
    gTextColumnWidthIndex = mel.eval("$tempVar=$gTextColumnWidthIndex;")
    cmds.formLayout(
        'swatchDisplayForm',
        edit=True,
        af=[
            ('swatchLabel', "top", 0),
            ('swatchLabel', "bottom", 0),
            ('swatchDisplay', "top", 0),
            ('swatchDisplay', "bottom", 0)
        ],
        aof=[
            ('swatchLabel', "right", -gTextColumnWidthIndex)
        ],
        an=[
            ('swatchLabel', "left"),
            ('swatchDisplay', "right")
        ],
        ac=[
            ('swatchDisplay', "left", 5, 'swatchLabel')
        ]
    )
    swatchDisplayReplace(plugName)


def swatchDisplayReplace(plugName):
    nodeAndAttrs = plugName.split(".")
    node = nodeAndAttrs[0]
    #
    cmds.swatchDisplayPort(
        'swatchDisplay',
        edit=True,
        shadingNode=node,
        annotation='Refresh Swatch',
        pressCommand=lambda *args: mel.eval("updateFileNodeSwatch " + node)
    )
    cmds.popupMenu('swatchPopup', edit=True, button=3)
    cmds.menuItem(
        'swatchSmall',
        edit=True,
        command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(64, 64), rs=64)
    )
    cmds.menuItem(
        'swatchMedium',
        edit=True,
        command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(96, 96), rs=96)
    )
    cmds.menuItem(
        'swatchLarge',
        edit=True,
        command=lambda *args: cmds.swatchDisplayPort('swatchDisplay', edit=True, wh=(128, 128), rs=128)
    )
    cmds.text('swatchLabel', edit=True, label=swatchLabel(node))


def file_button_fnc(*args):
    _atr_path = args[0]
    _file_path = cmds.getAttr(_atr_path)
    #
    _directory_path = os.path.dirname(_file_path)
    #
    __file_paths = cmds.fileDialog2(
        fileFilter='All Files (*.*)',
        cap='Load File',
        okc='Load',
        fm=4,
        dir=_directory_path
    ) or []
    if __file_paths:
        __file_path = __file_paths[0]
        cmds.setAttr(_atr_path, __file_path, type="string")


def file_new_fnc(atr_path):
    def edit_fnc_(new_file_path_):
        cmds.setAttr(atr_path, new_file_path_, type="string")
    #
    _ = atr_path.split('.')
    obj_name = _[0]
    port_name = _[-1]
    node_type_name = cmds.nodeType(obj_name)
    gui_name_0 = '{}_{}_entry'.format(node_type_name, port_name)
    gui_name_1 = '{}_{}_button'.format(node_type_name, port_name)
    label = get_name_prettify(port_name)
    #
    cmds.rowLayout(
        nc=2,
        cw2=(360, 30),
        cl2=('left', 'left'),
        adjustableColumn=1,
        columnAttach=[(1, 'left', -4), (2, 'left', 0)]
    )
    cmds.textFieldGrp(
        gui_name_0,
        label=label,
        changeCommand=edit_fnc_
    )
    cmds.textFieldGrp(
        gui_name_0,
        edit=True,
        text=cmds.getAttr(atr_path)
    )
    cmds.symbolButton(
        gui_name_1,
        image='folder-closed.png',
        command=lambda arg=None, x=atr_path: file_button_fnc(x)
    )
    cmds.scriptJob(
        parent=gui_name_0,
        replacePrevious=True,
        attributeChange=[
            atr_path,
            lambda: cmds.textFieldGrp(gui_name_0, edit=True, text=cmds.getAttr(atr_path))
        ]
    )


def file_replace_fnc(atr_path):
    _ = atr_path.split('.')
    obj_name = _[0]
    port_name = _[-1]
    node_type_name = cmds.nodeType(obj_name)
    gui_name_0 = '{}_{}_entry'.format(node_type_name, port_name)
    gui_name_1 = '{}_{}_button'.format(node_type_name, port_name)
    #
    cmds.textFieldGrp(
        gui_name_0,
        edit=True,
        text=cmds.getAttr(atr_path)
    )
    cmds.symbolButton(
        gui_name_1,
        edit=True,
        image='folder-closed.png',
        command=lambda arg=None, x=atr_path: file_button_fnc(x)
    )
    cmds.scriptJob(
        parent=gui_name_0,
        replacePrevious=True,
        attributeChange=[
            atr_path,
            lambda: cmds.textFieldGrp(gui_name_0, edit=True, text=cmds.getAttr(atr_path))
        ]
    )


class baseMode(object):
    def __init__(self, template):
        self.template = template
    @property
    def nodeName(self):
        return self.template.nodeName
    @property
    def attr(self):
        return self.template.attr
    #
    def nodeType(self):
        self.template.nodeType()
    #
    def nodeAttr(self, attr):
        return self.template.nodeAttr(attr)
    #
    def nodeAttrExists(self, attr):
        return self.template.nodeAttrExists(attr)


class rootMode(baseMode):
    def __init__(self, template):
        super(rootMode, self).__init__(template)
        #
        self._atr_path = None
        #
        self._nodeName = None
        self._type = self.template.nodeType()
    #
    def _updateCallback(self, nodeAttr):
        self.template._doUpdate(nodeAttr.split('.')[0])
    #
    def preSetup(self):
        self.addCustom('message', self._updateCallback, self._updateCallback)
    #
    def postSetup(self):
        pass
    #
    def update(self):
        pass
    #
    def addTemplate(self, attr, template):
        if template._isRootMode():
            template._doSetup(self.nodeAttr(attr))
        else:
            self.addChildTemplate(attr, template)
    @staticmethod
    def addChildTemplate(attr, template):
        template._setToChildMode()
        template._record = True
        template.setup()
        for attr in template._attributes:
            try:
                cmds.editorTemplate(suppress=attr)
            except RuntimeError:
                pass
        cmds.editorTemplate(
            aeCallback(template._doSetup),
            aeCallback(template._doUpdate),
            attr,
            callCustom=True
        )
    @staticmethod
    def _set_control_add_(attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False):
        if not label:
            label = get_name_prettify(attr)
        #
        args = [attr]
        kwargs = {}
        #
        if dynamic:
            kwargs['addDynamicControl'] = True
        else:
            kwargs['addControl'] = True
        #
        if changeCommand:
            if hasattr(changeCommand, '__call__'):
                changeCommand = aeCallback(changeCommand)
            #
            args.append(changeCommand)
        if label:
            kwargs['label'] = label
        if annotation:
            kwargs['annotation'] = annotation
        #
        cmds.editorTemplate(*args, **kwargs)
    @classmethod
    def _set_enumerate_control_add_(cls, port_path, enumerate_option):
        def new_fnc_(atr_path_):
            _ = atr_path_.split('.')
            _obj_name = _[0]
            _port_name = _[-1]
            _node_type_name = cmds.nodeType(_obj_name)
            _gui_name = '{}__{}'.format(_node_type_name, _port_name)
            #
            _enumerate_items = [
                (_seq, _i) for _seq, _i in enumerate(enumerate_option.split('|'))
            ]
            cmds.setUITemplate(
                'attributeEditorPresetsTemplate',
                pushTemplate=True
            )
            cmds.attrEnumOptionMenuGrp(
                _gui_name,
                attribute=atr_path_,
                label=label,
                enumeratedItem=_enumerate_items
            )
            cmds.setUITemplate(popTemplate=True)

        def replace_fnc_(atr_path_):
            _ = atr_path_.split('.')
            _obj_name = _[0]
            _port_name = _[-1]
            _node_type_name = cmds.nodeType(_obj_name)
            _gui_name = '{}__{}'.format(_node_type_name, _port_name)
            #
            cmds.attrEnumOptionMenuGrp(
                _gui_name,
                edit=True,
                attribute=atr_path_
            )
        #
        label = get_name_prettify(port_path)
        #
        cls.addCustom(port_path, new_fnc_, replace_fnc_)
    @classmethod
    def _set_file_name_control_add__(cls, port_path):
        def new_fnc_(atr_path_):
            def edit_fnc_(new_file_path_):
                cmds.setAttr(atr_path_, new_file_path_, type="string")
            #
            def button_fnc_(*args):
                _file_path = cmds.getAttr(atr_path_)
                #
                _directory_path = os.path.dirname(_file_path)
                #
                __file_paths = cmds.fileDialog2(
                    fileFilter='All Files (*.*)',
                    cap='Load File',
                    okc='Load',
                    fm=4,
                    dir=_directory_path
                ) or []
                if __file_paths:
                    __file_path = __file_paths[0]
                    edit_fnc_(__file_path)
                    cmds.textField(
                        _gui_name,
                        edit=True,
                        text=__file_path
                    )
            #
            _ = atr_path_.split('.')
            _obj_name = _[0]
            _port_name = _[-1]
            _node_type_name = cmds.nodeType(_obj_name)
            _gui_name = '{}__{}'.format(_node_type_name, _port_name)
            #
            cmds.rowLayout(
                numberOfColumns=3,
                columnWidth3=(145, 400, 30),
                columnAlign3=('right', 'center', 'left'),
                adjustableColumn=2,
                columnAttach=[(1, 'right', 0), (2, 'both', 0), (3, 'left', 0)],
            )
            cmds.text(label=label)
            cmds.textField(
                _gui_name,
                # label=label,
                changeCommand=edit_fnc_
            )
            cmds.textField(
                _gui_name,
                edit=True,
                text=cmds.getAttr(atr_path_)
            )
            cmds.symbolButton(
                image='folder-closed.png',
                command=button_fnc_
            )
            cmds.scriptJob(
                parent=_gui_name,
                replacePrevious=True,
                attributeChange=[
                    atr_path_,
                    lambda: cmds.textField(_gui_name, edit=True, text=cmds.getAttr(atr_path_))
                ]
            )
        #
        def replace_fnc_(atr_path_):
            _ = atr_path_.split('.')
            _obj_name = _[0]
            _port_name = _[-1]
            _node_type_name = cmds.nodeType(_obj_name)
            _gui_name = '{}__{}'.format(_node_type_name, _port_name)
            #
            cmds.textField(
                _gui_name,
                edit=True,
                text=cmds.getAttr(atr_path_)
            )
            #
            cmds.scriptJob(
                parent=_gui_name,
                replacePrevious=True,
                attributeChange=[
                    atr_path_,
                    lambda: cmds.textField(_gui_name, edit=True, text=cmds.getAttr(atr_path_))
                ]
            )
        #
        label = get_name_prettify(port_path)
        #
        cls.addCustom(port_path, new_fnc_, replace_fnc_)
    @classmethod
    def _set_file_name_control_add_(cls, port_path):
        cls.addCustom(
            port_path, file_new_fnc, file_replace_fnc
        )
    @classmethod
    def addControl(cls, attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False, useAsFileName=False, enumerateOption=None):
        if enumerateOption is not None:
            cls._set_enumerate_control_add_(
                attr, enumerateOption
            )
        elif useAsFileName is True:
            cls._set_file_name_control_add_(
                attr
            )
        else:
            cls._set_control_add_(
                attr,
                label,
                changeCommand,
                annotation,
                preventOverride,
                dynamic
            )
    @staticmethod
    def suppress(attr):
        cmds.editorTemplate(suppress=attr)
    @staticmethod
    def addCustom(attr, newFunc, replaceFunc):
        if hasattr(newFunc, '__call__'):
            newFunc = aeCallback(newFunc)
        if hasattr(replaceFunc, '__call__'):
            replaceFunc = aeCallback(replaceFunc)
        args = (newFunc, replaceFunc, attr)
        cmds.editorTemplate(callCustom=1, *args)
    @staticmethod
    def addSeparator():
        cmds.editorTemplate(addSeparator=True)
    @staticmethod
    def dimControl(nodeName, control, state):
        cmds.editorTemplate(dimControl=(nodeName, control, state))
    @staticmethod
    def beginLayout(name, collapse=True):
        cmds.editorTemplate(beginLayout=name, collapse=collapse)
    @staticmethod
    def endLayout():
        cmds.editorTemplate(endLayout=True)
    @staticmethod
    def beginScrollLayout():
        cmds.editorTemplate(beginScrollLayout=True)
    @staticmethod
    def endScrollLayout():
        cmds.editorTemplate(endScrollLayout=True)
    @staticmethod
    def beginNoOptimize():
        cmds.editorTemplate(beginNoOptimize=True)
    @staticmethod
    def endNoOptimize():
        cmds.editorTemplate(endNoOptimize=True)
    @staticmethod
    def interruptOptimize():
        cmds.editorTemplate(interruptOptimize=True)
    @staticmethod
    def addComponents():
        cmds.editorTemplate(addComponents=True)
    @staticmethod
    def addExtraControls(label=None):
        kwargs = {}
        if label:
            kwargs['extraControlsLabel'] = label
        cmds.editorTemplate(addExtraControls=True, **kwargs)


class AttrControlGrp(object):
    uiTypeDic = {
        'float': cmds.attrFieldSliderGrp,
        'float2': cmds.attrFieldGrp,
        'float3': cmds.attrFieldGrp,
        'color': cmds.attrColorSliderGrp,
        'bool': cmds.attrControlGrp,
        'long': cmds.attrFieldSliderGrp,
        'byte': cmds.attrFieldSliderGrp,
        'long2': cmds.attrFieldGrp,
        'long3': cmds.attrFieldGrp,
        'short': cmds.attrFieldSliderGrp,
        'short2': cmds.attrFieldGrp,
        'short3': cmds.attrFieldGrp,
        'enum': cmds.attrEnumOptionMenuGrp,
        'double': cmds.attrFieldSliderGrp,
        'double2': cmds.attrFieldGrp,
        'double3': cmds.attrFieldGrp,
        'string': attrTextFieldGrp,
        'message': cmds.attrNavigationControlGrp
    }
    def __init__(self, attribute, *args, **kwargs):
        self.attribute = attribute
        self.type = kwargs.pop('type', kwargs.pop('typ', None))
        #
        if not self.type:
            self.type = attrType(self.attribute)

        if self.type in ['color', 'enum', 'message']:
            self.callback = kwargs.pop('changeCommand', None)
        else:
            self.callback = None
        kwargs['attribute'] = self.attribute
        if self.type not in self.uiTypeDic:
            return
        cmd = self.uiTypeDic[self.type]
        try:
            self.control = cmd(*args, **kwargs)
        except RuntimeError:
            print "Error creating %s:" % cmd.__name__
            raise
        if self.callback:
            cmds.scriptJob(
                attributeChange=[self.attribute, self.callback],
                replacePrevious=True,
                parent=self.control
            )
    #
    def edit(self, **kwargs):
        kwargs['edit'] = True
        if self.type not in self.uiTypeDic:
            return
        self.uiTypeDic[self.type](self.control, **kwargs)
    #
    def setAttribute(self, attribute):
        self.attribute = attribute
        if self.type not in self.uiTypeDic:
            return
        self.uiTypeDic[self.type](self.control, edit=True, attribute=self.attribute)
        if self.callback:
            cmds.scriptJob(
                attributeChange=[self.attribute, self.callback],
                replacePrevious=True,
                parent=self.control
            )


class childMode(baseMode):
    def __init__(self, template):
        super(childMode, self).__init__(template)
        self._controls = []
        self._layoutStack = []
    #
    def preSetup(self):
        cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        self._layoutStack = [cmds.setParent(query=True)]
    @staticmethod
    def postSetup():
        cmds.setUITemplate(popTemplate=True)
    #
    def update(self):
        cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        try:
            for attr, updateFunc, parent in self._controls:
                cmds.setParent(parent)
                updateFunc(self.nodeAttr(attr))
        except:
            print("Template %r Failed to Update Attribute '%s'" % (self.template, self.attr))
            raise
        finally:
            cmds.setUITemplate(popTemplate=True)
    #
    def addTemplate(self, attr, template):
        self.addChildTemplate(attr, template)
    #
    def addChildTemplate(self, attr, template):
        template._setToChildMode()
        template._record = True
        template.setup()
        for attr in template._attributes:
            try:
                cmds.editorTemplate(suppress=attr)
            except RuntimeError:
                pass
        self.addCustom(attr, template._doSetup, template._doUpdate)
    #
    def addControl(self, attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False, enumeratedItem=None):
        if not label:
            label = get_name_prettify(attr)
        #
        kwargs = {'label': label, 'attribute': self.nodeAttr(attr)}
        if annotation:
            kwargs['annotation'] = annotation
        if changeCommand:
            kwargs['changeCommand'] = changeCommand
        if enumeratedItem:
            kwargs['enumeratedItem'] = enumeratedItem
        #
        parent = self._layoutStack[-1]
        cmds.setParent(parent)
        control = AttrControlGrp(**kwargs)
        #
        self._controls.append((attr, control.setAttribute, parent))
    #
    def addCustom(self, attr, createFunc, updateFunc):
        parent = self._layoutStack[-1]
        cmds.setParent(parent)
        col = cmds.columnLayout(adj=True)
        #
        createFunc(self.nodeAttr(attr))
        cmds.setParent(parent)
        self._controls.append((attr, updateFunc, col))
    @staticmethod
    def addSeparator():
        cmds.separator()
    #
    def beginLayout(self, label, **kwargs):
        kwargs['label'] = label
        cmds.setParent(self._layoutStack[-1])
        cmds.frameLayout(**kwargs)
        self._layoutStack.append(cmds.columnLayout(adjustableColumn=True))
    #
    def endLayout(self):
        self._layoutStack.pop()
        cmds.setParent(self._layoutStack[-1])
    #
    def beginNoOptimize(self):
        pass
    #
    def endNoOptimize(self):
        pass
    #
    def beginScrollLayout(self):
        pass
    #
    def endScrollLayout(self):
        pass
    #
    def addExtraControls(self):
        pass


class AbsTemplateBase(object):
    def __init__(self, nodeType):
        self._type = nodeType
        self._nodeName = None
        self._atr_path = None
    #
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._type)
    @property
    def nodeName(self):
        return self._nodeName
    @property
    def attr(self):
        return self._atr_path
    #
    def nodeType(self):
        if self._type is None:
            self._type = cmds.objectType(self.nodeName)
        return self._type
    #
    def nodeAttr(self, attr=None):
        if attr is None:
            attr = self.attr
        return self.nodeName + '.' + attr
    #
    def nodeAttrExists(self, attr):
        return cmds.addAttr(self.nodeAttr(attr), q=1, ex=1)


class AbsNodeTemplate(AbsTemplateBase):
    convertToMayaStyle = False
    def __init__(self, nodeType):
        super(AbsNodeTemplate, self).__init__(nodeType)
        #
        self._rootMode = rootMode(self)
        self._childMode = childMode(self)
        #
        self._mode = self._rootMode
        self._actions = []
        self._attributes = []
        self._record = False
    #
    def _setToRootMode(self):
        self._mode = self._rootMode
    #
    def _isRootMode(self):
        return self._mode == self._rootMode
    #
    def _setToChildMode(self):
        self._mode = self._childMode
    #
    def _isChildMode(self):
        return self._mode == self._childMode
    #
    def _setActiveNodeAttr(self, nodeName):
        parts = nodeName.split('.', 1)
        self._nodeName = parts[0]
        if len(parts) > 1:
            self._atr_path = parts[1]
    #
    def _doSetup(self, nodeAttr):
        self._setActiveNodeAttr(nodeAttr)
        self._mode.preSetup()
        if self._record:
            for func, args, kwargs in self._actions:
                func(*args, **kwargs)
        else:
            self.setup()
        self._mode.postSetup()
    #
    def _doUpdate(self, nodeAttr):
        self._setActiveNodeAttr(nodeAttr)
        self._mode.update()
    @modeMethod
    def update(self):
        pass
    @modeAttrMethod
    def addTemplate(self, attr, template):
        pass
    @modeAttrMethod
    def addChildTemplate(self, attr, template):
        pass
    @modeAttrMethod
    def addControl(self, attr, label=None, changeCommand=None, annotation=None, preventOverride=False, dynamic=False, useAsFileName=False, enumerateOption=None):
        pass
    @modeMethod
    def suppress(self, attr):
        pass
    @modeMethod
    def addSeparator(self):
        pass
    @modeAttrMethod
    def addCustom(self, attr, createFunc, updateFunc):
        pass
    @modeMethod
    def beginLayout(self, label, **kwargs):
        pass
    @modeMethod
    def endLayout(self):
        pass
    @modeMethod
    def beginNoOptimize(self):
        pass
    @modeMethod
    def endNoOptimize(self):
        pass
    @modeMethod
    def beginScrollLayout(self):
        pass
    @modeMethod
    def endScrollLayout(self):
        pass
    @modeMethod
    def addExtraControls(self):
        pass
    @contextmanager
    def scroll_layout(self):
        # noinspection PyArgumentList
        self.beginScrollLayout()
        yield
        # noinspection PyArgumentList
        self.endScrollLayout()
    @contextmanager
    def layout(self, label, **kwargs):
        # noinspection PyArgumentList
        self.beginLayout(label, **kwargs)
        yield
        # noinspection PyArgumentList
        self.endLayout()
    #
    def addSwatch(self):
        self.addCustom("message", swatchDisplayNew, swatchDisplayReplace)
    # for override
    def setup(self):
        pass
    @classmethod
    def get_qt_object(cls, maya_ui_name, qt_type=QtWidgets.QWidget):
        ptr = OpenMayaUI.MQtUtil.findControl(maya_ui_name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.findLayout(maya_ui_name)
            if ptr is None:
                ptr = OpenMayaUI.MQtUtil.findMenuItem(maya_ui_name)
        #
        if ptr is not None:
            obj = shiboken2.wrapInstance(long(ptr), qt_type)
            return obj
    @classmethod
    def get_current_widget(cls):
        currentWidgetName = cmds.setParent(query=True)
        return cls.get_qt_object(currentWidgetName)

    def set_port_create(self, atr_path):
        pass

    def set_port_replace(self, atr_path):
        pass


class AeMtd(object):
    CACHE = {}
    @classmethod
    def set_ae_register(cls, node_type, class_path):
        cls.CACHE[node_type] = class_path
        #
        proc_name = 'AE%sTemplate' % node_type
        script = '''global proc %s(string $node_name){python("from lxmaya import ma_ae; ma_ae.AeMtd.set_load('%s','" + $node_name + "')");}''' % (
            proc_name, node_type
        )
        mel.eval(script)
    @classmethod
    def set_load(cls, node_type, node_name):
        try:
            if node_type in cls.CACHE:
                class_path = cls.CACHE[node_type]
                modules = class_path.split('.')
                class_name = modules[-1]
                module_name = '.'.join(modules[:-1])
                if module_name:
                    import importlib
                    #
                    import imp
                    #
                    module = importlib.import_module(module_name)
                    imp.reload(module)
                    #
                    class_obj = module.__dict__[class_name]
                    class_obj(node_name)
        except Exception as e:
            print 'Error loading AE Template for node type {}'.format(node_type)
            import traceback
            traceback.print_exc()


class AeMtd2(object):
    @classmethod
    def aeProc(cls, modName, objName, procName):
        contents = '''global proc %(procName)s( string $nodeName ){python("import %(__name__)s;%(__name__)s.aeLoader('%(modName)s','%(objName)s','" + $nodeName + "')");}'''
        d = locals().copy()
        d['__name__'] = __name__
        mel.eval(contents % d)
    @classmethod
    def aeLoader(cls, modName, objName, nodeName):
        mod = __import__(modName, globals(), locals(), [objName], -1)
        try:
            f = getattr(mod, objName)
            if inspect.isfunction(f):
                f(nodeName)
            elif inspect.isclass(f):
                inst = f(cmds.nodeType(nodeName))
                inst._doSetup(nodeName)
            else:
                print "AE Object %s has Invalid Type %s" % (f, type(f))
        except Exception:
            print "Failed to Load Python Attribute Editor Template '%s.%s'" % (modName, objName)
            import traceback
            traceback.print_exc()
