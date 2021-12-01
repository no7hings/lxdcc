# coding:utf-8
import parse

parse_pattern = '\'{file}\'%{argument}'
e = "'/l/prod/cjd/work/assets/prp/chengzhen_b_shuimian/srf/surfacing/texture/ocean_tex_v01/ocean_displace.%04d.tx'%int(frame%326+1001)"
if e:
    p = parse.parse(parse_pattern, e)
    if p:
        print p.named.get('file'), p.named.get('argument')
