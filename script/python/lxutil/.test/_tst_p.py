# coding:utf-8
import lxcontent.objects as ctt_objects

d = {
    'option': {
        'x': 1,
        'asset_name': 'abc',
    },
    'root': '|<option.asset_name>',
    'x': '=(<option.x> + 2)*5'
}

c = ctt_objects.Configure(None, d)
c.set('asset_name', 'cc')
c.set_flatten()

print c.get('root')
print c.get('x')

print c
