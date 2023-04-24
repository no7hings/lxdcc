# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core

key_name = 'main'

key = 'usda/geometry/{}'.format(key_name)

c = utl_core.Jinja.get_configure(
    key
)

t = utl_core.Jinja.get_template(key)

raw = t.render(
    **c.value
)

print raw

bsc_core.StgFileOpt(
    '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/geometry/usd/v024/{}.usda'.format(key_name)
).set_write(raw)


