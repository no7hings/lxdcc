# coding:utf-8
import lxresolver.commands as rsv_cmds

r = rsv_cmds.get_resolver()

rsv_project = r.get_rsv_project(project='cjd')

print rsv_project.properties

print rsv_project.get_rsv_resources(branch='asset')
