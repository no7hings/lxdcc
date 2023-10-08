# coding:utf-8
import lxcontent.objects as ctt_objects

c = ctt_objects.Content(None, {})

c.set('test.a', 'a')

c.set('test.b', 'c')

print c
