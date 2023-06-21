# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

import lxshotgun.operators as stg_operators

c = stg_objects.StgConnector()

t_q = c.get_stg_task_query(
    project='nsa_dev', asset='nikki', step='cam', task='camera'
)

t_o = stg_operators.StgTaskOpt(
    t_q
)

print t_o.get_notice_stg_users()
