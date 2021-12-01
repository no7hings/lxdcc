# coding:utf-8
from lxutil import objects
d = {
    'option': {
        'x': 1,
        'asset_name': 'abc',
    },
    'root': '|<option.asset_name>',
    'x': '=(<option.x> + 2)*5'
}

c = objects.Configure(None, d)
c.set('asset_name', 'cc')
c.set_flatten()

print c.get('root')
print c.get('x')

print c
