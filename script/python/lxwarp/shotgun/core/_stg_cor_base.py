# coding:utf-8
import lxresource.core as rsc_core

import lxbasic.core as bsc_core


class StgUtil(object):
    CONFIGURE = rsc_core.ResourceContent.get_as_content('shotgun/main')

    URL = CONFIGURE.get('connection.url')
    SCRIPT = CONFIGURE.get('connection.script')
    CODE = CONFIGURE.get('connection.code')

    CA_CERTS = CONFIGURE.get('connection.ca_certs')

    CONNECTION = None

    @classmethod
    def generate_connection(cls):
        # noinspection PyUnresolvedReferences
        from shotgun_api3 import shotgun

        _ = shotgun.Shotgun(
            cls.URL,
            cls.SCRIPT,
            cls.CODE,
            ca_certs=bsc_core.StgPathMapper.map_to_current(
                cls.CA_CERTS
            )
        )
        return _

    @staticmethod
    def get_shot_frame_range(project_name, shot_name):
        # noinspection PyUnresolvedReferences
        import sgtk

        bundle = sgtk.platform.current_engine()
        if bundle:
            sg = bundle.shotgun
            shot = sg.find_one(
                'Shot', [
                    ['code', 'is', shot_name]
                ],
                ['sg_cut_in', 'sg_cut_out']
            )
            return shot.get('sg_cut_in'), shot.get('sg_cut_out')

    @staticmethod
    def get_project_resolution(project_name):
        # noinspection PyUnresolvedReferences
        import sgtk

        bundle = sgtk.platform.current_engine()
        if bundle:
            sg = bundle.shotgun
            project = sg.find_one(
                'Project',
                [
                    ['name', 'is', project_name]
                ],
                ['sg_resolution']
            )
            _ = project.get('sg_resolution')
            if _:
                return [int(i) for i in _.split('*')]


if __name__ == '__main__':
    c = StgUtil.generate_connection()
    print c

