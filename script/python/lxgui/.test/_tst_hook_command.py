# coding:utf-8
from lxutil import utl_core

utl_core.SubProcessRunner.set_run_with_result(
    cmd='rez-env lxdcc -- lxhook-command -o "hook_key=kit-panels/app-kit"'
)


# print urllib.urlopen(
#     'http://localhost:9527/cmd-run?uuid=7D982728-6966-11EC-B911-2CFDA1C062BB'
# )
