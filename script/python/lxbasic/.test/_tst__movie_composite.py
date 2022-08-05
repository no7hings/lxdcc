# coding:utf-8
from lxbasic import bsc_core

render_output_directory_path = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v025/render/katana-images'
render_output_file_path_pattern = '{directory}/main/{camera}.{layer}.{light_pass}.{look_pass}.{quality}/{render_pass}.{frame}.exr'

p = bsc_core.ParsePatternOpt(render_output_file_path_pattern)
p.set_update(directory=render_output_directory_path)
matchers = p.get_matches()

render_passes = [
    'primary', 'ass_object_color'
]

dict_ = {}
for i in matchers:
    i_layer = i['layer']
    i_render_pass = i['render_pass']
    if i_render_pass in render_passes:
        i_v = {}
        i_f = i['result']
        i_f_opt = bsc_core.StorageFileOpt(i_f)
        i_f_name_new, i_frame = bsc_core.MultiplyFileNameMtd.get_match_args(
            i_f_opt.name, '*.%04d.exr'
        )
        i_f_new = '{}/{}'.format(i_f_opt.directory_path, i_f_name_new)
        i_v['name'] = i_render_pass
        i_v['image_foreground'] = '/l/resource/td/asset/image/foreground/{}-{}.png'.format(
            i_layer, i_render_pass
        )
        dict_[i_f_new] = i_v
# resize
for k, i_v in dict_.items():
    i_f_src = k
    i_f_opt_src = bsc_core.StorageFileOpt(k)
    i_f_tgt = '{}/resize/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
    i_f_opt_tgt = bsc_core.StorageFileOpt(i_f_tgt)
    i_v['image_resize'] = i_f_tgt
    # i_f_opt_tgt.set_directory_create()
    # bsc_core.OiioMtd.set_fit_to(
    #     i_f_src, i_f_tgt, (2048, 2048)
    # )
# create background
for k, i_v in dict_.items():
    i_name = i_v['name']
    i_f_src = k
    i_f_opt_src = bsc_core.StorageFileOpt(k)
    i_f_tgt = '{}/background/{}.exr'.format(i_f_opt_src.directory_path, i_name)
    i_f_opt_tgt = bsc_core.StorageFileOpt(i_f_tgt)
    i_v['image_background'] = i_f_tgt
    # i_f_opt_tgt.set_directory_create()
    # bsc_core.OiioMtd.set_create_as_flat_color(
    #     i_f_tgt, (2048, 2048), (.25, .25, .25, 1)
    # )

# add background
for k, i_v in dict_.items():
    i_f_src = k
    i_f_opt_src = bsc_core.StorageFileOpt(k)
    i_f_tgt = '{}/base/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
    i_f_opt_tgt = bsc_core.StorageFileOpt(i_f_tgt)
    i_v['image_base'] = i_f_tgt
    i_resize = i_v['image_resize']
    i_background = i_v['image_background']
    # i_f_opt_tgt.set_directory_create()
    # bsc_core.OiioMtd.set_over_by(
    #     i_resize,
    #     i_background,
    #     i_f_tgt,
    #     (0, 0)
    # )
    print i_v

for k, i_v in dict_.items():
    i_f_src = k
    i_f_opt_src = bsc_core.StorageFileOpt(k)
    i_f_tgt = '{}/final/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
    i_f_opt_tgt = bsc_core.StorageFileOpt(i_f_tgt)
    i_base = i_v['image_base']
    i_foreground = i_v['image_foreground']
    print i_foreground, i_base
    print i_f_tgt
    i_f_opt_tgt.set_directory_create()
    bsc_core.OiioMtd.set_over_by(
        i_foreground,
        i_base,
        i_f_tgt,
        (0, 0)
    )
