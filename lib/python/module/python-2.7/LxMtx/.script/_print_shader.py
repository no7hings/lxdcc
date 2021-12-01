# coding=utf-8
from LxMa2mtx import ma2mtxObjects


def printShader(shaderSeq, shaderName):
    n = ma2mtxObjects.Node(shaderName)

    ss = [
        '### {}'.format(shaderName),
        '',
        '![Bllod](/data/f/shader_test/maya_output/shader.{}.png)'.format(str(shaderSeq + 1).zfill(4)),
        '',
        '|Attribute Name|Data Type|Value|',
        '|----|----|----|'
    ]

    for p in n.tgtNode().inports():
        portname = p.portname().toString()
        if not portname.startswith(('aov_', 'id')):
            if p.isChannel() is False:
                datatype = p.datatype().toString()
                fs = [portname, datatype]
                if p.isValueChanged():
                    fs.append('<u>{}</u>'.format(p.portraw()))
                else:
                    fs.append(p.portraw())
                ss.append('|{}|{}|{}|'.format(*fs))
    ss.append('')
    print '\n'.join(ss)


gs = [u'Blood_Geo', u'Brushed_Metal_Geo', u'Car_Paint_Geo', u'Car_Paint_Metallic_Geo', u'Ceramic_Geo', u'Chrome_Geo', u'Clay_Geo', u'Copper_Geo', u'Frosted_Glass_Geo', u'Glass_Geo', u'Gold_Geo', u'Honey_Geo', u'Incandescent_Bulb_Geo', u'Jade_Geo', u'Milk_Geo', u'Orange_Juice_Geo', u'Plastic_Geo', u'Rubber_Geo', u'Thin_Plastic_Geo', u'Two_Tone_Car_Paint2_Geo', u'Velvet_Geo', u'Wax_Geo']

ss = []
for seq, g in enumerate(gs):
    s = g[:-4]
    printShader(seq, s)
