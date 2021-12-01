# coding:utf-8
import lxbasic.objects as bsc_objects

c = bsc_objects.Configure(value={})

c.set('c', 'C')

c.set('b', '<c>')

c.set('a', '\\<A\\>')

c.set_flatten()

dict

print c['c']
