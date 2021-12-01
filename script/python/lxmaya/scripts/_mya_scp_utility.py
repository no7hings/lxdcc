# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds
# noinspection PyUnresolvedReferences,PyPep8Naming
import maya.api.OpenMaya as om2

import os

import glob


class CurveRebuild(object):
    def __init__(self, density=None, span_count=None, sample=10):
        curve_paths = cmds.ls(type='nurbsCurve', selection=1, dagObjects=1, long=1) or []
        self._om2_curves = []
        for crv_pth in curve_paths:
            om2_crv_obj = om2.MGlobal.getSelectionListByName(crv_pth).getDagPath(0)
            om2_crv = om2.MFnNurbsCurve(om2_crv_obj)
            self._om2_curves.append(om2_crv)
        #
        self._density = density
        self._span_count = span_count
        self._sample = sample
    @classmethod
    def _set_range_map_(cls, range_0, range_1, value_0):
        value_min_0, value_max_0 = range_0
        value_min_1, value_max_1 = range_1
        #
        percent = float(value_0 - value_min_0) / (value_max_0 - value_min_0)
        #
        value_1 = (value_max_1 - value_min_1) * percent + value_min_1
        return value_1

    def set_rebuild(self):
        rebuild_dict = {}
        for om2_curve in self._om2_curves:
            path = om2_curve.fullPathName()
            if path in rebuild_dict:
                raw = rebuild_dict[path]
            else:
                raw = {}
                rebuild_dict[path] = raw
            #
            points, tangents = self._get_curve_derivatives_(om2_curve)
            raw['tangents'] = tangents
            raw['points'] = points
            span_count = self._get_curve_span_count_(om2_curve)
            raw['span_count'] = span_count

        first_point = None
        for k, v in rebuild_dict.items():
            points = v['points']
            point_0 = points[0]
            point_1 = points[-1]
            if first_point is None:
                first_point = point_0
            else:
                a = point_0.distanceTo(first_point)
                b = point_0.distanceTo(point_1)
                if a > b/2:
                    v['reverse'] = True

        if rebuild_dict:
            for k, v in rebuild_dict.items():
                span_count = v['span_count']
                if span_count is not None:
                    cmds.rebuildCurve(k, rebuildType=0, spans=span_count)
                reverse = v.get('reverse', False)
                if reverse is True:
                    print 'reverse curve: "{}"'.format(k)
                    cmds.reverseCurve(k, constructionHistory=0, replaceOriginal=1)

    def _get_curve_derivatives_(self, om2_curve):
        points = []
        tangents = []
        length = om2_curve.length()
        for i in range(self._sample+1):
            percent = 1/float(self._sample)*i
            value = self._set_range_map_((0, 1), (0, length), percent)
            param = om2_curve.findParamFromLength(value)
            point, tangent = om2_curve.getDerivativesAtParam(param, 4)
            points.append(point)
            tangent = tangent.normalize()
            tangents.append(tangent)
        return points, tangents

    def _get_curve_span_count_(self, om2_curve):
        length = om2_curve.length()
        if self._density is not None:
            return int(length*self._density)
        elif self._span_count is not None:
            return self._span_count


class MtdCurveRebuild(object):
    def __init__(self, density=None, span_count=None, sample=10):
        curve_paths = cmds.ls(type='nurbsCurve', selection=1, dagObjects=1, long=1) or []
        self._om2_curves = []
        for crv_pth in curve_paths:
            om2_crv_obj = om2.MGlobal.getSelectionListByName(crv_pth).getDagPath(0)
            om2_crv = om2.MFnNurbsCurve(om2_crv_obj)
            self._om2_curves.append(om2_crv)
        #
        self._density = density
        self._span_count = span_count
        self._sample = sample


class FileSearch(object):
    EXT_INCLUDE = [
        '.tga',
        '.png',
        '.jpg',
    ]
    TYPE_INCLUDE = [
        ('file', 'fileTextureName'),
        ('aiImage', 'filename')
    ]
    def __init__(self, paths):
        self._paths = paths
    #
    def _get_search_dict_(self):
        def _rcs_fnc(path_):
            _results = glob.glob(u'{}/*'.format(path_)) or []
            _results.sort()
            for _path in _results:
                if os.path.isfile(_path):
                    basename = os.path.basename(_path)
                    base, ext = os.path.splitext(basename)
                    ext = ext.lower()
                    if base in self._search_dict:
                        match_dict = self._search_dict[base]
                    else:
                        match_dict = {}
                        self._search_dict[base] = match_dict
                    #
                    if ext in match_dict:
                        match_list = match_dict[ext]
                    else:
                        match_list = []
                        match_dict[ext] = match_list
                    #
                    match_list.append(_path)
                elif os.path.isdir(_path):
                    _rcs_fnc(_path)

        self._search_dict = {}
        [_rcs_fnc(i) for i in self._paths]

    def _set_obj_repath_(self):
        for obj_type, atr_name in self.TYPE_INCLUDE:
            objs = cmds.ls(type=obj_type)
            for obj in objs:
                source = cmds.getAttr('{}.{}'.format(obj, atr_name))
                if os.path.isfile(source) is False:
                    basename = os.path.basename(source)
                    base, ext = os.path.splitext(basename)
                    ext = ext.lower()
                    search_exes = [i for i in self.EXT_INCLUDE if i != ext]
                    search_exes.insert(0, ext)
                    if base in self._search_dict:
                        match_dict = self._search_dict[base]
                        matches = [i for ext in search_exes for i in match_dict.get(ext, [])]
                        if matches:
                            target = matches[-1]
                            cmds.setAttr('{}.{}'.format(obj, atr_name), target, type='string')
                            print u'result: "{}" repath "{}"'.format(obj, target)
                    else:
                        print u'warning: "{}" is not found'.format(source)

    def set_run(self):
        self._get_search_dict_()
        self._set_obj_repath_()

    def set_repath_to_orig(self):
        for obj_type, atr_name in self.TYPE_INCLUDE:
            objs = cmds.ls(type=obj_type)
            for obj in objs:
                src_file_path = cmds.getAttr('{}.{}'.format(obj, atr_name))
                if os.path.isfile(src_file_path) is True:
                    if os.path.isfile(src_file_path) is True:
                        base, ext = os.path.splitext(src_file_path)
                        _ = glob.glob('{}.*'.format(base)) or []
                        lis = []
                        for i_file_path in _:
                            i_base, i_ext = os.path.splitext(i_file_path)
                            if not i_ext == ext:
                                lis.append(i_file_path)
                        if lis:
                            orig_file_path = lis[0]
                            cmds.setAttr('{}.{}'.format(obj, atr_name), orig_file_path, type='string')


if __name__ == '__main__':
    import lxmaya.scripts as mya_scripts
    mya_scripts.FileSearch(['/l/prod/shl/work/assets/env/altar/srf/surfacing/texture/scene']).set_run()
