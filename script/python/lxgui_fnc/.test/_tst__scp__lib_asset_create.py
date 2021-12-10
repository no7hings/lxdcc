# coding:utf-8
import lxdeadline.objects as ddl_objects

import lxdeadline.methods as ddl_methods


method_query = ddl_objects.DdlMethodQuery(
    key='lib-asset-push', extend_option_kwargs=dict(configure='lib')
)

method = ddl_methods.DdlMethodRunner(
    method_option=method_query.get_method_option(),
    script_option=method_query.get_script_option(
        project='shl',
        assets=['cao_a'],
        with_system_create=True,
        with_shotgun_create=True,
        with_file_copy=True,
        #
        user='dongchangbao',
        td_enable=True
    )
)

method.set_run_with_deadline()
job_id = method.get_ddl_job_id()

print job_id
