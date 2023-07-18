# coding:utf-8
from lxbasic import bsc_core

f_i = '/production/library/resource/all/imperfection/rain_drops_and_streaks_001/v0001/image/preview.png'

_, cmd = bsc_core.ImgFileOpt(
    f_i
).get_thumbnail_jpg_create_args_with_background_over(
    width=256, background_rgba=(71, 71, 71, 255)
)

if cmd:
    bsc_core.SubProcessMtd.execute_with_result(
        cmd
    )
