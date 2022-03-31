# coding:utf-8
import os

import glob

from lxbasic import bsc_core

from lxutil import utl_configure, utl_core

from lxutil.fnc import utl_fnc_obj_abs

import lxutil.objects as utl_objects

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


class AbsDotXgenDef(object):
    @classmethod
    def _get_xgen_collection_file_paths_(cls, maya_scene_file_path):
        d = os.path.splitext(maya_scene_file_path)[0]
        glob_pattern = '{}__*.xgen'.format(d)
        return glob.glob(glob_pattern) or []
    @classmethod
    def _get_xgen_collection_names_(cls, maya_scene_file_path):
        file_paths = cls._get_xgen_collection_file_paths_(maya_scene_file_path)
        return [cls._get_xgen_collection_name_(i) for i in file_paths]
    @classmethod
    def _get_xgen_collection_name_(cls, xgen_collection_file_path):
        """
        :param xgen_collection_file_path: str()
        :return:
        """
        file_opt = bsc_core.StorageFileOpt(xgen_collection_file_path)
        file_name_base = file_opt.name_base
        return file_name_base.split('__')[-1]
    @classmethod
    def _set_xgen_collection_files_copy_(cls, file_path_src, file_path_tgt):
        file_paths_src = cls._get_xgen_collection_file_paths_(file_path_src)
        file_opt_tgt = bsc_core.StorageFileOpt(file_path_tgt)
        file_name_base_tgt = file_opt_tgt.name_base
        file_directory_path_tgt = file_opt_tgt.directory_path
        replace_list = []
        #
        for i_file_path_src in file_paths_src:
            i_file_opt_src = bsc_core.StorageFileOpt(i_file_path_src)
            i_file_name_src = i_file_opt_src.name
            i_xgen_collection_name = cls._get_xgen_collection_name_(i_file_path_src)
            i_file_name_tgt = '{}__{}.xgen'.format(file_name_base_tgt, i_xgen_collection_name)
            i_xgen_collection_file_path_tgt = '{}/{}'.format(file_directory_path_tgt, i_file_name_tgt)
            utl_dcc_objects.OsFile(i_file_path_src).set_copy_to_file(i_xgen_collection_file_path_tgt)
            #
            cls._set_xgen_collection_file_repair_(i_xgen_collection_file_path_tgt)
            #
            replace_list.append(
                (i_file_name_src, i_file_name_tgt)
            )
        #
        if replace_list:
            if os.path.isfile(file_path_tgt):
                with open(file_path_tgt) as f_r:
                    d = f_r.read()
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
                    with open(file_path_tgt, 'w') as f_w:
                        f_w.write(d)
    @classmethod
    def _set_xgen_collection_file_repath_(cls, xgen_collection_file_path, xgen_project_directory_path, xgen_collection_directory_path, xgen_collection_name):
        dot_xgen_file_reader = utl_objects.DotXgenFileReader(xgen_collection_file_path)
        dot_xgen_file_reader.set_project_directory_repath(xgen_project_directory_path)
        dot_xgen_file_reader.set_collection_directory_repath(
            xgen_collection_directory_path, xgen_collection_name
        )
        #
        dot_xgen_file_reader.set_save()
    @classmethod
    def _set_xgen_collection_file_repair_(cls, xgen_collection_file_path):
        i_dot_xgen_reader = utl_objects.DotXgenFileReader(xgen_collection_file_path)
        i_dot_xgen_reader.set_repair()
        i_dot_xgen_reader.set_save()


class DotMaExporter(
    utl_fnc_obj_abs.AbsExporter,
    AbsDotXgenDef
):
    OPTION = dict(
        file_path_src=None,
        file_path_tgt=None,
        root=None
    )
    def __init__(self, option):
        super(DotMaExporter, self).__init__(option)

    def set_run(self):
        file_path_src = self._option.get('file_path_src')
        file_path_tgt = self._option.get('file_path_tgt')
        #
        utl_dcc_objects.OsFile(file_path_src).set_copy_to_file(file_path_tgt)
        #
        self._set_xgen_collection_files_copy_(
            file_path_src,
            file_path_tgt
        )


class DotXgenExporter(
    utl_fnc_obj_abs.AbsFncOptionMethod,
    AbsDotXgenDef
):
    OPTION = dict(
        xgen_collection_file='',
        xgen_project_directory='',
        xgen_collection_directory='',
        xgen_collection_name='',
    )
    def __init__(self, option):
        super(DotXgenExporter, self).__init__(option)

    def set_run(self):
        option_opt = self.get_option()
        #
        xgen_collection_file_path = option_opt.get('xgen_collection_file')
        xgen_project_directory_path = option_opt.get('xgen_project_directory')
        xgen_collection_directory_path = option_opt.get('xgen_collection_directory')
        xgen_collection_name = option_opt.get('xgen_collection_name')
        #
        self._set_xgen_collection_file_repath_(
            xgen_collection_file_path,
            xgen_project_directory_path,
            xgen_collection_directory_path,
            xgen_collection_name,
        )


class DotXgenUsdaExporter(
    utl_fnc_obj_abs.AbsFncOptionMethod,
    AbsDotXgenDef
):
    OPTION = dict(
        file='',
        location='',
        maya_scene_file='',
    )
    def __init__(self, option=None):
        super(DotXgenUsdaExporter, self).__init__(option)

    def set_run(self):
        option_opt = self.get_option()
        file_path = option_opt.get('file')
        location = option_opt.get('location')
        location_dag_opt = bsc_core.DccPathDagOpt(location)
        maya_scene_file_path = option_opt.get('maya_scene_file')
        if maya_scene_file_path:
            xgen_collection_file_paths = self._get_xgen_collection_file_paths_(maya_scene_file_path)
            key = 'usda/asset-xgen'
            t = utl_configure.Jinja.get_template(
                key
            )

            c = utl_configure.Jinja.get_configure(
                key
            )
            for i_xgen_collection_file_path in xgen_collection_file_paths:
                i_xgen_collection_name = self._get_xgen_collection_name_(
                    i_xgen_collection_file_path
                )
                i_dot_xgen_file_reader = utl_objects.DotXgenFileReader(
                    i_xgen_collection_file_path
                )
                i_xgen_description_properties = i_dot_xgen_file_reader.get_description_properties()
                i_description_names = i_xgen_description_properties.get_top_keys()
                #
                c.set(
                    'asset.xgen.collections.{}.file'.format(i_xgen_collection_name),
                    bsc_core.StoragePathMtd.get_file_realpath(
                        file_path, i_xgen_collection_file_path
                    )
                )
                c.set(
                    'asset.xgen.collections.{}.description_names'.format(i_xgen_collection_name),
                    i_description_names
                )
            #
            c.set_flatten()
            raw = t.render(
                c.value
            )
            # print raw
            utl_core.File.set_write(
                file_path, raw
            )


if __name__ == '__main__':
    print DotXgenUsdaExporter(
        dict(
            file='/l/prod/cgm_dev/output/assets/chr/nn_14y_test/grm/groom/nn_14y_test.grm.groom.v001/cache/usd/xgen.usda',
            location='/master/hair',
            maya_scene_file='/l/prod/cgm_dev/output/assets/chr/nn_14y_test/grm/groom/nn_14y_test.grm.groom.v001/maya/nn_14y_test.ma',
        )
    ).set_run()
