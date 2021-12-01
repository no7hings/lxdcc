# coding:utf-8
from lxusd import commands

import lxresolver.commands as rsv_commands

resolver = rsv_commands.get_resolver()

work_source_file_path = '/l/prod/shl/work/assets/chr/shuitao/srf/srf_skin/katana/shuitao.srf.srf_skin.v012.katana'

task_properties = resolver.get_task_properties_by_work_scene_src_file_path(file_path=work_source_file_path)

commands.set_asset_work_set_usda_create(task_properties)

