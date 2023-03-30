# coding:utf-8
import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

print c.find_task_id(
    project='nsa_dev',
    resource='td_test',
    task='surface'
)
