# coding:utf-8
# cmds.file(new=1,force=1)
#
# cmds.unloadPlugin('lxConvertNodeExtra')
#
# cmds.loadPlugin('lxConvertNodeExtra')
#
# cmds.createNode('curveToMeshExtra')
#
# cmds.file('/data/f/lynxinode/test_1.ma', open=1)

cmds.file(new=1,force=1)

cmds.unloadPlugin('lxConvertNodeExtra')

cmds.loadPlugin('lxConvertNodeExtra')

# cmds.createNode('curveToMeshExtra')

cmds.file('/data/f/lynxinode/test_A.ma', open=1)

ctx = cmds.curveToMeshExtraContext(nop=1)
cmds.setToolTo(ctx)


[cmds.setAttr('curveToMeshExtra1.vTranslateExtra[{}].vTranslateExtra_FloatValue'.format(i)) for i in range(10)]
[cmds.setAttr('curveToMeshExtra1.vRotateExtra[{}].vRotateExtra_FloatValue'.format(i)) for i in range(10)]
[cmds.setAttr('curveToMeshExtra1.vScaleExtra[{}].vScaleExtra_FloatValue'.format(i)) for i in range(10)]

