# coding:utf-8
# import re
#
# k = r'(\()[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](\))(%04d)'
#
# base = 'caustic.(0001-0600)%04d.exr'
# c = 4
#
# r = re.finditer(k, base, re.IGNORECASE) or []
# base_new = base
# for i in r:
#     start, end = i.span()
#     s = '[0-9]' * c
#     print base[start:end]
#     base_new = base_new.replace(base[start:end], s, 1)
#
# print base_new
#
#
# from lxutil.dcc import dcc_objects
#
# f = dcc_objects.OsFile('/l/prod/shl/work/assets/chr/shuitao/srf/surfacing/houdini/caustic/v003_half02/caustic.(0001-0600)%04d.exr')
#
# print f.get_exists_files()


import parse

e = ''''/l/prod/shl/work/assets/chr/shuitao/srf/surfacing/houdini/caustic/v003_half02/caustic.%04d.exr'%(frame%600+1)'''

parse_pattern = '\'{file}\'%({argument})'

print parse.parse(parse_pattern, e)




