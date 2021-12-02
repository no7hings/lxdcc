# coding:utf-8
import lxmaya.fnc.builders as mya_fnc_builders
#
rsv_entity = session.rsv_obj
#
project = rsv_entity.get('project')
asset = rsv_entity.get('asset')
#
mya_fnc_builders.AssetBuilder(
    option=dict(
        project=project,
        asset=asset,
        with_model_geometry=True,
        with_surface_geometry_uv_map=True,
        with_groom_geometry=True,
        with_surface_look=True
    )
).set_run()