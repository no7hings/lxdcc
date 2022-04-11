# coding:utf-8
import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

rsv_project = r.get_rsv_project(project='cjd')

print rsv_project

print rsv_project.get_rsv_entities(branch='asset')
print rsv_project.get_rsv_entities(branch='asset', role=['chr', 'prp', 'flg'])
print rsv_project.get_rsv_entities(branch='asset', role='chr')
print rsv_project.get_rsv_entities(branch='asset', role='ch*')
print rsv_project.get_rsv_entities(asset='nn_gongshifu')
print rsv_project.get_rsv_entities(asset='nn_gongshif*')
