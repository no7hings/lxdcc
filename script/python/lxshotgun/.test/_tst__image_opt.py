# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects
#
import lxshotgun.operators as stg_operators


for i_look_pass in ['default', 'C2', 'C3', 'C4', 'C5']:

    f = '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/katana/output/{}/primary.####.exr'.format(
        i_look_pass
    )

    stg_operators.ImgFileOpt(
        utl_dcc_objects.OsFile(f)
    ).set_convert_to(
        output_file_path='/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/katana/output/{}.mov'.format(
            i_look_pass
        ),
        color_space='ACES CG'
    )
