# coding:utf-8
from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

import lxbasic.extra.methods as bsc_etr_methods

import lxresolver.commands as rsv_commands

r = rsv_commands.get_resolver()

p = r.get_rsv_project(
    project='nsa_dev'
)


m = bsc_etr_methods.get_module('new')

print m.EtrBase.get_app_execute_mapper(p)

f = m.EtrBase.get_deadline_configure_file(p)

deadline_configure = bsc_objects.Configure(value=f)

deadline_job_context = 'render'

if deadline_job_context:
    content_0 = deadline_configure.get_content(deadline_job_context)
    step = 'srf'
    if step:
        content_1 = content_0.get_content(step)
        print content_1
