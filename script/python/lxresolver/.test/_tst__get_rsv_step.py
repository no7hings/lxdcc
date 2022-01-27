# coding:utf-8
import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

rsv_project = r.get_rsv_project(project='cgm_dev')

print rsv_project.get_rsv_steps(
    asset='nn_14y'
)
