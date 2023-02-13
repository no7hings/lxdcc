# coding:utf-8
import json


class IspIgnore(object):
    def __init__(self, raw_string):
        if raw_string:
            self._raw = json.loads(raw_string) or {}
        else:
            self._raw = {}

    def get(self, fnc_isp_path, check_index):
        if fnc_isp_path in self._raw:
            return self._raw[fnc_isp_path].get(str(check_index), False)
        else:
            return False

    def set(self, fnc_isp_path, check_index, boolean):
        if fnc_isp_path in self._raw:
            _ = self._raw[fnc_isp_path]
        else:
            _ = {}
            self._raw[fnc_isp_path] = _
        _[str(check_index)] = boolean
    @property
    def raw_string(self):
        return json.dumps(self._raw)
