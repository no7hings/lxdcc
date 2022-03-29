# coding:utf-8
import lxutil.fnc.exporters as utl_fnc_exporters
from lxutil import utl_core

import lxresolver.commands as rsv_commands

import lxutil.dcc.dcc_objects as utl_dcc_objects


class AbsRsvApplication(object):
    def __init__(self):
        self._resolver = rsv_commands.get_resolver()
        self._any_scene_file_path = self._get_any_scene_file_path_()

    def _get_any_scene_file_path_(self):
        raise NotImplementedError()

    def get_rsv_task(self):
        return self._resolver.get_rsv_task_by_any_file_path(
            self._any_scene_file_path
        )

    def get_rsv_scene_properties(self):
        return self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
            self._any_scene_file_path
        )
    @classmethod
    def get_stg_connector(cls):
        import lxshotgun.objects as stg_objects
        return stg_objects.StgConnector()

    def set_file_send_to_publish(self, application):
        rsv_task = self.get_rsv_task()
        if rsv_task is not None:
            branch = rsv_task.get('branch')
            work_scene_src_file = utl_dcc_objects.OsFile(self._any_scene_file_path)
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
    #
    def get_scene_src_file(self, force=False):
        rsv_task = self.get_rsv_task()
        if rsv_task is not None:
            scene_file_path = self._get_any_scene_file_path_()
            rsv_scene_properties = rsv_task.get_rsv_scene_properties_by_any_scene_file_path(
                scene_file_path
            )
            # print rsv_scene_properties
            if rsv_scene_properties:
                workspace = rsv_scene_properties.get('workspace')
                if workspace in ['publish']:
                    return scene_file_path
                elif workspace in ['work']:
                    work_scene_src_file_path = scene_file_path
                    branch = rsv_scene_properties.get('branch')
                    application = rsv_scene_properties.get('application')
                    version = rsv_scene_properties.get('version')
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

    def get_output_scene_src_file(self, version_scheme='match'):
        rsv_scene_properties = self.get_rsv_scene_properties()
        if rsv_scene_properties is not None:
            workspace = rsv_scene_properties.get('workspace')
            if workspace == 'output':
                return self._any_scene_file_path
            elif workspace == 'work':
                rsv_task = self.get_rsv_task()
                work_scene_src_file_path = self._any_scene_file_path
                branch = rsv_scene_properties.get('branch')
                application = rsv_scene_properties.get('application')
                version = rsv_scene_properties.get('version')
                output_scene_src_file_unit = rsv_task.get_rsv_unit(
                    keyword='{branch}-output-{application}-scene-src-file'.format(
                        **dict(branch=branch, application=application)
                    )
                )
                if version_scheme == 'match':
                    scene_src_file_path = output_scene_src_file_unit.get_result(
                        version=version
                    )
                elif version_scheme == 'new':
                    version = rsv_task.get_new_version(workspace='output')
                    scene_src_file_path = output_scene_src_file_unit.get_result(
                        version=version
                    )
                else:
                    raise ValueError()

                work_scene_src_file = utl_dcc_objects.OsFile(work_scene_src_file_path)
                scene_src_file = utl_dcc_objects.OsFile(scene_src_file_path)
                if scene_src_file.get_is_exists() is False:
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
