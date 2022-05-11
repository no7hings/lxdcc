# coding:utf-8
import lxmaya

lxmaya.set_reload()

import lxmaya.fnc.importers as mya_fnc_importers

xgen_collection_file_paths = [
    ''
]
xgen_collection_directory_path = ''

xgen_grow_file_paths = [
    ''
]


mya_fnc_importers.GeometryXgenImporter(
    option=dict(
        xgen_collection_file=xgen_collection_file_paths,
        xgen_collection_directory=xgen_collection_directory_path,
        xgen_location='/master/hair',
        #
        grow_file=xgen_grow_file_paths,
        grow_location='/master/hair/hair_shape/hair_growMesh',
    )
)
