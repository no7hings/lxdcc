# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

import lxshotgun.operators as stg_operators

c = stg_objects.StgConnector()

q = c.get_stg_step_query(
    step='srf'
)

print q

o = stg_operators.StgStepOpt(q)

print o.get_downstream_stg_steps()
