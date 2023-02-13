# coding:utf-8
from lxbasic import bsc_configure, bsc_core


class RsvConfigureMtd(object):
    ENVIRON_KEY = 'LYNXI_RESOLVER_CONFIGURES'
    @classmethod
    def get_search_directories(cls):
        return bsc_core.EnvironMtd.get_as_array(cls.ENVIRON_KEY)
    @classmethod
    def get_basic_project_file(cls):
        return bsc_configure.Root.get_configure_file('resolver/basic/project')
    @classmethod
    def get_default_project_file(cls):
        return bsc_configure.Root.get_configure_file('resolver/default/project')
    @classmethod
    def get_default_project_files(cls):
        return [
            bsc_configure.Root.get_configure_file('resolver/{}/project'.format(i)) for i in ['default', 'new']
        ]
    @classmethod
    def get_all_project_files(cls):
        list_ = []
        for i_path in cls.get_search_directories():
            i_path_opt = bsc_core.StgPathOpt(i_path)
            if i_path_opt.get_is_exists() is True:
                i_glob_pattern = '{}/project.yml'.format(i_path_opt.path)
                i_results = bsc_core.StgExtraMtd.get_paths_by_fnmatch_pattern(
                    i_glob_pattern
                )
                list_.extend(i_results)
        return list_


class ResolverMtd(object):
    @classmethod
    def set_rsv_obj_sort(cls, rsv_objs):
        rsv_objs.sort(
            key=lambda x: bsc_core.RawTextMtd.to_number_embedded_args(x.path)
        )


if __name__ == '__main__':
    import lxbasic.objects as bsc_objects
    env = bsc_objects.Environ()
    env.LYNXI_RESOLVER_CONFIGURES += '/data/e/myworkspace/td/lynxi/script/configure/resolver/default'
    env.LYNXI_RESOLVER_CONFIGURES += '/data/e/myworkspace/td/lynxi/script/configure/resolver/new'
    print RsvConfigureMtd.get_basic_project_file()
    print RsvConfigureMtd.get_search_directories()
    print RsvConfigureMtd.get_all_project_files()
