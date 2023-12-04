# coding:utf-8
import lxbasic.core as bsc_core

import lxresource.core as rsc_core

key_name = 'payload'

key = 'usda/geometry/{}'.format(key_name)

c = rsc_core.ResourceJinja.get_configure(
    key
)

t = rsc_core.ResourceJinja.get_template(key)

raw = t.render(
    **c.value
)

print raw

bsc_core.StgFileOpt(
    '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/extend/geometry/usd/v003/{}.usda'.format(key_name)
).set_write(raw)


