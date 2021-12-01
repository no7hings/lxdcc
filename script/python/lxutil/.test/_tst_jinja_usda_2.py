# coding:utf-8
from lxutil.objects import _utl_obj_raw

f = _utl_obj_raw.DotUsdaFile(
    '/data/f/look-properties-usd/usd/shading.usda'
)

f.set_surface_look_write(
    look_root_name='look',
    look_pass_name='default',
    look_pass_names=[
        'default',
        'C2',
        'C3',
        'C4',
        'C5',
    ],
    look_file_path='/data/f/look-properties-usd/look/klf/qunzhongnv_b.klf',
    look_properties_file_dict={
        u'C3': u'/data/f/look-properties-usd/usd/look/C3.properties.usda', 
        u'C2': u'/data/f/look-properties-usd/usd/look/C2.properties.usda', 
        u'default': u'/data/f/look-properties-usd/usd/look/default.properties.usda', 
        u'C5': u'/data/f/look-properties-usd/usd/look/C5.properties.usda', 
        u'C4': u'/data/f/look-properties-usd/usd/look/C4.properties.usda'
    }

)
#
# f = _utl_obj_raw.DotUsdaFile(
#     '/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v012/cache/usd/registry.usda'
# )
#
# f.set_surface_registry_write(
#     look_file_path='/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v012/cache/usd/shading.usda',
#     uv_map_file_path='/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v012/cache/usd/uv_map.usd',
# )
