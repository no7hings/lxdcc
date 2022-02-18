# coding:utf-8
import lxutil.fnc.exporters as utl_fnc_exporters
from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxutil.dcc.dcc_objects as utl_dcc_objects


class AbsRsvApplication(object):
    def __init__(self):
        self._resolver = rsv_commands.get_resolver()
        self._scene_file_path = self._get_scene_file_path_()

    def _get_scene_file_path_(self):
        raise NotImplementedError()

    def get_rsv_task(self):
        return self._resolver.get_rsv_task_by_work_file_path(
            self._scene_file_path
        )

    def set_file_send_to_publish(self, application):
        rsv_task = self.get_rsv_task()
        if rsv_task is not None:
            branch = rsv_task.get('branch')
            work_scene_src_file = utl_dcc_objects.OsFile(self._scene_file_path)
            work_scene_src_file_path = work_scene_src_file.path
            #
            scene_src_file_unit = rsv_task.get_rsv_unit(
                keyword='{branch}-{application}-scene-src-file'.format(
                    **dict(branch=branch, application=application)
                )
            )
            latest_scene_src_file_path = scene_src_file_unit.get_result(
                version='latest'
            )
            if latest_scene_src_file_path:
                latest_scene_src_file = utl_dcc_objects.OsFile(latest_scene_src_file_path)
                if work_scene_src_file.get_is_same_timestamp_to(latest_scene_src_file) is True:
                    utl_core.Log.set_module_warning_trace(
                        'file send',
                        'file="{}", "{}" is non-changed'.format(
                            work_scene_src_file_path,
                            latest_scene_src_file_path
                        )
                    )
                    return
            #
            new_scene_src_file_path = scene_src_file_unit.get_result(
                version='new'
            )
            #
            scene_src_file = utl_dcc_objects.OsFile(new_scene_src_file_path)
            if scene_src_file.get_is_exists() is False:
                utl_fnc_exporters.DotMaExport(
                    option=dict(
                        file_path_src=work_scene_src_file_path,
                        file_path_tgt=new_scene_src_file_path
                    )
                ).set_run()

    def get_scene_src_file(self, force=False):
        rsv_task = self.get_rsv_task()
        if rsv_task is not None:
            scene_file_path = self._get_scene_file_path_()
            rsv_task_properties = rsv_task.get_rsv_properties_by_any_file_path(
                scene_file_path
            )
            # print rsv_task_properties
            if rsv_task_properties:
                workspace = rsv_task_properties.get('workspace')
                if workspace in ['publish']:
                    return scene_file_path
                elif workspace in ['work']:
                    work_scene_src_file_path = scene_file_path
                    branch = rsv_task_properties.get('branch')
                    application = rsv_task_properties.get('application')
                    version = rsv_task_properties.get('version')
                    scene_src_file_unit = rsv_task.get_rsv_unit(
                        keyword='{branch}-{application}-scene-src-file'.format(
                            **dict(branch=branch, application=application)
                        )
                    )
                    scene_src_file_path = scene_src_file_unit.get_result(
                        version=version
                    )
                    work_scene_src_file = utl_dcc_objects.OsFile(work_scene_src_file_path)
                    scene_src_file = utl_dcc_objects.OsFile(scene_src_file_path)
                    if scene_src_file.get_is_exists() is False or force is True:
                        work_scene_src_file.set_copy_to_file(scene_src_file_path)
                        if application == 'maya':
                            utl_fnc_exporters.DotMaExport(
                                option=dict(
                                    file_path_src=work_scene_src_file_path,
                                    file_path_tgt=scene_src_file_path
                                )
                            ).set_run()
                        return scene_src_file_path
                    else:
                        return scene_src_file_path
                else:
                    raise ValueError()
