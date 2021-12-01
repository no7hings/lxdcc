# coding:utf-8
from lxutil import objects

c = objects.Content(None, {})

c.set('test.a', 'a')

c.set('test.b', 'c')

print c
