# coding:utf-8
from urllib import quote, unquote

d = u'测试'

d_0 = quote(d.encode('utf-8'))

print d_0

print unquote(d_0)


print unquote('aaaa')

