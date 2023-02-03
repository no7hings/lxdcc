# coding:utf-8
import itertools

import collections

from lxbasic import bsc_core

render_output_directory_path = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v025/render/katana-images'
render_output_file_path_pattern = '{directory}/main/{camera}.{layer}.{light_pass}.{look_pass}.{quality}/{render_pass}.{frame}.exr'

p = bsc_core.PtnParseOpt(render_output_file_path_pattern)
p.set_update(directory=render_output_directory_path)
matchers = p.get_matches()

layers = [
    'high', 'shape'
]

render_passes = ['primary', 'ass_asset_color', 'ass_group_color', 'ass_object_color', 'ass_shell_color', 'ass_wire']

dict_ = collections.OrderedDict()
for i_layer, i_render_pass in itertools.product(layers, render_passes):
    i_p = p.set_update_to(
        layer=i_layer, render_pass=i_render_pass
    )
    i_matchers = i_p.get_matches()
    for j_match in i_matchers:
        j_option = {}
        j_file_path = j_match['result']
        j_file_opt = bsc_core.StgFileOpt(j_file_path)
        i_f_name_new, i_frame = bsc_core.StgFileMultiplyMtd.get_match_args(
            j_file_opt.name, '*.%04d.exr'
        )
        i_f_new = '{}/{}'.format(j_file_opt.directory_path, i_f_name_new)
        j_option['name'] = i_render_pass
        j_option['image_foreground'] = '/l/resource/td/asset/image/foreground-v001/{}-{}.png'.format(
            i_layer, i_render_pass
        )
        dict_[i_f_new] = j_option

# resize
for k, i_v in dict_.items():
    i_f_src = k
    i_f_opt_src = bsc_core.StgFileOpt(k)
    i_f_tgt = '{}/resize/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
    i_f_opt_tgt = bsc_core.StgFileOpt(i_f_tgt)
    i_v['image_resize'] = i_f_tgt
    i_f_opt_tgt.set_directory_create()
    # bsc_core.ImgOiioMtd.set_fit_to(i_f_src, i_f_tgt, (2048, 2048))
# create background
for k, i_v in dict_.items():
    i_name = i_v['name']
    i_f_src = k
    i_f_opt_src = bsc_core.StgFileOpt(k)
    i_f_tgt = '{}/background/{}.exr'.format(i_f_opt_src.directory_path, i_name)
    i_f_opt_tgt = bsc_core.StgFileOpt(i_f_tgt)
    i_v['image_background'] = i_f_tgt
    i_f_opt_tgt.set_directory_create()
    # bsc_core.ImgOiioMtd.set_create_as_flat_color(i_f_tgt, (2048, 2048), (.25, .25, .25, 1))
# add background
for k, i_v in dict_.items():
    i_f_src = k
    i_f_opt_src = bsc_core.StgFileOpt(k)
    i_f_tgt = '{}/base/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
    i_f_opt_tgt = bsc_core.StgFileOpt(i_f_tgt)
    i_v['image_base'] = i_f_tgt
    i_resize = i_v['image_resize']
    i_background = i_v['image_background']
    i_f_opt_tgt.set_directory_create()
    # bsc_core.ImgOiioMtd.set_over_by(i_resize, i_background, i_f_tgt, (0, 0))
# add foreground
for k, i_v in dict_.items():
    i_f_src = k
    i_f_opt_src = bsc_core.StgFileOpt(k)
    i_f_tgt = '{}/final/{}'.format(i_f_opt_src.directory_path, i_f_opt_src.name)
    i_f_opt_tgt = bsc_core.StgFileOpt(i_f_tgt)
    i_v['image_final'] = i_f_tgt
    i_base = i_v['image_base']
    i_foreground = i_v['image_foreground']
    i_f_opt_tgt.set_directory_create()
    # bsc_core.ImgOiioMtd.set_over_by(i_foreground, i_base, i_f_tgt, (0, 0))

vedio_path = '/l/prod/cgm/publish/assets/chr/td_test/mod/modeling/td_test.mod.modeling.v025/render/katana-images/main/all.mov'

images_final = [v['image_final'] for k, v in dict_.items()]

bsc_core.VdoRvioOpt(
    option=dict(
        input=' '.join(['"{}"'.format(i) for i in images_final]),
        output=vedio_path
    )
).set_convert_to_vedio()
