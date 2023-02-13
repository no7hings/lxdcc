# coding:utf-8
import os


class PyEnviron(object):
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
                [i.lstrip().rstrip() for i in self._value.split(PyEnviron.PATHSEP)],
                [i.lstrip().rstrip() for i in self._value.lower().split(PyEnviron.PATHSEP)]
            )

        def _get_fnc_(self):
            return self._environ._opt_cache_get_fnc_(self._key)

        def _set_fnc_(self, value):
            self._value = value
            self._update_opt_stack_fnc_(
                self._key, value, PyEnviron.OptTypes.Set
            )
            self._update_opt_cache_fnc_()

        def _append_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() not in list_lower:
                    list_origin.append(value)
                    self._value = PyEnviron.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc_(
                        self._key, value, PyEnviron.OptTypes.Append
                    )
                    self._update_opt_cache_fnc_()
            else:
                self._value = value
                self._update_opt_stack_fnc_(
                    self._key, value, PyEnviron.OptTypes.Set
                )
                self._update_opt_cache_fnc_()

        def _prepend_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() not in list_lower:
                    list_origin.insert(0, value)
                    self._value = PyEnviron.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc_(
                        self._key, value, PyEnviron.OptTypes.Prepend
                    )
                    self._update_opt_cache_fnc_()
            else:
                self._value = value
                self._update_opt_stack_fnc_(
                    self._key, value, PyEnviron.OptTypes.Set
                )
                self._update_opt_cache_fnc_()

        def _remove_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() in list_lower:
                    list_origin.remove(list_origin[list_lower.index(value.lower())])
                    self._value = PyEnviron.PATHSEP.join(list_origin)
                    self._update_opt_stack_fnc_(
                        self._key, value, PyEnviron.OptTypes.Remove
                    )
                    self._update_opt_cache_fnc_()
                    return True
            return False

        def _update_opt_stack_fnc_(self, key, value, opt_type):
            self._environ._opt_stack_update_fnc_(key, value, opt_type)

        def _update_opt_cache_fnc_(self):
            self._environ._opt_cache_set_fnc_(self._key, self._value)

        def _new_fnc_(self):
            environ_value = PyEnviron.PyEnvironValue(self._value)
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
        self._environ_opt_stack = PyEnviron.OPT_STACK
        #
        if isinstance(cache, dict):
            self._environ_opt_cache = cache
        else:
            self._environ_opt_cache = PyEnviron.OPT_CACHE
        #
        if isinstance(variants, dict):
            self._environ_variants = variants
        else:
            self._environ_variants = dict()
    @staticmethod
    def restore_cache():
        PyEnviron.OPT_STACK = []
        PyEnviron.OPT_CACHE = dict()

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
        environ_value = PyEnviron.PyEnvironValue(self._opt_cache_get_fnc_(key))
        environ_value.key = key
        environ_value.parent = self
        #
        self.__dict__[key] = environ_value
        return environ_value.get()

    def _set_fnc_(self, key, value):
        key = key.upper()
        #
        environ_value = PyEnviron.PyEnvironValue(value)
        environ_value.key = key
        environ_value.parent = self
        environ_value.set(value)
        self.__dict__[key] = environ_value

    def has_key(self, key):
        return self._opt_cache_has_key_fnc_(key)

    def has_value(self, key, value):
        value_ = self._opt_cache_get_fnc_(key)
        if value_ is not None:
            _ = [i.lstrip().rstrip() for i in value_.lower().split(PyEnviron.PATHSEP)]
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


class PyEnviron_(PyEnviron):
    def __init__(self):
        super(PyEnviron_, self).__init__(os.environ)

    def accept(self):
        pass


if __name__ == '__main__':
    env = PyEnviron_()
    #
    print env.TEST_A, ',', os.environ.get('TEST_A')
    env.TEST_A = '/a'
    print env.TEST_A, ',', os.environ.get('TEST_A')
    env.TEST_A += '/b'
    print env.TEST_A, ',', os.environ.get('TEST_A')
    env.TEST_A.append('/c')
    print env.TEST_A, ',', os.environ.get('TEST_A')
    env.TEST_A.prepend('/d')
    print env.TEST_A, ',', os.environ.get('TEST_A')
    #
    # env.TEST_B = 'A'
    env.TEST_B += 'A'
    print env.TEST_B, ',', os.environ.get('TEST_B')
    env.TEST_B += 'B', 'C'
    print env.TEST_B, ',', os.environ.get('TEST_B')

    print env.OPT_STACK
