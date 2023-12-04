# coding:utf-8
import platform as _platform

import pkgutil as _pkgutil

USD_FLAG = False

__pypxr = _pkgutil.find_loader('pxr')

if __pypxr:
    if _platform.system() == 'Linux':
        USD_FLAG = True

        from pxr import Usd, Sdf, Vt, Gf, Kind, UsdShade, UsdGeom, UsdLux
