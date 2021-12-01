# coding:utf-8
import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

rsv_project = r.get_rsv_project(project='shl')

print rsv_project

rsv_entities = rsv_project.get_rsv_entities(branch='asset', role=['chr', 'prp', 'flg'])
print rsv_entities[0]
print rsv_project._project__get_rsv_objs_('/shl/chr/*')
