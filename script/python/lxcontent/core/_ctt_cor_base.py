# coding:utf-8
import os

import yaml

import json

import collections


class CttYamlBase(object):
    @classmethod
    def dump(cls, raw, stream=None, **kwargs):
        class _Cls(yaml.SafeDumper):
            pass

        # noinspection PyUnresolvedReferences
        def _fnc(dumper_, data_):
            return dumper_.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data_.items(),
            )

        _Cls.add_representer(collections.OrderedDict, _fnc)
        return yaml.dump(raw, stream, _Cls, **kwargs)

    @classmethod
    def load(cls, stream):
        class _Cls(yaml.SafeLoader):
            pass

        # noinspection PyArgumentList
        def _fnc(loader_, node_):
            loader_.flatten_mapping(node_)
            return collections.OrderedDict(loader_.construct_pairs(node_))

        # noinspection PyUnresolvedReferences
        _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
        return yaml.load(stream, _Cls)


class CttYaml(object):
    def __init__(self, file_path):
        self._file_path = file_path

    def write(self, raw):
        with open(self._file_path, 'w') as y:
            CttYamlBase.dump(
                raw,
                y,
                indent=4,
                default_flow_style=False,
            )

    def read(self):
        with open(self._file_path) as y:
            raw = CttYamlBase.load(y)
            y.close()
            return raw


class CttFile(object):
    def __init__(self, file_path):
        self.__file_path = file_path

    def read(self):
        path = self.__file_path
        ext = os.path.splitext(path)[-1]
        if os.path.isfile(path):
            if ext in {'.json'}:
                with open(path) as j:
                    raw = json.load(j, object_pairs_hook=collections.OrderedDict)
                    j.close()
                    return raw
            elif ext in {'.yml'}:
                with open(path) as y:
                    raw = CttYamlBase.load(y)
                    y.close()
                    return raw
            else:
                with open(path) as f:
                    raw = f.read()
                    f.close()
                    return raw

    def write(self, raw):
        path = self.__file_path
        ext = os.path.splitext(path)[-1]
        directory = os.path.dirname(path)
        if os.path.isdir(directory) is False:
            # noinspection PyBroadException
            try:
                os.makedirs(directory)
            except Exception:
                return

        if ext in {'.json'}:
            with open(path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif ext in {'.yml'}:
            with open(path, 'w') as y:
                CttYamlBase.dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                )
        else:
            with open(path, 'w') as f:
                f.write(raw.encode('utf-8'))


class CttVariant(object):
    class OptTypes(object):
        Set = 'set'
        Append = 'append'
        Prepend = 'prepend'
        Remove = 'remove'

    PATHSEP = os.pathsep
    OPT_STACK = []
    OPT_CACHE = dict()

    class PyEnvironValue(str):
        def __init__(self, value):
            super(CttVariant.PyEnvironValue, self).__init__(value)
            self._value = value
            self._key = ''
            self._environ = None

        def __iadd__(self, value):
            if isinstance(value, (set, tuple, list)):
                [self._append_fnc_(i) for i in list(value)]
            else:
                self._append_fnc_(value)
            return self._new_fnc_()

        # env.TEST -= 'test'
        def __isub__(self, value):
            if isinstance(value, (set, tuple, list)):
                [self._remove_fnc_(i) for i in list(value)]
            else:
                self._remove_fnc_(value)
            return self._new_fnc_()

        # env.TEST == 'test'
        def __eq__(self, other):
            return self._eq_fnc_(other)

        def _get_args_(self):
            return (
                [i.lstrip().rstrip() for i in self._value.split(CttVariant.PATHSEP)],
                [i.lstrip().rstrip() for i in self._value.lower().split(CttVariant.PATHSEP)]
            )

        def _get_fnc_(self):
            return self._environ._opt_cache_get_fnc_(self._key)

        def _set_fnc_(self, value):
            self._value = value
            self._update_opt_stack_fnc_(
                self._key, value, CttVariant.OptTypes.Set
            )
            self._update_opt_cache_fnc_()

        def _append_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() not in list_lower:
                    list_origin.append(value)
                    self._value = CttVariant.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc_(
                        self._key, value, CttVariant.OptTypes.Append
                    )
                    self._update_opt_cache_fnc_()
            else:
                self._value = value
                self._update_opt_stack_fnc_(
                    self._key, value, CttVariant.OptTypes.Set
                )
                self._update_opt_cache_fnc_()

        def _prepend_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() not in list_lower:
                    list_origin.insert(0, value)
                    self._value = CttVariant.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc_(
                        self._key, value, CttVariant.OptTypes.Prepend
                    )
                    self._update_opt_cache_fnc_()
            else:
                self._value = value
                self._update_opt_stack_fnc_(
                    self._key, value, CttVariant.OptTypes.Set
                )
                self._update_opt_cache_fnc_()

        def _remove_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() in list_lower:
                    list_origin.remove(list_origin[list_lower.index(value.lower())])
                    self._value = CttVariant.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc_(
                        self._key, value, CttVariant.OptTypes.Remove
                    )
                    self._update_opt_cache_fnc_()
                    return True
            return False

        def _update_opt_stack_fnc_(self, key, value, opt_type):
            self._environ._opt_stack_update_fnc_(key, value, opt_type)

        def _update_opt_cache_fnc_(self):
            self._environ._opt_cache_set_fnc_(self._key, self._value)

        def _new_fnc_(self):
            environ_value = CttVariant.PyEnvironValue(self._value)
            environ_value.key = self._key
            environ_value.parent = self._environ

            self.parent.__dict__[self._key] = environ_value
            return environ_value

        def _eq_fnc_(self, value):
            return self._value == value

        @property
        def parent(self):
            return self._environ

        @parent.setter
        def parent(self, parent):
            self._environ = parent

        @property
        def key(self):
            return self._key

        @key.setter
        def key(self, key):
            self._key = key

        def get(self):
            return self._get_fnc_()

        def set(self, value):
            self._set_fnc_(value)

        def append(self, value):
            return self._append_fnc_(value)

        def prepend(self, value):
            return self._prepend_fnc_(value)

        def remove(self, value):
            return self._remove_fnc_(value)

        def __str__(self):
            return self._value or 'None'

        def __repr__(self):
            return self.__str__()

    def __init__(self, cache=None, variants=None):
        self._environ_opt_stack = CttVariant.OPT_STACK
        #
        if isinstance(cache, dict):
            self._environ_opt_cache = cache
        else:
            self._environ_opt_cache = CttVariant.OPT_CACHE
        #
        if isinstance(variants, dict):
            self._environ_variants = variants
        else:
            self._environ_variants = dict()

    @staticmethod
    def restore_cache():
        CttVariant.OPT_STACK = []
        CttVariant.OPT_CACHE = dict()

    def accept(self):
        pass

    # env.TEST
    def __getattr__(self, key):
        if key in ['_environ_opt_stack', '_environ_opt_cache', '_environ_variants']:
            return self.__dict__[key]
        else:
            return self._get_fnc_(key)

    # env.TEST = 'test'
    def __setattr__(self, key, value):
        if key in ['_environ_opt_stack', '_environ_opt_cache', '_environ_variants']:
            self.__dict__[key] = value
        else:
            self._set_fnc_(key, value)

    def _opt_stack_update_fnc_(self, key, value, opt_type):
        self._environ_opt_stack.append(
            (key, value, opt_type, self._environ_variants)
        )

    def _opt_cache_has_key_fnc_(self, key):
        return key in self._environ_opt_cache

    def _opt_cache_get_fnc_(self, key):
        return self._environ_opt_cache.get(key, '')

    def _opt_cache_set_fnc_(self, key, value):
        self._environ_opt_cache[key] = value

    def _opt_cache_get_all_fnc_(self):
        return self._environ_opt_cache

    #
    def _get_fnc_(self, key):
        key = key.upper()
        #
        environ_value = CttVariant.PyEnvironValue(self._opt_cache_get_fnc_(key))
        environ_value.key = key
        environ_value.parent = self
        #
        self.__dict__[key] = environ_value
        return environ_value.get()

    def _set_fnc_(self, key, value):
        key = key.upper()
        #
        environ_value = CttVariant.PyEnvironValue(value)
        environ_value.key = key
        environ_value.parent = self
        environ_value.set(value)
        self.__dict__[key] = environ_value

    def has_key(self, key):
        return self._opt_cache_has_key_fnc_(key)

    def has_value(self, key, value):
        value_ = self._opt_cache_get_fnc_(key)
        if value_ is not None:
            _ = [i.lstrip().rstrip() for i in value_.lower().split(CttVariant.PATHSEP)]
            return value.lower() in _
        return False

    def __str__(self):
        list_ = []
        for k, v in self._opt_cache_get_all_fnc_().items():
            list_.append('{} = {}'.format(k, v))
        list_.sort()
        return '\r\n'.join(list_)

    def __repr__(self):
        return self.__str__()


class CttEnvironment(CttVariant):
    def __init__(self):
        super(CttEnvironment, self).__init__(os.environ)

    def accept(self):
        pass


if __name__ == '__main__':
    print CttFile(
        '/data/e/workspace/lynxi/resource/plug/maya/easy_tools/scripts/easy/gui/qt.yml'
    ).read()
