# coding:utf-8
import lxusd.dcc.dcc_objects as usd_dcc_objects

usd_file_path = '/l/prod/cgm/publish/assets/env/builds_ca/srf/surfacing/builds_ca.srf.surfacing.v010/cache/usd/geo/hi.usd'
root = '/master'

s = usd_dcc_objects.Scene()

s.set_load_from_dot_usd(usd_file_path, root)

u = s.universe

print u.get_obj('/master/hi').get_children()
