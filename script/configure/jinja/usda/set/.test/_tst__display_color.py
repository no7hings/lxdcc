# coding:utf-8
import lxresource.core as rsc_core

key = 'usda/set/surface'

c = rsc_core.RscJinjaConfigure.get_configure(key)

k = 'geo_extra'

t = rsc_core.Jinja.get_template('{}/{}'.format(key, k))

raw = t.render(
    **c.value
)

print raw
