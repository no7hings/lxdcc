# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

import lxshotgun.operators as stg_operators

c = stg_objects.StgConnector()

r_q = c.get_stg_resource_query(
    project='nsa_dev', asset='nikki'
)
r_o = stg_operators.StgResourceOpt(r_q)

s_q = c.get_stg_step_query(
    step='srf'
)

s_o = stg_operators.StgStepOpt(s_q)

downstream_stg_steps = s_o.get_downstream_stg_steps()
print s_o.get_notice_stg_users()

print r_o.get_stg_tasks(downstream_stg_steps)

print r_o.get_stg_shots()

print r_o.get_shot_stg_tasks(downstream_stg_steps)

