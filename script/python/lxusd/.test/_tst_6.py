# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects; reload(utl_dcc_objects)
p = utl_dcc_objects.PyReloader(
    [
        'lxscheme',
        'lxobj', 'lxresolver',
        'lxarnold', 'lxusd',
        'lxutil', 'lxutil_gui',
        'lxmaya', 'lxmaya_gui',
        'publish'
    ]
)
p.set_reload()


from lxusd.fnc import exporters

e = exporters.GeometryInfoXmlExporter(
    file_path='/data/xml_test/test.xml',
    root='/master/hi'
)

