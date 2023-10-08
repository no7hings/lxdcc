# coding:utf-8
import os

import glob

import re


def get_multiply_file_paths(file_path, ext_includes=None):
    def get_ext_replace_fnc_(file_path_, ext_):
        return os.path.splitext(file_path_)[0] + ext_
    #
    def set_os_path_reduce_fnc_(file_path_, pathsep_):
        path_ = file_path_.replace('\\', pathsep_)
        _ = path_.split(pathsep_)
        new_path = pathsep_.join([_i for _i in _ if _i])
        if path_.startswith(pathsep_):
            return pathsep_ + new_path
        return new_path
    #
    re_keys = [
        ('<udim>', 4),
        ('#', -1),
        (r'\$F04', 4),
        (r'\$F', 4),
        (r'%04d', 4),
    ]
    pathsep = '/'
    # convert pathsep
    file_path = set_os_path_reduce_fnc_(file_path, pathsep)
    #
    directory = os.path.dirname(file_path)
    base = os.path.basename(file_path)
    base_new = base
    for k, c in re_keys:
        r = re.finditer(k, base, re.IGNORECASE) or []
        for i in r:
            start, end = i.span()
            if c == -1:
                s = '[0-9]'
                base_new = base_new.replace(base[start:end], s, 1)
            else:
                s = '[0-9]' * c
                base_new = base_new.replace(base[start:end], s, 1)
    #
    glob_pattern = pathsep.join([directory, base_new])
    #
    list_ = glob.glob(glob_pattern)
    if list_:
        list_.sort()
    #
    add_list_ = []
    if isinstance(ext_includes, (tuple, list)):
        for ext in ext_includes:
            for i in list_:
                add_ = get_ext_replace_fnc_(i, ext)
                if os.path.isfile(add_) is True:
                    add_list_.append(add_)
    return list_ + add_list_


# print get_multiply_file_paths('/depts/td/dongchangbao/to_zhusun/test_multilply/udim_sequence/shader.<UDIM>.####.png', ['.tx'])
#
# print get_multiply_file_paths('/depts/td/dongchangbao/to_zhusun/test_multilply/udim_sequence/shader.<UDIM>.$F.png', ['.tx'])
#
# print get_multiply_file_paths('/depts/td/dongchangbao/to_zhusun/test_multilply/udim_sequence/shader.<UDIM>.$F04.png', ['.tx'])
#
# print get_multiply_file_paths('/depts/td/dongchangbao/to_zhusun/test_multilply/udim_sequence/shader.<UDIM>.$F04.png', ['.tx'])

# print get_multiply_file_paths('/depts/td/dongchangbao/to_zhusun/test_multilply/udim_sequence/shader.<UDIM>.%04d.png', ['.tx'])

print get_multiply_file_paths('/l/prod/shl/work/assets/chr/huotao/srf/surfacing/images/v008/c10170/v01/noise_uv_zuoramp/noise_uv_zuoramp.<udim>.####.exr', ['.tx'])
