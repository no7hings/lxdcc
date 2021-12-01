# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import os

import glob


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
    FileSearch(['/data/f/game_test_0/S0270']).set_repath_to_orig()
