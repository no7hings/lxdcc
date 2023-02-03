# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


def set_ramps_convert():
    rmps = cmds.ls(type='ramp')
    c = 8
    for rmp in rmps:
        if not cmds.connectionInfo('{}.vCoord'.format(rmp), isExactDestination=1):
            continue
        inp = cmds.connectionInfo('{}.vCoord'.format(rmp), sourceFromDestination=1)

        for o in ['outColor', 'outColor.outColorR', 'outColor.outColorG', 'outColor.outColorB', 'outAlpha']:
            if not cmds.connectionInfo('{}.{}'.format(rmp, o), isExactSource=1):
                continue

            otps = cmds.connectionInfo('{}.{}'.format(rmp, o), destinationFromSource=1)

            idxs = [int(i) for i in cmds.getAttr('{}.colorEntryList'.format(rmp), multiIndices=1)]
            if [cmds.connectionInfo('{}.colorEntryList[{}].color'.format(rmp, i), isExactDestination=1) for i in
                idxs] == [False] * len(idxs):
                continue
            print 'start convert: "{}"'.format(rmp)
            rgbas = []
            for i in range(c):
                if i in idxs:
                    rgbas.append(
                        cmds.connectionInfo('{}.colorEntryList[{}].color'.format(rmp, i), sourceFromDestination=1) or
                        cmds.getAttr('{}.colorEntryList[{}].color'.format(rmp, i))[0]
                    )
                else:
                    rgbas.append(None)

            ar_rgba = '{}__rgba'.format(rmp)
            if cmds.objExists(ar_rgba) is False:
                cmds.shadingNode('aiLayerRgba', name=ar_rgba, asShader=1)

            rgbas.reverse()
            for i in range(c):
                v = rgbas[i]
                if v is not None:
                    cmds.setAttr('{}.enable{}'.format(ar_rgba, i + 1), True)
                    a = '{}.input{}'.format(ar_rgba, i + 1)
                    if isinstance(v, six.string_types):
                        if cmds.connectionInfo(a, isExactDestination=1) is False:
                            cmds.connectAttr(v, a)
                    elif isinstance(v, (tuple, list)):
                        cmds.setAttr(a, *v)
                    #
                    idx = c - i - 1
                    if idx > 0:
                        p0 = cmds.getAttr('{}.colorEntryList[{}].position'.format(rmp, idx - 1))
                        p1 = cmds.getAttr('{}.colorEntryList[{}].position'.format(rmp, idx))
                        ar_msk = '{}__msk_{}'.format(rmp, i + 1)
                        if cmds.objExists(ar_msk) is False:
                            cmds.shadingNode('aiRampFloat', name=ar_msk, asShader=1)
                            cmds.setAttr('{}.type'.format(ar_msk), 0)
                        cmds.setAttr('{}.ramp[0].ramp_Position'.format(ar_msk), p0)
                        cmds.setAttr('{}.ramp[0].ramp_FloatValue'.format(ar_msk), 0)
                        cmds.setAttr('{}.ramp[1].ramp_Position'.format(ar_msk), p1)
                        cmds.setAttr('{}.ramp[1].ramp_FloatValue'.format(ar_msk), 1)
                        #
                        a = '{}.input'.format(ar_msk)
                        if cmds.connectionInfo(a, isExactDestination=1) is False:
                            cmds.connectAttr(inp, a)
                        a = '{}.mix{}'.format(ar_rgba, i + 1)
                        if cmds.connectionInfo(a, isExactDestination=1) is False:
                            cmds.connectAttr('{}.outValue'.format(ar_msk), a)
                    #
                else:
                    cmds.setAttr('{}.enable{}'.format(ar_rgba, i + 1), False)
            if o == 'outAlpha':
                o_1 = 'outColor.outColorR'
            [cmds.connectAttr('{}.{}'.format(ar_rgba, o_1), i, force=1) for i in otps]
            print 'complete convert: "{}"'.format(rmp)


if __name__ == '__main__':
    set_ramps_convert()
