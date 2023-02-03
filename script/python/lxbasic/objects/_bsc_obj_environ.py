# coding:utf-8
import os


class Environ(object):
    PATHSEP = os.pathsep
    CACHE = {}

    class Element(str):
        def __init__(self, value):
            self._value = value
            self._key = ''
            self._parent = None

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
                [i.lstrip().rstrip() for i in self._value.split(Environ.PATHSEP)],
                [i.lstrip().rstrip() for i in self._value.lower().split(Environ.PATHSEP)]
            )

        def _set_fnc_(self, value):
            self._value = value
            self._raw_update_fnc_()

        def _append_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() not in list_lower:
                    list_origin.append(value)
                    self._value = Environ.PATHSEP.join(list_origin)
                    self._raw_update_fnc_()
            else:
                self._value = value
                self._raw_update_fnc_()

        def _prepend_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() not in list_lower:
                    list_origin.insert(0, value)
                    self._value = Environ.PATHSEP.join(list_origin)
                    self._raw_update_fnc_()
            else:
                self._value = value
                self._raw_update_fnc_()

        def _remove_fnc_(self, value):
            if self._value:
                list_origin, list_lower = self._get_args_()
                if value.lower() in list_lower:
                    list_origin.remove(list_origin[list_lower.index(value.lower())])
                    self._value = Environ.PATHSEP.join(list_origin)
                    self._raw_update_fnc_()
                    return True
            return False

        def _raw_update_fnc_(self):
            self._parent._env_set_fnc_(self._key, self._value)

        def _new_fnc_(self):
            value_op = Environ.Element(self._value)
            value_op.key = self._key
            value_op.parent = self._parent

            self.parent.__dict__[self._key] = value_op
            return value_op

        def _eq_fnc_(self, value):
            return self._value == value
        @property
        def parent(self):
            return self._parent
        @parent.setter
        def parent(self, parent):
            self._parent = parent
        @property
        def key(self):
            return self._key
        @key.setter
        def key(self, key):
            self._key = key

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

    def __init__(self, raw=None):
        pass
    # env.TEST
    def __getattr__(self, key):
        return self._get_fnc_(key)
    # env.TEST = 'test'
    def __setattr__(self, key, value):
        self._set_fnc_(key, value)

    def _env_set_fnc_(self, key, value):
        os.environ[key] = value

    def _get_fnc_(self, key):
        key = key.upper()
        #
        value_op = Environ.Element(os.environ.get(key, ''))
        value_op.key = key
        value_op.parent = self
        #
        self.__dict__[key] = value_op
        return value_op

    def _set_fnc_(self, key, value):
        key = key.upper()
        #
        value_op = Environ.Element(value)
        value_op.key = key
        value_op.parent = self
        #
        self._env_set_fnc_(key, value)
        self.__dict__[key] = value_op
    @classmethod
    def has_key(cls, key):
        return os.environ.get(key) is not None
    @classmethod
    def has_value(cls, key, value):
        value_ = os.environ.get(key)
        if value_ is not None:
            _ = [i.lstrip().rstrip() for i in value_.lower().split(Environ.PATHSEP)]
            return value.lower() in _
        return False

    def __str__(self):
        list_ = []
        for k, v in os.environ.items():
            list_.append('{} = {}'.format(k, v))
        list_.sort()
        return '\r\n'.join(list_)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    env = Environ()
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
