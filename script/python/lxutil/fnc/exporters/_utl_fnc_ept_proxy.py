# coding:utf-8
import os

from lxbasic import bsc_core

from lxutil import utl_configure, utl_core

from lxutil.fnc import utl_fnc_obj_abs


class DotXarcExporter(utl_fnc_obj_abs.AbsFncOptionMethod):
    OPTION = dict(
        file='',
        name='',
        jpg_file='',
        color=[],
        gpu_files=[],
        ass_files=[]
    )
    MAPPER_DICT = {
        '/l/prod': '${PG_PROJ_ROOT}',
        'l:/prod': '${PG_PROJ_ROOT}',
    }
    def __init__(self, option=None):
        super(DotXarcExporter, self).__init__(option)
    @classmethod
    def _set_j2_option_update_(cls, option, keys):
        def convert_fnc_(p_):
            for _k, _v in cls.MAPPER_DICT.items():
                if p_.lower().startswith(_k.lower()):
                    return _v + p_[len(_k):]
            return p_

        file_path = option.get('file')
        directory_path = os.path.dirname(file_path)
        #
        for i_k, i_v in option.items():
            if i_k in keys:
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
        j2_template = utl_configure.Jinja.XARC.get_template('proxy.j2')
        raw = j2_template.render(
            **self._option
        )

        bsc_core.StgFileOpt(file_path).set_write(
            raw
        )

        utl_core.Log.set_module_result_trace(
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
            'gpu_files': [u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.abc', u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.lod01.abc', u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.lod02.abc'],
            'ass_files': [u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.ass', u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.lod01.ass', u'/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.lod02.ass']
        }

    ).set_run()

