# coding:utf-8
import jinja2

from lxutil.dcc import dcc_objects

jinja_loader = jinja2.FileSystemLoader('/data/e/myworkspace/td/lynxi/script/python/lxusd/.data')

env = jinja2.Environment(loader=jinja_loader)

p = dict(
    properties=dict(
        asset='nn_gongshifu',
        dcc=dict(
            root='master'
        )
    ),
    roots=dict(
        geometry_hi='hi',
        hair='hair',
        effect='effect'
    ),
    files=dict(
        geometry_hi='/l/prod/shl/publish/assets/chr/nn_gongshifu/mod/modeling/nn_gongshifu.mod.modeling.v007/cache/usd/geo/hi.usd',
        hair='/l/prod/shl/publish/assets/chr/nn_gongshifu/grm/groom/nn_gongshifu.grm.groom.v003/cache/usd/registry.usda',
        effect='/t/prod/shl/publish/assets/vfx/shuiqunzi/efx/effects/shuiqunzi.efx.effects.v001/cache/registry.usda',
        uv_map_hi='/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/geometry/scene/v009/hi.usd',
    ),
    option=dict(
        up_axis='Y',
        unit=0.01
    ),
    sub_layers=[
        'look',
        'effect',
        'hair',
        'geometry',
    ]
)

set_j2_template = env.get_template('set-usda-template.j2')
set_file_path = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/set/scene/set.usda'
raw = set_j2_template.render(**p)
dcc_objects.OsFile(set_file_path).set_write(raw)

geometry_file_path = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/set/scene/geometry.usda'
geometry_j2_template = env.get_template('geometry-usda-template.j2')
raw = geometry_j2_template.render(**p)
dcc_objects.OsFile(geometry_file_path).set_write(raw)

hair_file_path = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/set/scene/hair.usda'
hair_j2_template = env.get_template('hair-usda-template.j2')
raw = hair_j2_template.render(**p)
dcc_objects.OsFile(hair_file_path).set_write(raw)

look_file_path = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/set/scene/look.usda'
look_j2_template = env.get_template('look-usda-template.j2')
raw = look_j2_template.render(**p)
dcc_objects.OsFile(look_file_path).set_write(raw)

effect_file_path = '/l/prod/shl/work/assets/chr/nn_gongshifu/srf/surfacing/set/scene/effect.usda'
effect_j2_template = env.get_template('effect-usda-template.j2')
raw = effect_j2_template.render(**p)
dcc_objects.OsFile(effect_file_path).set_write(raw)
