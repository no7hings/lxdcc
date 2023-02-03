# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_configure


class ScpOslFile(object):
    @classmethod
    def set_katana_ui_template_create(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StgFileOpt(output_file_path)
        output_file_opt.set_directory_create()
        info = bsc_core.OslFileMtd.get_info(file_path)
        if info:
            j2_template = utl_configure.Jinja.ARNOLD.get_template('katana-ui-template-v002.j2')
            raw = j2_template.render(
                **info
            )
            # print(raw)
            output_file_opt.set_write(raw)
    @classmethod
    def set_maya_ui_template_create(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StgFileOpt(output_file_path)
        output_file_opt.set_directory_create()
        info = bsc_core.OslFileMtd.get_info(file_path)
        if info:
            j2_template = utl_configure.Jinja.ARNOLD.get_template('maya-ui-template-v002.j2')
            raw = j2_template.render(
                **info
            )
            # print(raw)
            output_file_opt.set_write(raw)
