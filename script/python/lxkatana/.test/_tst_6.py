# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxobj', 'lxresolver',
        'lxarnold',
        'lxutil', 'lxutil_gui',
        'lxkatana', 'lxkatana_gui'
    ]
)
p.set_reload()

from lxkatana.dcc import dcc_objects


mss = dcc_objects.MaterialAssigns.get_objs()

for ms in mss:
    v = ms.get_port('CEL').get()
    if 'nn_gongsifu_hair_collection' in v:
        v = v.replace('nn_gongsifu_hair_collection', 'nn_gongshifu_hair_collection')
        ms.get_port('CEL').set(v)
