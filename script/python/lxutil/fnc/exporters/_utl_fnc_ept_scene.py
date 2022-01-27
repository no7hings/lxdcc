# coding:utf-8
import os

import glob

from lxutil.fnc import utl_fnc_obj_abs

import lxutil.dcc.dcc_objects as utl_dcc_objects


class DotMaSceneInfoExporter(utl_fnc_obj_abs.AbsExporter):
    OPTION = dict(
        file_path=None,
        root=None
    )
    def __init__(self, option):
        super(DotMaSceneInfoExporter, self).__init__(option)

    def set_run(self):
        import os
        #
        import lxutil.scripts as utl_scripts
        #
        import lxutil.dcc.dcc_objects as utl_dcc_objects
        #
        file_path = self._option.get('file_path')
        root = self._option.get('root')
        #
        base, ext = os.path.splitext(file_path)
        r = utl_scripts.DotMaFileReader(file_path)
        _info = r.get_mesh_info(root=root)
        #
        utl_dcc_objects.OsYamlFile('{}.info.yml'.format(base)).set_write(_info)


class DotMaExport(utl_fnc_obj_abs.AbsExporter):
    OPTION = dict(
        file_path_src=None,
        file_path_tgt=None,
        root=None
    )
    def __init__(self, option):
        super(DotMaExport, self).__init__(option)

    @classmethod
    def _get_xgen_file_paths_(cls, file_path):
        current_file_path = file_path
        d = os.path.splitext(current_file_path)[0]
        p = '{}__*.xgen'.format(d)
        return glob.glob(p) or []
    @classmethod
    def _set_dot_xgen_file_copy_(cls, file_path_src, file_path_tgt):
        xgen_file_paths_src = cls._get_xgen_file_paths_(file_path_src)
        target_base = os.path.splitext(os.path.basename(file_path_tgt))[0]
        target_directory_path = os.path.dirname(file_path_tgt)
        replace_list = []
        for i_xgen_file_paths_src in xgen_file_paths_src:
            source_xgen_file_name = os.path.basename(i_xgen_file_paths_src)
            source_base = os.path.splitext(source_xgen_file_name)[0]
            xgen_name = source_base.split('__')[-1]
            target_xgen_file_name = '{}__{}.xgen'.format(target_base, xgen_name)
            target_xgen_file_path = '{}/{}'.format(target_directory_path, target_xgen_file_name)
            utl_dcc_objects.OsFile(i_xgen_file_paths_src).set_copy_to_file(target_xgen_file_path)
            replace_list.append(
                (source_xgen_file_name, target_xgen_file_name)
            )
        #
        if replace_list:
            if os.path.isfile(file_path_tgt):
                with open(file_path_tgt) as fr:
                    d = fr.read()
                    for i in replace_list:
                        s, t = i
                        d = d.replace(
                            r'setAttr ".xfn" -type "string" "{}";'.format(s),
                            r'setAttr ".xfn" -type "string" "{}";'.format(t)
                        )
                        d = d.replace(
                            r'"xgFileName" " -type \"string\" \"{}\""'.format(s),
                            r'"xgFileName" " -type \"string\" \"{}\""'.format(t)
                        )
                    with open(file_path_tgt, 'w') as fw:
                        fw.write(d)

    def set_run(self):
        file_path_src = self._option.get('file_path_src')
        file_path_tgt = self._option.get('file_path_tgt')
        #
        utl_dcc_objects.OsFile(file_path_src).set_copy_to_file(file_path_tgt)
        #
        self._set_dot_xgen_file_copy_(
            file_path_src,
            file_path_tgt
        )


if __name__ == '__main__':
    DotMaExport(
        option=dict(
            file_path_src='/l/prod/shl/work/assets/chr/huotao/srf/surfacing/maya/scenes/huotao.srf.surfacing.v022.ma',
            file_path_tgt='/l/prod/lib/work/assets/chr/ast_shl_huotao/srf/surfacing/maya/scenes/ast_shl_huotao.srf.surfacing.v001.ma'
        )
    ).set_run()
