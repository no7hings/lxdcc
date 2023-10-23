# coding:utf-8
import lxbasic.core as bsc_core
p = bsc_core.PyReloader(
    [
        'lxuniverse', 'lxresolver',
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

