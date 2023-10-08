# coding:utf-8
from lxbasic import bsc_core

from lxutil import utl_core


class ScpOslFile(object):
    @classmethod
    def generate_katana_ui_template(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StgFileOpt(output_file_path)
        output_file_opt.create_directory()
        info = bsc_core.OslFileMtd.get_info(file_path)
        if info:
            j2_template = utl_core.Jinja.get_template('arnold/katana-ui-template-v002')
            raw = j2_template.render(
                **info
            )
            # print(raw)
            output_file_opt.set_write(raw)

    @classmethod
    def generate_maya_ui_template(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StgFileOpt(output_file_path)
        output_file_opt.create_directory()
        info = bsc_core.OslFileMtd.get_info(file_path)
        if info:
            j2_template = utl_core.Jinja.get_template('arnold/maya-ui-template-v002')
            raw = j2_template.render(
                **info
            )
            # print(raw)
            output_file_opt.set_write(raw)
