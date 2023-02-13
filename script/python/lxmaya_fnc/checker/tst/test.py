# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

from lxmaya_fnc import ma_fnc_abstract

import lxmaya.dcc.dcc_objects as ma_dcc_objects


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
        # override label configure
        self.loader.label = u'My Test'
        # 使用yaml的规则配置
        self.loader.descriptions = u"""
        # key = description
        - My-test 00 is Error:
            # notes
            notes:
                - 测试
            # repair
            repair:
                # repair description
                description: Repair 01
            # ignore
            ignore:
                # # ignore-value
                value: True
                # ignore-enable
                enable: True
        - My-test 01 is Error
        - My-test 02 is Error
        - My-test 03 is Error
        - My-test 04 is Error
        """
        # 使用python的规则配置
        # self.loader.descriptions = [
        #     # dict / str / unicode
        #     {
        #         # key
        #         'My-test 01 is Error':
        #             {
        #                 # notes
        #                 'notes': [
        #                     u'测试 01'
        #                 ],
        #                 # repair
        #                 'repair': {
        #                     'description': 'Repair 01'
        #                 },
        #                 # ignore
        #                 'ignore': {
        #                     'enable': True
        #                 }
        #             }
        #     },
        #     'My-test 02 is Error'
        # ]
    # 错误的节点 参考
    def _check_method_0(self, *args):
        # obj是DCC节点的抽象实例
        obj, check_index = args[:2]
        # 以下是常用的参数获取，可以调DCC的API自行处理
        # print obj.type
        # print obj.path
        # print obj.name
        # print obj
        # 使用现有的API
        # is_error = not obj.get_is_exists()
        # 使用DCC的API
        is_error = not cmds.objExists(obj.path)
        # error object
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # 修复 错误的节点
    def _repair_method_0(self, obj):
        # delete
        # print obj.path
        # print obj.name
        # print obj.type
        # print obj
        # use exists method
        # obj.set_delete()
        # use dcc api
        if cmds.objExists(obj.path):
            cmds.delete(obj.path)
    # 错误的节点 部件 参考： /mod/mesh_manifold_custom
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_comps = []
        comp_names = obj.get_edge_non_manifold_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs
    # 错误的节点 文件连接 参考： /srf/texture_custom
    def _check_method_2(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        #
        os_files = obj.get_file_plf_objs()
        for os_file in os_files:
            if not os_file.ext == '.tx':
                # 可以直接调用OsFile的类
                # ma_dcc_objects.OsFile(file_path)
                error_obj_files.append(os_file)
        #
        self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs
    # 错误的节点 节点连接 参考： /ani/control_custom
    def _check_method_3(self, *args):
        obj, check_index = args[:2]
        #
        error_node_paths = obj.get_source_node_paths(include_types=['animCurve'])
        error_obj_sources = []
        for node_path in error_node_paths:
            error_node = ma_dcc_objects.Node(node_path)
            error_obj_sources.append(error_node)
        #
        is_error = self.set_error_obj_sources_update(obj, check_index, error_obj_sources)
        #
        outputs = []
        return outputs
    # 错误的信息
    def _check_method_4(self, *args):
        # obj是DCC节点的抽象实例
        check_args, check_index = args[:2]
        # 以下是常用的参数获取，可以调DCC的API自行处理
        is_error = True
        string = 'test'
        # error object
        self.set_error_obj_update(is_error, string, check_index)
        #
        outputs = []
        return outputs

    def set_check_run(self):
        self.set_restore()
        # dcc object paths
        paths = []
        # obj 是DCC节点的抽象实例，直接使用定义好的就行
        objs = [ma_dcc_objects.Node(i) for i in paths]
        #
        self._set_objs_check_(objs, include_indices=[0])

        # dcc object paths
        paths = ['test']
        # obj 是DCC节点的抽象实例，直接使用定义好的就行
        self._set_objs_check_(paths, include_indices=[4])
