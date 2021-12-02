# coding:utf-8
from lxbasic import bsc_core


# dic = bsc_core.MultiplyDirectoryMtd.get_all_multiply_file_dict(
#     '/data/f/sequence_chart_test/chr_a/R2', '*.%04d.*'
# )
#
# for k, v in dic.items():
#     print bsc_core.IntegerArrayMtd.set_merge_to(v)

# print bsc_core.MultiplyFileNameMtd.get_match_args(
#     'A.1001.1001.exr', '*.<udim>.%04d.*'
# )
# print bsc_core.MultiplyFileNameMtd.get_match_args(
#     'A.1001.exr', '*.####.*'
# )

print bsc_core.MultiplyPatternMtd.to_fnmatch_style(
    '*.$F03.$F04.*'
)
