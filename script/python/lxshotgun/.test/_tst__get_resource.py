# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

q = c.get_stg_resource_query(
    project='nsa_dev', asset='nikki'
)
print q.get('sg_test_thumb')

