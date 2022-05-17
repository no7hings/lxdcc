# coding:utf-8
import lxutil.objects as utl_objects

r = utl_objects.DotAssReader(
    '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v038/cache/ass/laohu_xiao.ass'
)

print r.get_file_paths()
