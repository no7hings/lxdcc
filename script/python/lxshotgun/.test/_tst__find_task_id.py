# coding:utf-8
import lxshotgun.objects as stg_objects

c = stg_objects.StgConnector()

print c.find_task_id(
    project='nsa_dev',
    resource='z87',
    task='lightrig'
)

# import sys
#
# d = {'project': 'nsa_dev', 'shot': 'z87010'}
#
# sys.stdout.write(
#     (
#         '\033[34m'
#         'resolved environments:\n'
#         '\033[32m'
#         '{}'
#         '\033[0m\n'
#     ).format('\n'.join(['{}={}'.format(k.rjust(20), v) for k, v in d.items()]))
# )
