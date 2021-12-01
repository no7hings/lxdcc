# coding:utf-8


def set_texture_tiles_preview_generate_script_job_create():
    """
    create script job for "texture tiles(UDIM, ...) preview" at scene opened
    """
    def fnc_():
        fs = cmds.ls(type='file')
        for f in fs:
            mel.eval('generateUvTilePreview {}'.format(f))
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    # noinspection PyUnresolvedReferences
    import maya.mel as mel

    index = cmds.scriptJob(parent='modelPanel4', event=['SceneOpened', fnc_])

    print 'create script job: "texture tiles preview generate" at {}'.format(index)


def set_camera_switch_script_job_create():
    """
    create script job for "light-rig camera switch"
    """
    def fnc_():
        i = cmds.getAttr('rig_locator.switch_camera')
        if i == 0:
            cmds.modelEditor('modelPanel4', edit=True, camera='full_body_cameraShape')
        elif i == 1:
            cmds.modelEditor('modelPanel4', edit=True, camera='upper_body_cameraShape')
        elif i == 2:
            cmds.modelEditor('modelPanel4', edit=True, camera='closeup_cameraShape')
    # noinspection PyUnresolvedReferences
    import maya.cmds as cmds
    # noinspection PyUnresolvedReferences
    import maya.mel as mel

    index = cmds.scriptJob(parent='modelPanel4', attributeChange=['rig_locator.switchCamera', fnc_])

    print 'create script job: "light-rig camera switch" at {}'.format(index)
