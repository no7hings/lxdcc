# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

q = c.get_stg_user_query(
    user='dongchangbao'
)

i = q.get('groups')

print i

# print urllib.urlopen(i).read()
