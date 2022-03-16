# coding:utf-8
from lxutil import utl_core

import lxutil.dcc.dcc_objects as utl_dcc_objects

import os


class ImageOpt(object):
    COLOR_SPACE_OPTION = {
        'ACEScg_sRGB': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/sRGB_for_ACEScg_Maya.csp',
        'ACEScg_Rec709': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/Rec.709_for_ACEScg_Maya.csp'
    }
    def __init__(self, obj):
        self._obj = obj
        #
        if utl_core.System.get_is_windows():
            self._rv_io_path = 'C:/Program Files/Shotgun/*/bin/rvio_hw.exe'
            self._rv_ls_path = 'C:/Program Files/Shotgun/*/bin/rvls.exe'
        elif utl_core.System.get_is_linux():
            self._rv_io_path = '/opt/rv/bin/rvio'
            self._rv_ls_path = '/opt/rv/bin/rvls'
        else:
            raise SystemError()

    def set_convert_to(self, output_file_path=None, color_space='Linear'):
        if os.path.isfile(self._rv_io_path):
            arguments = [self._rv_io_path]
            #
            input_file_path = self._obj.path
            input_file_path_base = self._obj.path_base
            input_ext = self._obj.ext
            if output_file_path is None:
                output_file_path = '{}{}'.format(input_file_path_base, '.mov')
            #
            output_file = utl_dcc_objects.OsFile(output_file_path)
            output_ext = output_file.ext
            output_file.set_directory_create()
            #
            arguments += [
                '"{}"'.format(input_file_path),
                '-quality', '1.0', '-scale', '1.0', '-o',
                '"{}"'.format(output_file_path),

            ]
            if color_space in ['ACES CG']:
                arguments += [
                    '-dlut "{}"'.format(
                        utl_core.Path.set_map_to_platform(
                            self.COLOR_SPACE_OPTION['ACEScg_sRGB']
                        )
                    )
                ]
            #
            utl_core.SubProcessRunner.set_run_with_result(
                ' '.join(arguments)
            )
            utl_core.Log.set_module_result_trace(
                'dot-mov-convert',
                u'file="{}"'.format(output_file_path)
            )
        else:
            utl_core.Log.set_module_warning_trace(
                'dot-mov-convert',
                u'bin="{}" is non-exists'.format(self._rv_io_path)
            )

    def get_mov_message(self):
        if os.path.isfile(self._rv_ls_path):
            arguments = [self._rv_ls_path]
            if self._obj.get_is_exists() is True:
                arguments += ['-x', '"{}"'.format(self._obj.path)]
                utl_core.SubProcessRunner.set_run_with_result(
                    ' '.join(arguments)
                )


class StgImageOpt(object):
    COLOR_SPACE_OPTION = {
        'ACEScg_sRGB': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/sRGB_for_ACEScg_Maya.csp',
        'ACEScg_Rec709': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/Rec.709_for_ACEScg_Maya.csp'
    }
    def __init__(self, obj):
        self._obj = obj
        #
        if utl_core.System.get_is_windows():
            self._rv_io_path = 'C:/Program Files/Shotgun/*/bin/rvio_hw.exe'
            self._rv_ls_path = 'C:/Program Files/Shotgun/*/bin/rvls.exe'
        elif utl_core.System.get_is_linux():
            self._rv_io_path = '/opt/rv/bin/rvio'
            self._rv_ls_path = '/opt/rv/bin/rvls'
        else:
            raise SystemError()


class AbsStgObjOpt(object):
    def __init__(self, stg_obj_query):
        self._stg_obj_query = stg_obj_query
    @property
    def shotgun(self):
        return self._stg_obj_query.shotgun
    @property
    def query(self):
        return self._stg_obj_query

    def __str__(self):
        return self._stg_obj_query.__str__()


class StgProjectOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgProjectOpt, self).__init__(stg_obj_query)

    def get_color_space(self):
        return self._stg_obj_query.get('sg_colorspace') or 'Linear'

    def set_stg_asset_create(self, **kwargs):
        self.shotgun.set_stg_entity_create(**kwargs)


class StgTaskOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgTaskOpt, self).__init__(stg_obj_query)

    def get_stg_assignees(self):
        return self._stg_obj_query.get('task_assignees') or []

    def set_stg_assignees_append(self, stg_user):
        self._stg_obj_query.set_stg_obj_append(
            'task_assignees', stg_user
        )

    def get_stg_status(self):
        return self._stg_obj_query.get('sg_status_list')

    def get_stg_last_version(self):
        return self._stg_obj_query.get('sg_last_version')

    def set_stg_last_version(self, stg_version):
        self._stg_obj_query.set_update('sg_last_version', stg_version)


class StgVersionOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgVersionOpt, self).__init__(stg_obj_query)

    def get_stg_tags(self):
        return self._stg_obj_query.get('tags') or []

    def set_stg_tags_append(self, stg_tag):
        self._stg_obj_query.set_stg_obj_append(
            'tags', stg_tag
        )

    def get_description(self):
        return self._stg_obj_query.get('description')

    def set_description(self, description):
        self._stg_obj_query.set_update('description', description)

    def set_folder(self, directory_path):
        windows_task_directory = utl_core.Path.set_map_to_windows(directory_path)
        linux_task_directory = utl_core.Path.set_map_to_linux(directory_path)
        stg_folder = {
            'name': directory_path,
            'local_path': directory_path,
            'local_path_windows': windows_task_directory,
            'local_path_linux': linux_task_directory
        }
        self.set_stg_folder(stg_folder)

    def set_stg_folder(self, stg_folder):
        self._stg_obj_query.set_update('sg_version_folder', stg_folder)

    def get_stg_folder(self):
        return self._stg_obj_query.get('sg_version_folder')

    def get_stg_type(self):
        return self._stg_obj_query.get('sg_version_type')

    def set_stg_type(self, stg_type):
        self._stg_obj_query.set_update('sg_version_type', stg_type)
        utl_core.Log.set_module_result_trace(
            'stg-version-set',
            u'stg-type="{}"'.format(stg_type)
        )

    def set_stg_status(self, stg_status):
        self._stg_obj_query.set_update('sg_status_list', stg_status)
        utl_core.Log.set_module_result_trace(
            'stg-version-set',
            u'stg-status="{}"'.format(stg_status)
        )

    def get_stg_status(self):
        return self._stg_obj_query.get('sg_status_list')

    def set_stg_todo(self, stg_todo):
        self._stg_obj_query.set_update('sg_todo', stg_todo)
        utl_core.Log.set_module_result_trace(
            'stg-version-set',
            u'stg-todo="{}"'.format(stg_todo)
        )

    def get_stg_todo(self):
        return self._stg_obj_query.get('sg_todo')

    def get_movie(self):
        return self._stg_obj_query.get('sg_uploaded_movie')

    def set_movie_upload(self, file_path):
        if os.path.isfile(file_path):
            self._stg_obj_query.set_upload('sg_uploaded_movie', file_path)
            utl_core.Log.set_module_result_trace(
                'stg-version-set',
                u'file="{}"'.format(file_path)
            )
        else:
            utl_core.Log.set_module_result_trace(
                'stg-version-set',
                u'file="{}" is non-exists'.format(file_path)
            )

    def set_log_add(self, text):
        key = 'sg_td_batch_log'
        _ = self._stg_obj_query.get(key) or u''
        if _:
            _ += '\n' + text
        else:
            _ += text

        self._stg_obj_query.set(
            key, _
        )

    def set_link_model_version(self, stg_version):
        self._stg_obj_query.set(
            'sg_model_version', stg_version
        )


class StgLookPassOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgLookPassOpt, self).__init__(stg_obj_query)

    def set_image_upload(self, file_path):
        if os.path.isfile(file_path):
            self._stg_obj_query.set_upload('image', file_path)
            utl_core.Log.set_module_result_trace(
                'stg-look-pass-upload',
                u'file="{}"'.format(file_path)
            )
        else:
            utl_core.Log.set_module_result_trace(
                'stg-look-pass-upload',
                u'file="{}" is non-exists'.format(file_path)
            )

    def set_link_surface_version(self, stg_version):
        self._stg_obj_query.set(
            'sg_surface_version', stg_version
        )

    def set_link_render_stats_file(self, file_path):
        self._stg_obj_query.set_upload(
            'sg_render_stats_file', file_path
        )

    def set_link_render_profile_file(self, file_path):
        self._stg_obj_query.set_upload(
            'sg_render_profile_file', file_path
        )
