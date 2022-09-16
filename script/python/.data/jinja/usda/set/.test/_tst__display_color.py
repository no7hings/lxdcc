# coding:utf-8
from lxutil import utl_configure

key = 'usda/set/surface'

c = utl_configure.Jinja.get_configure(key)

k = 'display_color'

t = utl_configure.Jinja.get_template('{}/{}'.format(key, k))

raw = t.render(
    **c.value
)

print raw
