# coding:utf-8
import lxbasic.objects as bsc_objects

c = bsc_objects.Configure(value={})
print c

c.set('a', '\\<A\\>')
c.set('c', 'C')
c.set('b', '<c>')
c.set('e.a.b.c', '<c>')
print c

c.set_flatten()
print c
print c['b']
print c.get('b')

c.set('e.a.b.c', 'e')
print c
