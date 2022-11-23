# coding:utf-8
import lxdatabase.objects as dtb_objects

p_ = '{key}_{size}_{tag}.{ext}'


cfg_f = '/data/e/myworkspace/td/lynxi/script/python/lxdatabase/.data/lib-configure.yml'
dtb = dtb_objects.DtbResourceLib(cfg_f)


print dtb.get_entity(
    entity_type='assign',
    filters=[
        ('node', 'is', '/surface/stained_concrete_wall_vdxicdm')
    ]
)


print dtb.get_entities(
    entity_type=dtb.EntityTypes.Assign,
    filters=[
        ('node', 'is', '/surface/thai_beach_sand_tdsmeeko')
    ]
)
