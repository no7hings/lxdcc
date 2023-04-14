# coding:utf-8
from lxutil import utl_core

key = 'usda/set/surface'

c = utl_core.Jinja.get_configure(key)

k = 'geo_extra'

t = utl_core.Jinja.get_template('{}/{}'.format(key, k))

raw = t.render(
    **c.value
)

print raw
