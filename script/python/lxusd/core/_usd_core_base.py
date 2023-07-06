# coding:utf-8
# noinspection PyUnresolvedReferences
from pxr import Usd, Sdf, Gf, UsdShade, UsdGeom, UsdLux

import six

from lxuniverse import unr_configure


# noinspection PyUnresolvedReferences
class UsdTypeMtd(object):
    TYPE_MAPPER = {
        unr_configure.Type.CONSTANT_BOOLEAN: Sdf.ValueTypeNames.Bool,
        unr_configure.Type.CONSTANT_INTEGER: Sdf.ValueTypeNames.Int,
        unr_configure.Type.CONSTANT_FLOAT: Sdf.ValueTypeNames.Float,
        unr_configure.Type.CONSTANT_STRING: Sdf.ValueTypeNames.String,
        #
        unr_configure.Type.COLOR_COLOR3: Sdf.ValueTypeNames.Color3f,
        unr_configure.Type.ARRAY_COLOR3: Sdf.ValueTypeNames.Color3fArray,
        #
        unr_configure.Type.ARRAY_STRING: Sdf.ValueTypeNames.StringArray,
    }
    @classmethod
    def get(cls, key):
        if key in cls.TYPE_MAPPER:
            return cls.TYPE_MAPPER[key]


class UsdPrimQuery(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim


class UsdStapeOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Imageable(self._usd_prim)

    def get_is_visible(self):
        p = self._usd_fnc.GetVisibilityAttr()
        if p:
            return p.Get() != UsdGeom.Tokens.invisible
        return True

    def set_visible(self, boolean):
        if boolean is True:
            self._usd_fnc.MakeVisible()
        else:
            self._usd_fnc.MakeInvisible()

    def swap_visibility(self):
        self.set_visible(
            not self.get_is_visible()
        )

    def get_primvar(self, key):
        if self._usd_fnc.HasPrimvar(key) is True:
            return self._usd_fnc.GetPrimvar(key).Get()


class UsdShaderOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdShade.Shader(self._usd_prim)

    def set_file(self, file_path):
        _ = self._usd_fnc.GetInput('file')
        if _ is None:
            _ = self._usd_fnc.CreateInput('file', Sdf.ValueTypeNames.Asset)
        _.Set(file_path)

    def set_metallic(self, value):
        _ = self._usd_fnc.GetInput('metallic')
        if _ is None:
            _ = self._usd_fnc.CreateInput('metallic', Sdf.ValueTypeNames.Float)
        _.Set(value)

    def set_ior(self, value):
        _ = self._usd_fnc.GetInput('ior')
        if _ is None:
            _ = self._usd_fnc.CreateInput('ior', Sdf.ValueTypeNames.Float)
        _.Set(value)

    def set_as_float(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Float)
        _.Set(value)

    def set_as_float3(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Float3)
        _.Set(value)

    def set_as_float4(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Float4)
        _.Set(value)

    def set_as_asset(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Asset)
        #
        _.Set(value)


class UsdMaterialAssignOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim

    def assign(self, *args):
        arg = args[0]
        r = self._usd_prim.CreateRelationship('material:binding')
        if isinstance(arg, six.string_types):
            r.AddTarget(
                self._usd_prim.GetStage().GetPrimAtPath(arg).GetPath()
            )
        elif isinstance(arg, Sdf.Path):
            r.AddTarget(
                arg
            )
        elif isinstance(arg, Usd.Prim):
            r.AddTarget(
                arg.GetPath()
            )


class UsdXformOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Xform(self._usd_prim)

    def set_translate(self, x, y, z):
        pass

    def set_matrix(self, matrix):
        op = self._usd_fnc.MakeMatrixXform()
        op.Set(Gf.Matrix4d(matrix))


class UsdArnoldGeometryPropertiesOpt(object):
    PROPERTIES_TYPE_MAPPER = dict(
        opaque=unr_configure.Type.CONSTANT_BOOLEAN,
        matte=unr_configure.Type.CONSTANT_BOOLEAN,
        # visibility
        self_shadows=unr_configure.Type.CONSTANT_BOOLEAN,
        # export
        sss_setname=None,
        trace_sets=None,
        # volume
        step_size=unr_configure.Type.CONSTANT_FLOAT,
        volume_padding=unr_configure.Type.CONSTANT_FLOAT,
        smoothing=unr_configure.Type.CONSTANT_BOOLEAN,
        # mesh-subdiv
        subdiv_type=unr_configure.Type.CONSTANT_STRING,
        subdiv_iterations=unr_configure.Type.CONSTANT_INTEGER,
        subdiv_adaptive_error=unr_configure.Type.CONSTANT_FLOAT,
        subdiv_adaptive_metric=unr_configure.Type.CONSTANT_STRING,
        subdiv_adaptive_space=unr_configure.Type.CONSTANT_STRING,
        subdiv_uv_smoothing=unr_configure.Type.CONSTANT_STRING,
        subdiv_smooth_derivs=unr_configure.Type.CONSTANT_BOOLEAN,
        subdiv_frustum_ignore=unr_configure.Type.CONSTANT_BOOLEAN,
        # mesh-displacement
        disp_height=unr_configure.Type.CONSTANT_FLOAT,
        disp_padding=unr_configure.Type.CONSTANT_FLOAT,
        disp_zero_value=unr_configure.Type.CONSTANT_FLOAT,
        disp_autobump=unr_configure.Type.CONSTANT_BOOLEAN,
        # curve
        mode=unr_configure.Type.CONSTANT_STRING,
        min_pixel_width=unr_configure.Type.CONSTANT_FLOAT,
    )
    VISIBILITY_MAPPER = dict(

    )
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Imageable(self._usd_prim)
        self._usd_mesh = UsdGeom.Mesh(self._usd_prim)

    def set_properties(self, data):
        for k, v in data.items():
            self.set_property(k, v)

        # self._usd_mesh.CreateSubdivisionSchemeAttr(
        #     UsdGeom.Tokens.catmullClark
        # )

    def set_property(self, key, value):
        if key in self.PROPERTIES_TYPE_MAPPER:
            path = 'arnold:{}'.format(key)
            if self._usd_fnc.HasPrimvar(path) is False:
                p = self._usd_fnc.CreatePrimvar(
                    path,
                    UsdTypeMtd.get(
                        self.PROPERTIES_TYPE_MAPPER[key]
                    )
                )
            else:
                p = self._usd_fnc.GetPrimvar(
                    path
                )
            p.Set(value)


class UsdLightOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._shaping_api = UsdLux.ShapingAPI(self._usd_prim)
        self._shadow_api = UsdLux.ShadowAPI(self._usd_prim)

    def set_shadow_enable(self, boolean):
        self._shadow_api.CreateShadowEnableAttr().Set(boolean)
        self._shadow_api.CreateShadowColorAttr().Set((1.0, 0.0, 0.0))

    def set_texture_file(self, value):
        usd_fnc = UsdLux.DomeLight(self._usd_prim)
        p = usd_fnc.GetTextureFileAttr()
        if not p:
            p = usd_fnc.CreateTextureFileAttr()
        p.Set(value)
