# coding:utf-8
import copy


class TextureTxCreator(object):
    OPTION = dict()
    def __init__(self, file_path=None, root=None, option=None):
        self._file_path = file_path
        self._root = root
        self._option = copy.copy(self.OPTION)
        if isinstance(option, dict):
            for k, v in option.items():
                if k in self.OPTION:
                    self._option[k] = v

    def set_run(self):
        pass
