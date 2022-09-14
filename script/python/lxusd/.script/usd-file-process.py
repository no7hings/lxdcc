# coding:utf-8
import sys


def cache_hierarchy_fnc(option_opt):
    from lxusd import usd_core

    location = option_opt.get('location')
    file_path = option_opt.get('file')
    stage_opt = usd_core.UsdStageOpt(file_path)
    return [location+i for i in stage_opt.get_all_obj_paths()]


def main(argv):
    from lxbasic import bsc_core

    from lxusd import usd_setup

    usd_setup.UsdSetup.set_environs_setup()
    option = argv[1]
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    key = option_opt.get('method')
    if key == 'cache-hierarchy':
        print cache_hierarchy_fnc(option_opt)


if __name__ == '__main__':
    main(sys.argv)
