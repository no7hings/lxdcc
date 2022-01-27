# coding:utf-8
import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

# rsv_project = r.get_rsv_project(project='cjd')
#
# rsv_shot = rsv_project.get_rsv_entity(
#     shot='e10060'
# )
#
# print rsv_shot
#
# rsv_tasks = rsv_shot.get_rsv_tasks(step='efx*')
#
# for i_rsv_task in rsv_tasks:
#     print i_rsv_task.name


print r.get_rsv_entities(
    project='cjd', branch='shot'
)
