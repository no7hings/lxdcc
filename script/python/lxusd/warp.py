# coding:utf-8
import pkgutil

USD_FLAG = False

__pypxr = pkgutil.find_loader('pxr')

if __pypxr:
    USD_FLAG = True

    from pxr import Usd, Sdf, Vt, Gf, Kind, UsdShade, UsdGeom, UsdLux
