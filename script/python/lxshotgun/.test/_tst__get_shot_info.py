# coding:utf-8
import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

print c.get_stg_resource_queries(
    project='lib', branch='shot'
)
