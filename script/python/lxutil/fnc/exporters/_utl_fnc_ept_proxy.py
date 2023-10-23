# coding:utf-8
from lxbasic import bsc_core

import lxresource.core as rsc_core

from lxutil import utl_core

from lxutil.fnc import utl_fnc_obj_abs


class DotXarcExporter(utl_fnc_obj_abs.AbsFncOptionBase):
    OPTION = dict(
        file='',
        name='',
        jpg_file='',
        color=[],
        gpu_files=[],
        ass_files=[]
    )

    def __init__(self, option=None):
        super(DotXarcExporter, self).__init__(option)

    @classmethod
    def _set_j2_option_update_(cls, option, include_keys):
        def convert_fnc_(path_):
            return utl_core.PathEnv.map_to_env(
                path_, pattern='${KEY}'
            )

        #
        for i_k, i_v in option.items():
            if i_k in include_keys:
                if isinstance(i_v, (tuple, list)):
                    for j_seq, j in enumerate(i_v):
                        i_v[j_seq] = convert_fnc_(j)
                else:
                    option[i_k] = convert_fnc_(i_v)

    def set_run(self):
        option = self.get_option()
        #
        self._set_j2_option_update_(option, ['jpg_file', 'gpu_files', 'ass_files'])
        #
        file_path = option.get('file')
        #
        j2_template = rsc_core.RscJinjaConfigure.get_template('xarc/proxy')
        raw = j2_template.render(
            **self._option
        )

        bsc_core.StgFileOpt(file_path).set_write(
            raw
        )

        bsc_core.Log.trace_method_result(
            'dot-xarc-export',
            'file="{}"'.format(file_path)
        )


if __name__ == '__main__':
    DotXarcExporter(
        option={
            'jpg_file': u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/jpg/default.jpg',
            'name': 'ast_shl_cao_a_static',
            'color': [1, 1, 1],
            'file': u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/xarc/default/static.xarc',
            'gpu_files': [
                u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.abc',
                u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.lod01.abc',
                u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.lod02.abc'],
            'ass_files': [
                u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.ass',
                u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.lod01.ass',
                u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.lod02.ass']
        }

    ).set_run()
