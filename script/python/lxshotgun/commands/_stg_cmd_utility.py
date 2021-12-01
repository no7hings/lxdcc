# coding:utf-8
from lxshotgun import stg_core


def get_shot_frame_range(shot_name):
    # noinspection PyUnresolvedReferences
    import sgtk
    #
    bundle = sgtk.platform.current_engine()
    if bundle:
        sg = bundle.shotgun
        shot = sg.find_one('Shot', [['code', 'is', shot_name]], ['sg_cut_in', 'sg_cut_out'])
        return shot.get('sg_cut_in'), shot.get('sg_cut_out')


def get_project_resolution(project_name):
    # noinspection PyUnresolvedReferences
    import sgtk
    #
    bundle = sgtk.platform.current_engine()
    if bundle:
        sg = bundle.shotgun
        project = sg.find_one('Project', [['name', 'is', project_name]], ['sg_resolution'])
        _ = project.get('sg_resolution')
        if _:
            return [int(i) for i in _.split('*')]
