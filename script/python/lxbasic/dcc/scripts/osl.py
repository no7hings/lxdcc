# coding:utf-8
import lxbasic.core as bsc_core

import lxresource.core as rsc_core


class ScpOslFile(object):
    @classmethod
    def generate_katana_ui_template(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StgFileOpt(output_file_path)
        output_file_opt.create_directory()
        info = bsc_core.OslFileMtd.get_info(file_path)
        if info:
            j2_template = rsc_core.ResourceJinja.get_template('arnold/katana-ui-template-v002')
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
            j2_template = rsc_core.ResourceJinja.get_template('arnold/maya-ui-template-v002')
            raw = j2_template.render(
                **info
            )
            # print(raw)
            output_file_opt.set_write(raw)
