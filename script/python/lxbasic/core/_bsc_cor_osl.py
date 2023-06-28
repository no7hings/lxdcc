# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_process, _bsc_cor_storage


class OslFileMtd(object):
    OBJ_PATTERN = 'shader "{name}"\n'
    PORT_PATTERN = '    "{name}" "{type}"\n'
    DEFAULT_VALUE_PATTERN = '		Default value: {value}\n'
    METADATA_PATTERN = '		metadata: {type} {name} = {value}\n'
    @classmethod
    def set_compile(cls, file_path):
        file_opt = _bsc_cor_storage.StgFileOpt(file_path)
        compile_file_path = '{}.oso'.format(file_opt.path_base)
        #
        cmd_args = [
            Bin.get_oslc(),
            '-o "{}" "{}"'.format(compile_file_path, file_opt.path),
        ]
        _bsc_cor_process.SubProcessMtd.execute_with_result(' '.join(cmd_args))
    @classmethod
    def get_info(cls, file_path):
        dic = collections.OrderedDict()
        #
        file_opt = _bsc_cor_storage.StgFileOpt(file_path)
        compile_file_path = '{}.oso'.format(file_opt.path_base)
        #
        cmd_args = [
            Bin.get_oslinfo(),
            '-v "{}"'.format(compile_file_path),
        ]
        p = _bsc_cor_process.SubProcessMtd.set_run(' '.join(cmd_args))
        _ = p.stdout.readlines()
        if _:
            p = parse.parse(cls.OBJ_PATTERN, _[0])
            if p:
                dic.update(p.named)
            #
            ports_dict = collections.OrderedDict()
            dic['ports'] = ports_dict
            #
            i_port_dict = collections.OrderedDict()
            for i in _[1:]:
                i_p_0 = parse.parse(cls.PORT_PATTERN, i)
                if i_p_0:
                    i_port_dict = collections.OrderedDict()
                    i_name_0 = i_p_0.named['name']
                    i_type_0 = i_p_0.named['type']
                    i_assign_0 = 'input'
                    if i_type_0.startswith('output'):
                        i_type_0 = i_type_0.split(' ')[-1]
                        i_assign_0 = 'output'
                    #
                    i_port_dict['type'] = i_type_0
                    i_port_dict['assign'] = i_assign_0
                    i_port_dict['metadata'] = collections.OrderedDict()
                    ports_dict[i_name_0] = i_port_dict
                else:
                    i_p_1 = parse.parse(cls.DEFAULT_VALUE_PATTERN, i)
                    if i_p_1:
                        i_type = i_port_dict['type']
                        i_value_1 = i_p_1.named['value']
                        if i_type in ['int', 'float', 'string']:
                            i_value_1 = eval(i_value_1)
                        #
                        i_port_dict['value'] = i_value_1
                    else:
                        i_p_2 = parse.parse(cls.METADATA_PATTERN, i)
                        i_name_2 = i_p_2.named['name']
                        i_type_2 = i_p_2.named['type']
                        i_value_2 = i_p_2.named['value']
                        #
                        i_metadata_dict = collections.OrderedDict()
                        i_metadata_dict['type'] = i_type_2
                        if i_type_2 in ['int', 'float', 'string']:
                            i_value_2 = eval(i_value_2)
                        #
                        i_metadata_dict['value'] = i_value_2
                        i_port_dict['metadata'][i_name_2] = i_metadata_dict
        return dic
