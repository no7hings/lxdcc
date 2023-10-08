# coding:utf-8
import copy

from lxbasic import bsc_core

import lxbasic.abstracts as bsc_abstracts


class DotUsdaFile(bsc_abstracts.AbsFileReader):
    """
    """
    def __init__(self, file_path):
        super(DotUsdaFile, self).__init__(file_path)

        # print self.lines

    def do_convert(self, mode='use_ass'):
        lines = self.get_lines()
        lines_new = copy.copy(lines)

        p_1 = bsc_core.PtnDocParseOpt(
            '{line_left}prepend references = @{abc_file}@<{location}>\n'
        )
        self.do_for_pattern(p_1, lines, lines_new, mode)

        f_o = bsc_core.StgFileOpt(self._file_path)
        output_file_path = '{}.fix{}'.format(
            f_o.path_base, f_o.ext
        )
        bsc_core.StgFileOpt(
            output_file_path
        ).set_write(
            ''.join(lines_new)
        )

    def do_for_pattern(self, p, lines, lines_new, mode):
        match_lines = p.get_matched_lines(lines)
        properties_p_ass = (
            '''{line_left}{{\n{line_left}    asset userProperties:pgOpIn:ass:opArgs:filename = @{ass_file}@\n'''
            '''{line_left}    string userProperties:pgOpIn:ass:opType = "ArnoldStandin"\n'''
        )
        properties_p_usd = (

        )
        for i_line in match_lines:
            i_variants = p.get_variants(i_line)
            if i_variants:
                i_index = lines.index(i_line)
                i_line_left = i_variants['line_left']
                i_line_new = '{}# {}'.format(i_line_left, i_line.lstrip())
                lines_new[i_index] = i_line_new
                #
                i_xform_start_index = i_index-1
                i_xform = lines[i_xform_start_index]
                i_xform_new = i_xform.replace('over "', 'def Xform "')
                lines_new[i_xform_start_index] = i_xform_new
                #
                i_properties_start_index = i_index + 2
                i_properties_start = lines[i_properties_start_index]
                if i_properties_start.strip() == '{':
                    i_line_left = i_properties_start.split('{')[0]
                    i_abc_file_path = i_variants['abc_file']
                    if mode == 'use_ass':
                        i_file_path_new = i_abc_file_path\
                            .replace('geometry/abc', 'proxy/ass')\
                            .replace('.abc', '.ass')
                    elif mode == 'use_usd':
                        i_file_path_new = i_abc_file_path\
                            .replace('geometry/abc', 'geometry/usd')\
                            .replace('.abc', '.usd')
                    else:
                        raise RuntimeError()
                    i_p_new = properties_p_ass.format(
                        line_left=i_line_left,
                        ass_file=i_file_path_new
                    )
                    lines_new[i_properties_start_index] = i_p_new


if __name__ == '__main__':
    DotUsdaFile(
        '/l/prod/cgm/work/assets/env/env_waterfall/srf/surfacing/clarisse/plants_013.usda'
    ).do_convert()

