# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxmaya_fnc import ma_fnc_abstract


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
        # override label configure
        self.loader.label = u'Shot-frame-range'
        # 使用yaml的规则配置
        self.loader.descriptions = u"""
        # key = description
        - the start and end of timeline will be update to shotgun :
            # notes
            notes:
                - the start and end of timeline are different with shotgun "cut in", "cut out"
            ignore:
                # ignore-enable
                value: True
                enable: True
        """
    # 错误的节点 参考
    def _check_method_0(self, *args):
        outputs = []
        return outputs

    def set_check_run(self):
        self.set_restore()
        # dcc object paths
        paths = ['frame_range']
        #
        self._set_objs_check_(paths, include_indices=[0])
