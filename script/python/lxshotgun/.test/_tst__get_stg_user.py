# coding:utf-8
import urllib

import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

us = c.get_stg_users(name=['笔帽'])

print us

# print urllib.urlopen(i).read()

for i in us:
    print c.to_query(i).get('email')
    print c.to_query(i).get('login')
