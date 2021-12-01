# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxshotgun.objects as stg_objects

s_c = stg_objects.StgConnector()
s_c_q = s_c.get_stg_look_pass_query(project='cjd', look_pass='A2')
if s_c_q is None:
    pass

a = s_c_q.get('sg_asset')
if a:
    a_n = stg_objects.StgObjQuery(s_c, a).get('code')

# s_c_q.set_upload('image', '/data/f/look_pass/qunzhongnan_c/A2.snapshot/image.0000.jpg')