# coding:utf-8
"""
this module is for the old call
"""
from lxbasic.core import *


if __name__ == '__main__':
    pass
    # print RawTextOpt('user_data_int').to_rgb_(
    #     s_p=10, v_p=10
    # )
    #
    # os.environ['LYNXI_CONFIGURES'] = '/data/e/myworkspace/td/lynxi/script/configure'
    # print RscConfigure.get_yaml('storage/path-mapper')
    # print RscConfigure.get_yaml('session/deadline/submiter')
    # print RscConfigure.get_yaml('session/deadline/rsv-task-submiter')
    # print RscConfigure.get_yaml('katana/node-graph/texture')
    #
    # print RscConfigure.get_yaml('arnold/node')
    # print RscConfigure.get_yaml('arnold/convert')
    #
    # print RscConfigure.get_yaml('clarisse/gui/menu')
    #
    # print RscConfigure.get_yaml('database/library/resource-basic')
    #
    # print RscConfigure.get_yaml('storage/asset-system-workspace')

    # print RawTextMtd.to_integer(
    #     'merge'
    # )
    # print RawTextOpt('abc').to_rgb_()
    #
    # print Resource.get(
    #     'lua-scripts'
    # )
    # print RawTextOpt(
    #     '1001-1120:5'
    # ).to_frames()

    # print StgPathPermissionBaseMtd.get_mode(
    #     'r-x', 'r-x', 'r-x'
    # )
    # StgPathPermissionMtd.lock_all_directories(
    #     '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture/main/v002'
    # )
    # print StgPathPermissionMtd.change_owner('/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture/main/v002')

    # StgPathPermissionMtd.change_owner(
    #     '/production/shows/nsa_dev/assets/chr/td_test/user/team.srf/extend/texture'
    # )
    # StgPathPermissionMtd.unlock_all_files(
    #     '/job/PLE/bundle/thirdparty/lxdcc_rsc/master-8/script/python/.resources/icons'
    # )
    #
    # print RawTextMtd.to_integer('geometry')
    # print RawTextOpt(
    #     'dreambae'
    # ).to_rgb_0()
    # print RawTextOpt(
    #     'dreambae_nightare'
    # ).to_rgb_0()
    # print RawTextMtd.to_integer(
    #     'l_out_eye_001_hishape'
    # )
    # StgPathPermissionMtd.create_directory(
    #     '/production/library/resource', 777
    # )
    # print ImgOiioOptForThumbnail(
    #     '/production/library/resource/all/atlas/sword_fern_pjvef2/v0001/image/preview.png'
    # ).generate_thumbnail(ext='.png')

    # print Resource.get(
    #     'asset/library/geometry_sphere.usda'
    # )
    # print SysBaseMtd.get_environment()
    # StgRarFileOpt(
    #     '/l/temp/zeqi/tex/test/DirtWipes 016.rar'
    # ).extract_all_elements_to(
    #     '/l/temp/zeqi/tex/test'
    # )
    # for i in [
    #     'DirtAWipes007',
    #     'Dirt007AWipes',
    #     'tube coral_v2 2.2'
    # ]:
    #     print RawTextMtd.clear_up_to(i)
    #     print i, RawTextMtd.split_any_to(i)

    # print [RawTextOpt(str(i)).to_rgb_(maximum=1) for i in range(898)]

    # from random import choice
    #
    # print [choice(range(6)) for i in range(898)]
    # print TimePrettifyMtd.to_prettify_by_timetuple(
    #     TimePrettifyMtd.to_timetuple(
    #         '2023-08-08 10:58:23', '%Y-%m-%d %H:%M:%S'
    #     ),
    #     language=1
    # )
    # print RawColorMtd.rgb_to_aces(
    #     1.0, 0.0, 0.0
    # )
    # print RawColorMtd.rgb_to_aces(
    #     0.188, 0.188, 0.188
    # )
    # print RawColorMtd.aces_to_rgb(
    #     0.188, 0.188, 0.188
    # )

    # input_ = FfmpegMtd.create_image_sequence_completion_cache(
    #     '/data/e/workspace/lynxi/test/maya/software-render/render/09/test/image/cam_full_body.####.jpg',
    #     (1, 160)
    # )

    # cmd = FfmpegMtd.get_image_concat_command(
    #     input='/l/temp/td/dongchangbao/render_test/render/test/cam_full_body.white/primary.####.jpg',
    #     output='/l/temp/td/dongchangbao/render_test/render/test/cam_full_body.white.mov',
    #     fps=24,
    #     start_frame=1,
    #     end_frame=80,
    # )
    #
    # print cmd
    #
    # PrcBaseMtd.execute_with_result(
    #     cmd
    # )

    # cmd = FfmpegMtd.test(
    #     input='/l/temp/td/dongchangbao/render_test/render/test/cam_head.white.mov'
    # )
    # PrcBaseMtd.execute_with_result(
    #     cmd
    # )
    #
    # cmd = FfmpegMtd.test(
    #     input='/l/temp/td/dongchangbao/render_test/upper_body.mov'
    # )
    # PrcBaseMtd.execute_with_result(
    #     cmd
    # )

    # cmd = FfmpegMtd.get_vedio_concat_command(
    #     input=[
    #         '/l/temp/td/dongchangbao/render_test/render/test/cam_full_body.white.mov',
    #         '/l/temp/td/dongchangbao/render_test/render/test/cam_full_body.wireframe.mov'
    #     ],
    #     output='/l/temp/td/dongchangbao/render_test/render/test/cam_full_body.mov',
    # )
    # print cmd
    # PrcBaseMtd.execute_with_result(
    #     cmd
    # )

    # inputs = FfmpegMtd.completion_image_sequences(
    #     '/data/e/workspace/lynxi/test/maya/software-render/render/test_4.2023_0825_1952_59/cam_head.white/primary.####.jpg',
    #     frame_range=(1, 80),
    #     frame_step=5,
    # )

    # def test(a):
    #     print A
    #
    # t_p = TrdFncsChainPool()
    # all_fnc_args = [
    #     ('start a', functools.partial(test, 'test a \n')),
    #     ('start b', functools.partial(test, 'test b \n')),
    #     ('start c', functools.partial(sys.stdout.write, 'test c \n'))
    # ]
    # for i_label, i_fnc in all_fnc_args:
    #     i_t = t_p.create_one(i_fnc)
    #     i_t.connect_started_to(
    #         functools.partial(sys.stdout.write, i_label + '\n')
    #     )
    #     i_t.connect_failed_to(lambda x: sys.stdout.write(x+'\n'))
    #
    # t_p.start_all()

    # c_c = RawRgbRange(count=10000)
    # print c_c.get_rgb(1)
    # print StgTextureOpt(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg'
    # ).get_udim_region_args()
    # print StgTextureOpt(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg'
    # ).get_units()

    # original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 示例列表
    #
    # print RawListMtd.grid_to(original_list, 4)

    # def fnc_(t_):
    #     _m = 10
    #     for _i in range(_m):
    #         time.sleep(.5)
    #         t_.update_processing()
    #
    # t = TrdFncProcessing()
    #
    # t.connect_started_to(fnc_)
    #
    # t.run()

    # print StgTextureMtd.get_unit_paths(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.1001.jpg'
    # )
    # print StgTextureMtd.get_unit_paths(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg'
    # )
    # print StgTextureMtd.get_udim_region_args(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.1002.jpg'
    # )
    # print StgTextureMtd.get_udim_region_args(
    #     '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg'
    # )

    # print Executes.oslc()

    # r, g, b = 255, 127, 63
    # print ((b+1)/2+32)-1

    # print RscIcon.find_all_file_keys_at('application')

    print RawTextMtd.find_words('IWork a')


