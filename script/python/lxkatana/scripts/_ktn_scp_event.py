# coding:utf-8
import threading

import six

import lxbasic.core as bsc_core

import lxkatana.core as ktn_core


class ScpEventForArnold(object):
    DIRECTORY_KEY = 'user.extra.texture_directory'
    DIRECTORY_VALUE = '/texture_directory'

    BUILD_BUTTON_KEY = 'user.texture_builder'

    BUILD_DATA = [
        (BUILD_BUTTON_KEY, dict(widget='button', value='import lxkatana.scripts as ktn_scripts; ktn_scripts.ScpTextureBuilder(node).do_create()')),
    ]

    class NodeTypes(object):
        Material = 'NetworkMaterialCreate'
        NodeGroup = 'ShadingGroup'
        Node = 'ArnoldShadingNode'

    # noinspection PyUnusedLocal
    @classmethod
    def on_material_create(cls, *args, **kwargs):
        if kwargs['nodeType'] == cls.NodeTypes.Material:
            node_opt = ktn_core.NGObjOpt(kwargs['node'])
            cls._create_material(node_opt)

    @classmethod
    def _create_material(cls, node_opt):
        """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpEventForArnold._create_material(
    ktn_core.NGObjOpt(
        NodegraphAPI.GetNode('NetworkMaterialCreate')
    )
)
        """

        def pre_fnc_():
            _flag = False
            _p_ns = [
                (cls.DIRECTORY_KEY, dict(widget='file', value=cls.DIRECTORY_VALUE)),
            ] + cls.BUILD_DATA
            for _i_p_n, _i_p_r in _p_ns:
                if node_opt.get_port(_i_p_n) is None:
                    _flag = True
                    ktn_core.NGObjOpt(node_opt.ktn_obj).create_port_by_data(
                        _i_p_n, _i_p_r, expand_all_group=True
                    )
            return _flag

        def create_fnc():
            _key = cls.DIRECTORY_KEY
            # ignore when expression is enable
            if node_opt.get_is_expression(_key) is True:
                return False
            # ignore when value is changed
            if node_opt.get(_key) != cls.DIRECTORY_VALUE:
                return False
            # ignore parent is non-exists
            _parent_opt = node_opt.get_parent_opt()
            if not _parent_opt:
                return False
            # ignore parent has not directory
            if not _parent_opt.get_port(_key):
                return False
            #
            node_opt.set_expression(_key, 'getParent().{}'.format(_key))
            return True

        if pre_fnc_() is True:
            create_fnc()

    # noinspection PyUnusedLocal
    @classmethod
    def on_image_create(cls, *args, **kwargs):
        if kwargs['nodeType'] == cls.NodeTypes.Node:
            node_opt = ktn_core.NGObjOpt(kwargs['node'])
            if node_opt.get('nodeType') in ['image']:
                cls._create_or_cpy_image(node_opt)

    @classmethod
    def _create_or_cpy_image(cls, node_opt):
        """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpEventForArnold._create_or_cpy_image(
    ktn_core.NGObjOpt(
        NodegraphAPI.GetNode('image')
    )
)
        """

        def pre_fnc_():
            _p_ns = [
                (cls.DIRECTORY_KEY, dict(widget='file', value=cls.DIRECTORY_VALUE)),
            ]
            _flag = False
            for _i_p_n, _i_p_r in _p_ns:
                if node_opt.get_port(_i_p_n) is None:
                    _flag = True
                    ktn_core.NGObjOpt(node_opt.ktn_obj).create_port_by_data(
                        _i_p_n, _i_p_r, expand_all_group=True
                    )
            return _flag

        def create_fnc_():
            _key = cls.DIRECTORY_KEY

            _ancestors = node_opt.get_ancestors()
            # ignore when ancestors is not found
            if _ancestors:
                _ancestors = node_opt.get_ancestors()
                if _ancestors:
                    for i_seq, _i in enumerate(_ancestors):
                        _i_opt = ktn_core.NGObjOpt(_i)
                        if _i_opt.get_type_name() == cls.NodeTypes.Material:
                            # ignore when attribute is not found at material
                            if not _i_opt.get(_key):
                                return False

                            node_opt.set_expression(
                                _key, '{}.{}'.format('.'.join(['getParent()']*(i_seq+1)), _key)
                            )
                            return True
            return False

        def post_create_fnc_():
            _key = cls.DIRECTORY_KEY
            #
            if not node_opt.get(cls.DIRECTORY_KEY):
                return False
            #
            if not node_opt.get('parameters.filename.value'):
                node_opt.set(
                    'parameters.filename.enable', 1
                )
                node_opt.set_expression(
                    'parameters.filename.value', '{}+\'/tx\'+\'/texture_name.<udim>.tx\''.format(_key)
                )
                #
                node_opt.set(
                    'parameters.ignore_missing_textures.enable', 1
                )
                node_opt.set(
                    'parameters.ignore_missing_textures.value', 1
                )
            #
            node_opt.set_attributes(
                dict(
                    ns_colorr=0.3199999928474426,
                    ns_colorg=0.07999999821186066,
                    ns_colorb=0.3199999928474426
                )
            )

        def copy_fnc_():
            _key = cls.DIRECTORY_KEY
            # ignore when expression is disable
            if node_opt.get_is_expression(_key) is True:
                # check expression is valid
                if not node_opt.get(_key):
                    _ancestors = node_opt.get_ancestors()
                    # ignore when ancestors is not found
                    if _ancestors:
                        _ancestors = node_opt.get_ancestors()
                        if _ancestors:
                            for i_seq, _i in enumerate(_ancestors):
                                _i_opt = ktn_core.NGObjOpt(_i)
                                if _i_opt.get_type_name() == cls.NodeTypes.Material:
                                    # ignore when attribute is not found at material
                                    if not _i_opt.get(_key):
                                        return False

                                    node_opt.set_expression(
                                        _key, '{}.{}'.format('.'.join(['getParent()']*(i_seq+1)), _key)
                                    )
                                    return True
            return False

        if pre_fnc_() is True:
            if create_fnc_() is True:
                timer = threading.Timer(1, post_create_fnc_)
                timer.start()
        else:
            copy_fnc_()

    # noinspection PyUnusedLocal
    @classmethod
    def on_node_group_create(cls, *args, **kwargs):
        if kwargs['nodeType'] == cls.NodeTypes.NodeGroup:
            node_opt = ktn_core.NGObjOpt(kwargs['node'])
            cls._create_node_group(node_opt)

    @classmethod
    def _create_node_group(cls, node_opt):
        """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpEventForArnold._create_node_group(
    ktn_core.NGObjOpt(
        NodegraphAPI.GetNode('ShadingGroup')
    )
)
        """
        def pre_fnc_():
            _flag = False
            for _i_p_n, _i_p_r in cls.BUILD_DATA:
                if node_opt.get_port(_i_p_n) is None:
                    _flag = True
                    ktn_core.NGObjOpt(node_opt.ktn_obj).create_port_by_data(
                        _i_p_n, _i_p_r, expand_all_group=True
                    )
            return _flag

        if pre_fnc_() is True:
            pass

    # noinspection PyUnusedLocal
    @classmethod
    def on_shader_create(cls, *args, **kwargs):
        if kwargs['nodeType'] == cls.NodeTypes.Node:
            node_opt = ktn_core.NGObjOpt(kwargs['node'])
            if node_opt.get('nodeType') in ['standard_surface']:
                cls._create_shader(node_opt)

    @classmethod
    def _create_shader(cls, node_opt):
        """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpEventForArnold._create_shader(
    ktn_core.NGObjOpt(
        NodegraphAPI.GetNode('ShadingGroup')
    )
)
        """
        def pre_fnc_():
            _flag = False
            for _i_p_n, _i_p_r in cls.BUILD_DATA:
                if node_opt.get_port(_i_p_n) is None:
                    _flag = True
                    ktn_core.NGObjOpt(node_opt.ktn_obj).create_port_by_data(
                        _i_p_n, _i_p_r, expand_all_group=True
                    )
            return _flag

        if pre_fnc_() is True:
            pass


class ScpTextureBuilder(object):
    KEY = 'texture build'

    def __init__(self, ktn_obj):
        if isinstance(ktn_obj, six.string_types):
            self._ktn_obj = ktn_core.NodegraphAPI.GetNode(
                ktn_obj
            )
        else:
            self._ktn_obj = ktn_obj

        self._obj_opt = ktn_core.NGObjOpt(self._ktn_obj)

    def do_create(self):
        if self._obj_opt.get_is(['NetworkMaterialCreate', 'ShadingGroup', 'ArnoldShadingNode']):
            import lxgui.core as gui_core

            if self._obj_opt.get_is('ShadingGroup'):
                if self._obj_opt.has_children():
                    gui_core.GuiDialog.create(
                        self.KEY,
                        content=(
                            'this "ShadingGroup" is not valid, create a new "ShadingGroup" and retry'
                        ),
                        status=gui_core.GuiDialog.ValidationStatus.Warning,
                        #
                        cancel_label='Close',
                        #
                        yes_visible=False, no_visible=False, cancel_visible=True,
                    )
                    return False

            file_path = None

            import lxgui.qt.core as gui_qt_core
            text = gui_qt_core.GuiQtUtil.get_text_from_clipboard()
            if text:
                if bsc_core.StgFileMtd.get_is_exists(text) is True:
                    if bsc_core.StgFileMtd.get_ext(text) in {'.tx', '.png', '.jpg', '.tiff', '.exr'}:
                        file_path = text
            
            if file_path is None:
                file_path = gui_core.GuiFileDialog.open_file()

            if file_path:
                import lxsession.commands as ssn_commands

                args = ssn_commands.get_hook_args('*/gen-texture-builder')
                if args:
                    session, execute_fnc = args
                    execute_fnc()
                    prx_window = session.get_prx_window()
                    prx_window.setup(
                        self._obj_opt.get_path(),
                        file_path
                    )

    def do_paste(self):
        import lxgui.core as gui_core

        import lxgui.qt.core as gui_qt_core

        file_path = None

        text = gui_qt_core.GuiQtUtil.get_text_from_clipboard()

        if text:
            if bsc_core.StgFileMtd.get_is_exists(text) is True:
                if bsc_core.StgFileMtd.get_ext(text) in {'.tx', '.png', '.jpg', '.tiff', '.exr'}:
                    file_path = text

        if file_path is not None:
            if self._obj_opt.get_is({'NetworkMaterialCreate'}):
                w = gui_core.GuiDialogAsBubbleChoose.create(
                    ['material', 'shader', 'group', 'image'],
                    'create texture in material group, choose a scheme to continue'
                )
                scheme = w.get_result()

                if scheme is not None:
                    import lxkatana.scripts as ktn_scripts
                    if scheme == 'image':
                        ktn_scripts.ScpTextureBuildForPaste.create_one(self._obj_opt, file_path)
                    else:
                        ktn_scripts.ScpTextureBuildForPaste(
                            self._obj_opt, scheme, file_path
                        ).accept()
            elif self._obj_opt.get_is({'ShadingGroup'}):
                w = gui_core.GuiDialogAsBubbleChoose.create(
                    ['group', 'image'],
                    'create texture in material group, choose a scheme to continue'
                )
                scheme = w.get_result()

                if scheme is not None:
                    import lxkatana.scripts as ktn_scripts
                    if scheme == 'image':
                        ktn_scripts.ScpTextureBuildForPaste.create_one(self._obj_opt, file_path)
                    else:
                        ktn_scripts.ScpTextureBuildForPaste(
                            self._obj_opt, scheme, file_path
                        ).accept()
