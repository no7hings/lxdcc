# coding:utf-8
from lxbasic import bsc_core


# dic = bsc_core.StgDirectoryMultiplyMtd.get_all_multiply_file_dict(
#     '/data/f/sequence_chart_test/chr_a/R2', '*.%04d.*'
# )
#
# for k, v in dic.items():
#     print bsc_core.RawIntArrayMtd.merge_to(v)

# print bsc_core.StgFileMultiplyMtd.get_match_args(
#     'A.1001.1001.exr', '*.<udim>.%04d.*'
# )
# print bsc_core.StgFileMultiplyMtd.get_match_args(
#     'A.1001.exr', '*.####.*'
# )

print bsc_core.PtnMultiplyFileMtd.to_fnmatch_style(
    '*.$F03.$F04.*'
)
