# coding:utf-8
from lxbasic import bsc_core

import lxutil.fnc.exporters as utl_fnc_exporters

import lxresolver.commands as rsv_commands


class AbsSsnRsvApplication(object):
    def __init__(self):
        self._resolver = rsv_commands.get_resolver()
        self._any_scene_file_path = self._get_any_scene_file_path_()

    def _get_any_scene_file_path_(self):
        raise NotImplementedError()

    def get_rsv_project(self):
        return self._resolver.get_rsv_project_by_any_file_path(
            self._any_scene_file_path
        )

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

    def get_release_scene_src_file(self, version_scheme='match', ext_extras=None):
        """
        copy scene file to publish workspace:
            when target is exists, ignore;
            when file's workspace is "publish" return current file

        :param version_scheme: str(<version-scheme>), "match" or "new"
        :param ext_extras: list(<ext>)
        :return: str(<file-path>)
        """
        rsv_project = self.get_rsv_project()
        if rsv_project is None:
            raise RuntimeError()
        #
        workspace_release = rsv_project.get_workspace_release()
        workspace_source = rsv_project.get_workspace_source()
        workspace_user = rsv_project.get_workspace_user()
        workspace_temporary = rsv_project.get_workspace_temporary()
        # current workspace
        workspace_key_cur = rsv_project.WorkspaceKeys.Release
        workspace_cur = workspace_release
        rsv_scene_properties = self.get_rsv_scene_properties()
        if rsv_scene_properties is None:
            raise RuntimeError()
        #
        workspace = rsv_scene_properties.get('workspace')
        if workspace == workspace_cur:
            return self._any_scene_file_path
        # copy to current workspace
        elif workspace in [workspace_source, workspace_user, workspace_temporary]:
            rsv_task = self.get_rsv_task()
            scene_src_file_path_src = self._any_scene_file_path
            branch = rsv_scene_properties.get('branch')
            application = rsv_scene_properties.get('application')
            version = rsv_scene_properties.get('version')
            scene_src_file_unit = rsv_task.get_rsv_unit(
                keyword='{branch}-{application}-scene-src-file'.format(
                    **dict(branch=branch, application=application)
                )
            )
            if version_scheme == 'match':
                scene_src_file_path_tgt = scene_src_file_unit.get_result(
                    version=version
                )
            elif version_scheme == 'new':
                version_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='{branch}-release-version-dir'
                )
                version = version_rsv_unit.get_new_version()
                scene_src_file_path_tgt = scene_src_file_unit.get_result(
                    version=version
                )
            else:
                raise RuntimeError()
            #
            rsv_task.create_directory(
                workspace_key=workspace_key_cur
            )
            #
            scene_src_file_opt_src = bsc_core.StgFileOpt(scene_src_file_path_src)
            if scene_src_file_opt_src.get_is_exists() is True:
                scene_src_file_opt_tgt = bsc_core.StgFileOpt(scene_src_file_path_tgt)
                if scene_src_file_opt_tgt.get_is_exists() is False:
                    scene_src_file_opt_src.set_copy_to_file(scene_src_file_path_tgt)
                    if application == 'maya':
                        utl_fnc_exporters.DotMaExporter(
                            option=dict(
                                file_path_src=scene_src_file_path_src,
                                file_path_tgt=scene_src_file_path_tgt
                            )
                        ).set_run()
                    #
                    if ext_extras:
                        for i_ext in ext_extras:
                            i_src = '{}.{}'.format(scene_src_file_opt_src.path_base, i_ext)
                            i_tgt = '{}.{}'.format(scene_src_file_opt_tgt.path_base, i_ext)
                            bsc_core.StgFileOpt(i_src).set_copy_to_file(i_tgt)
                    return scene_src_file_path_tgt
                else:
                    return scene_src_file_path_tgt
            else:
                return scene_src_file_path_tgt
        else:
            raise RuntimeError()

    def get_temporary_scene_src_file(self, version_scheme='match', ext_extras=None):
        """
        copy scene file to output workspace:
            when target is exists, ignore;
            when file's workspace is "output" return current file

        :param version_scheme: str(<version-scheme>), "match" or "new"
        :param ext_extras: list(<ext>)
        :return: str(<file-path>)
        """
        rsv_project = self.get_rsv_project()
        if rsv_project is None:
            raise RuntimeError()
        #
        workspace_release = rsv_project.get_workspace_release()
        workspace_source = rsv_project.get_workspace_source()
        workspace_user = rsv_project.get_workspace_user()
        workspace_temporary = rsv_project.get_workspace_temporary()
        # current workspace
        workspace_key_cur = rsv_project.WorkspaceKeys.Temporary
        cur_workspace = workspace_temporary
        rsv_scene_properties = self.get_rsv_scene_properties()
        if rsv_scene_properties is None:
            raise RuntimeError()
        #
        workspace = rsv_scene_properties.get('workspace')
        if workspace == cur_workspace:
            return self._any_scene_file_path
        # copy to current workspace
        elif workspace in [workspace_source, workspace_user, workspace_release]:
            rsv_task = self.get_rsv_task()
            scene_src_file_path_src = self._any_scene_file_path
            branch = rsv_scene_properties.get('branch')
            application = rsv_scene_properties.get('application')
            version = rsv_scene_properties.get('version')
            output_scene_src_file_unit = rsv_task.get_rsv_unit(
                keyword='{branch}-temporary-{application}-scene-src-file'.format(
                    **dict(branch=branch, application=application)
                )
            )
            if version_scheme == 'match':
                scene_src_file_path_tgt = output_scene_src_file_unit.get_result(
                    version=version
                )
            elif version_scheme == 'new':
                version_rsv_unit = rsv_task.get_rsv_unit(
                    keyword='{branch}-temporary-version-dir'
                )
                version = version_rsv_unit.get_new_version()
                scene_src_file_path_tgt = output_scene_src_file_unit.get_result(
                    version=version
                )
            else:
                raise RuntimeError()
            #
            rsv_task.create_directory(
                workspace_key=workspace_key_cur
            )
            #
            scene_src_file_opt_src = bsc_core.StgFileOpt(scene_src_file_path_src)
            if scene_src_file_opt_src.get_is_exists() is True:
                scene_src_file_opt_tgt = bsc_core.StgFileOpt(scene_src_file_path_tgt)
                if scene_src_file_opt_tgt.get_is_exists() is False:
                    scene_src_file_opt_src.set_copy_to_file(scene_src_file_path_tgt)
                    if application == 'maya':
                        utl_fnc_exporters.DotMaExporter(
                            option=dict(
                                file_path_src=scene_src_file_path_src,
                                file_path_tgt=scene_src_file_path_tgt
                            )
                        ).set_run()
                    #
                    if ext_extras:
                        for i_ext in ext_extras:
                            i_src = '{}.{}'.format(scene_src_file_opt_src.path_base, i_ext)
                            i_tgt = '{}.{}'.format(scene_src_file_opt_tgt.path_base, i_ext)
                            bsc_core.StgFileOpt(i_src).set_copy_to_file(i_tgt)
                    return scene_src_file_path_tgt
                else:
                    return scene_src_file_path_tgt
            else:
                return scene_src_file_path_tgt
        else:
            raise RuntimeError()

    def get_virtual_publish_scene_src_file(self, keyword):
        cur_workspace = 'publish'
        rsv_scene_properties = self.get_rsv_scene_properties()
        if rsv_scene_properties is not None:
            workspace = rsv_scene_properties.get('workspace')
            if workspace == cur_workspace:
                return self._any_scene_file_path
            elif workspace == 'work':
                rsv_task = self.get_rsv_task()
                branch = rsv_scene_properties.get('branch')
                application = rsv_scene_properties.get('application')
                rsv_unit = rsv_task.get_rsv_unit(keyword=keyword)
                rsv_unit_result = rsv_unit.get_result(version='latest')
                rsv_unit_properties = rsv_unit.get_properties_by_result(rsv_unit_result)
                print rsv_unit_properties

    def get_virtual_output_scene_src_file_(self, keyword):
        pass
