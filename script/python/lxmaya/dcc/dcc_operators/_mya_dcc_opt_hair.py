# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from lxbasic import bsc_core

from lxuniverse import unr_configure

from lxmaya import ma_core

from lxutil.dcc import utl_dcc_opt_abs


class XgenDescriptionOpt(utl_dcc_opt_abs.AbsObjOpt):
    def __init__(self, *args, **kwargs):
        super(XgenDescriptionOpt, self).__init__(*args, **kwargs)

    def get_path(self, lstrip=None):
        # remove namespace, use transform path
        raw = ma_core._ma_obj_path__get_with_namespace_clear_(self._obj.transform.path)
        # replace pathsep
        raw = raw.replace(self._obj.PATHSEP, unr_configure.Obj.PATHSEP)
        # strip path
        if lstrip is not None:
            if raw.startswith(lstrip):
                raw = raw[len(lstrip):]
        return raw

    def get_path_as_uuid(self, lstrip=None):
        return bsc_core.HashMtd.get_hash_value(self.get_path(lstrip), as_unique_id=True)

    def get_name(self):
        # use transform name
        raw = self._obj.transform.name
        raw = ma_core._ma_obj_name__get_with_namespace_clear_(raw)
        return raw

    def get_name_as_uuid(self):
        return bsc_core.HashMtd.get_hash_value(self.get_name(), as_unique_id=True)

    def get_usd_basis_curve_data(self):
        guides = cmds.ls(
            self._obj.transform.path, type='xgmSplineGuide', dagObjects=1, noIntermediate=1, long=1
        )
        points = []
        counts = []
        widths = [0.003]
        for i in guides:
            i_points = ma_core.CmdXgenSplineGuideOpt(
                i
            ).get_control_points()
            points.extend(i_points)
            counts.append(len(i_points))
            # widths.append(0.003)
        return counts, points, widths


class XgenSplineGuideOpt(utl_dcc_opt_abs.AbsObjOpt):
    def __init__(self, *args, **kwargs):
        super(XgenSplineGuideOpt, self).__init__(*args, **kwargs)

    def get_control_points(self):
        return ma_core.CmdXgenSplineGuideOpt(
            self._obj.path
        ).get_control_points()

    def get_curve_data(self):
        points = self.get_control_points()
        degree = 2
        form = 1
        count = len(points)
        knots = ma_core.Om2Method._get_curve_knots_(count, degree)
        span = count - 3
        return points, knots, degree, form, span

    def get_usd_curve_data(self):
        points = self.get_control_points()
        degree = 2
        form = 1
        count = len(points)
        knots = ma_core.Om2Method._get_curve_knots_(count, degree)
        span = count - 3
        ranges = [(0, 1)]
        widths = [.1]
        order = [degree]
        return points, knots, ranges, widths, order

    def get_usd_basis_curve_data(self):
        points = self.get_control_points()
        counts = [len(points)]
        widths = [0.003]
        return counts, points, widths
