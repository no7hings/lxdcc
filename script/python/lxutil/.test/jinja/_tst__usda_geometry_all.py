# coding:utf-8
import lxresource.core as rsc_core

key_name = 'auxiliary'

key = 'usda/geometry/all/{}'.format(key_name)

c = rsc_core.ResourceJinja.get_configure(
    key
)

t = rsc_core.ResourceJinja.get_template(key)

raw = t.render(
    **c.value
)

print raw

# bsc_core.StgFileOpt(
#     '/production/shows/nsa_dev/assets/chr/td_test/user/team.mod/extend/geometry/usd/v002/{}.usda'.format(key_name)
# ).set_write(raw)


