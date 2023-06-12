# coding:utf-8
import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

print c.get_stg_project_query(project='nsa_dev').get_all_keys()

# print c.get_stg_project_query(project='nsa_dev').get('users')
