# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

import lxshotgun.operators as stg_operators

c = stg_objects.StgConnector()

v_q = c.get_stg_version_query(
    id='70080'
)
v_o = stg_operators.StgVersionOpt(v_q)

r_o = stg_operators.StgResourceOpt(v_o.get_stg_resource_query())

print r_o.get_cc_stg_users()

t_o = stg_operators.StgTaskOpt(v_o.get_stg_task_query())

print t_o.get_cc_stg_users()

