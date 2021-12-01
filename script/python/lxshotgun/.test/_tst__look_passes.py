# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxshotgun.objects as stg_objects

s_c = stg_objects.StgConnector()

l_p_qs = s_c.get_stg_look_pass_queries(project='cjd')

for i_p_q in l_p_qs[:1]:
    print i_p_q
    i_stg_asset = i_p_q.get('sg_asset')
    old_name = i_p_q.get('code')
    asset = stg_objects.StgObjQuery(s_c, i_stg_asset).get('code')
    if not old_name.startswith(asset):
        look_pass = old_name
        new_name = '{}.{}'.format(asset, old_name)
        i_p_q.set('code', new_name)
