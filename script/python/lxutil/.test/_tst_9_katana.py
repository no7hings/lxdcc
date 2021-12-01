# coding:utf-8
from lxutil.commands import _utl_cmd_product


e = _utl_cmd_product.AssetTaskFileGain(project='cg7', asset='king_cloud', step='srf', task='surfacing')

rs = e.get_look_file_export_args()


for k, v in rs.items():
    print k
    for i in v:
        print i
