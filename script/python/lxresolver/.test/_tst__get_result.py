# coding:utf-8
import collections

import lxresolver.commands as rsv_commands

c = collections.OrderedDict(
    [('keyword', 'asset-work-texture-tx-dir'), ('path', '/cgm/chr/bl_xiz_f/srf/surfacing/asset-work-texture-tx-dir'), ('pattern', u'{root}/{project}/{workspace}/assets/{role}/{asset}/{step}/{task}/texture/{layer}/{version}/tx'), (u'project', u'cgm'), ('type', 'unit'), ('root', '/l/prod'), ('root_secondary', '/t/prod'), ('root_primary', '/l/prod'), ('platform', 'linux'), (u'asset', u'bl_xiz_f'), ('branch', 'asset'), (u'role', u'chr'), (u'step', u'srf'), (u'task', u'surfacing'), (u'version', u'v001'), (u'workspace', u'work'), ('root_choice', 'root_primary'), (u'layer', u'main')]
)

r = rsv_commands.get_resolver()

print r.get_result(**c)
