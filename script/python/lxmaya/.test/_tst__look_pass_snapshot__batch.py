# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxresolver.commands as rsv_commands

import lxmaya.dcc.dcc_objects as mya_dcc_objects

import lxmaya.fnc.exporters as mya_fnc_exporter

import lxshotgun.objects as stg_objects

f = mya_dcc_objects.Scene.get_current_file_path()

r = rsv_commands.get_resolver()
s_c = stg_objects.StgConnector()
rsv_task_properties = r.get_task_properties_by_any_scene_file_path(file_path=f)
if rsv_task_properties:
    asset = rsv_task_properties.get('asset')

    n = mya_dcc_objects.Node('master')

    p = n.get_port('pg_lookpass')

    pass_names = p.get_enumerate_strings()

    for i, i_passe_name in enumerate(pass_names):
        if i_passe_name != 'default':
            p.set(i)
            mya_fnc_exporter.PreviewExporter(
                file_path='/data/f/look_pass/{}/{}.mov'.format(asset, i_passe_name),
                root='/master',
                option=dict(
                    use_render=False,
                    convert_to_dot_mov=True,
                )
            ).set_run()
            #
            s_c_q = s_c.get_stg_look_pass_query(project='cjd', look_pass=i_passe_name)
            if s_c_q:
                a = s_c_q.get('sg_asset')
                if a:
                    a_n = stg_objects.StgObjQuery(s_c, a).get('code')
                    if a_n == asset:
                        s_c_q.set_upload(
                            'image', '/data/f/look_pass/{}/{}.snapshot/image.0000.jpg'.format(asset, i_passe_name)
                        )
