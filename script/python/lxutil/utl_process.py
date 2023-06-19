# coding:utf-8


class MayaProcess(object):
    @classmethod
    def get_command(cls, option):
        import lxbasic.objects as bsc_objects

        c = bsc_objects.PackageContextNew(' '.join(['lxdcc', 'maya', 'maya@2019.2', 'usd', 'mtoa@4.2.1.1'])).get_command(
            args_execute=[
                (
                    r'-- maya -batch -command '
                    r'"python('
                    r'\"importlib=__import__(\\\"importlib\\\");'
                    r'ssn_commands=importlib.import_module(\\\"lxsession.commands\\\");'
                    r'ssn_commands.set_option_hook_execute(option=\\\"{hook_option}\\\")\")"'
                ).format(
                    hook_option='option_hook_key="dcc-process/maya-process"&'+option
                )
            ],
        )
        return c


if __name__ == '__main__':
    from lxbasic import bsc_core

    # cmd = MayaProcess.get_command(
    #     'method=fbx-to-usd&fbx={}&usd={}'.format(
    #         '/production/library/resource/all/3d_asset/cement_bollard_with_base_sdfx4/v0001/geometry/fbx/cement_bollard_with_base_sdfx4.fbx',
    #         '/production/library/resource/all/3d_asset/cement_bollard_with_base_sdfx4/v0001/geometry/usd/cement_bollard_with_base_sdfx4.usd'
    #     )
    # )
    #
    # bsc_core.SubProcessMtd.execute_with_result_in_linux(
    #     cmd, clear_environ='auto'
    # )
    # /production/shows/nsa_dev/assets/oth/genariceyes/user/work.wengmengdi/maya/scenes/srf_anishading/genariceyes.srf.srf_anishading.v001_002.ma
    cmd = MayaProcess.get_command(
        'method=collection-and-repath-texture&file={}&scene_directory={}&texture_directory={}'.format(
            '/production/shows/nsa_dev/assets/chr/nikki/shared/srf/srf_anishading/nikki.srf.srf_anishading.v003/source/nikki.ma',
            '/production/shows/nsa_dev/assets/chr/nikki/shared/srf/srf_anishading/nikki.srf.srf_anishading.v003/maya',
            '/production/shows/nsa_dev/assets/chr/nikki/shared/srf/srf_anishading/nikki.srf.srf_anishading.v003/texture'
        )
    )

    bsc_core.SubProcessMtd.execute_with_result_in_linux(
        cmd, clear_environ='auto'
    )
