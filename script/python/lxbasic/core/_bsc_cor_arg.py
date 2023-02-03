# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw


class ArgDictStringMtd(object):
    ARGUMENT_SEP = '&'
    @classmethod
    def to_string(cls, **kwargs):
        vars_ = []
        keys = kwargs.keys()
        keys.sort()
        for k in keys:
            v = kwargs[k]
            if isinstance(v, (tuple, list)):
                # must convert to str
                vars_.append('{}={}'.format(k, '+'.join(map(str, v))))
            else:
                vars_.append('{}={}'.format(k, v))
        return cls.ARGUMENT_SEP.join(vars_)


class ArgDictStringOpt(object):
    #  =%20
    # "=%22
    # #=%23
    # %=%25
    # &=%26
    # (=%28
    # )=%29
    # +=%2B
    # ,=%2C
    # /=%2F
    # :=%3A
    # ;=%3B
    # <=%3C
    # ==%3D
    # >=%3E
    # ?=%3F
    # @=%40
    # \=%5C
    # |=%7C
    ARGUMENT_SEP = '&'
    def __init__(self, option, default_option=None):
        dic = collections.OrderedDict()
        if isinstance(default_option, six.string_types):
            self._set_update_by_string_(dic, default_option)
        elif isinstance(default_option, dict):
            dic.update(default_option)

        if isinstance(option, six.string_types):
            self._set_update_by_string_(dic, option)
        elif isinstance(option, dict):
            dic.update(option)
        else:
            raise TypeError()
        #
        self._option_dict = dic
        #
        self._string_dict = {
            'key': self.to_string()
        }
    @classmethod
    def _set_update_by_string_(cls, dic, option_string):
        ks = [i.lstrip().rstrip() for i in option_string.split(cls.ARGUMENT_SEP)]
        for k in ks:
            key, value = k.split('=')
            value = value.lstrip().rstrip()
            #
            value = cls._set_value_convert_by_string_(value)
            dic[key.lstrip().rstrip()] = value
    @classmethod
    def _set_value_convert_by_string_(cls, value_string):
        if isinstance(value_string, six.string_types):
            if value_string in ['None']:
                return None
            elif value_string in ['True', 'False']:
                return eval(value_string)
            elif value_string in ['true', 'false']:
                return [True, False][['true', 'false'].index(value_string)]
            elif value_string in ['()', '[]', '{}']:
                return eval(value_string)
            elif '+' in value_string:
                return value_string.split('+')
            else:
                return value_string

    def get_value(self):
        return self._option_dict
    value = property(get_value)

    def get(self, key, as_array=False, as_integer=False):
        if key in self._option_dict:
            _ = self._option_dict[key]
            if as_integer is True:
                if isinstance(_, int):
                    return _
                elif isinstance(_, float):
                    return int(_)
                elif isinstance(_, six.string_types):
                    if _:
                        if str(_).isdigit():
                            return int(_)
                        elif _bsc_cor_raw.RawTextOpt(_).get_is_float():
                            return int(float(_))
                        return 0
                    return 0
                return 0
            if as_array is True:
                if isinstance(_, (tuple, list)):
                    return _
                if _:
                    return [_]
                return []
            return self._option_dict[key]

    def get_as_path(self, key):
        pass

    def get_as_array(self, key):
        return self.get(key, as_array=True)

    def get_as_boolean(self, key):
        return self.get(key) or False

    def get_as_integer(self, key):
        return self.get(key, as_integer=True)

    def pop(self, key):
        if key in self._option_dict:
            return self._option_dict.pop(
                key
            )

    def get_as(self, key, type_):
        pass

    def set(self, key, value):
        self._option_dict[key] = value

    def set_update(self, dic, override=True):
        if override is False:
            [dic.pop(k) for k in dic if k in self._option_dict]
        #
        self._option_dict.update(dic)

    def set_update_by_string(self, option):
        self._option_dict.update(
            self.__class__(option).get_value()
        )

    def get_key_is_exists(self, key):
        return key in self._option_dict

    def get_raw(self):
        return self._option_dict

    def to_option(self):
        return self.to_string()

    def to_string(self):
        return ArgDictStringMtd.to_string(
            **self._option_dict
        )

    def __str__(self):
        return json.dumps(
            self._option_dict,
            indent=4,
            skipkeys=True,
            sort_keys=True
        )


class ArgListStringOpt(object):
    PATTERN = r'[\[](.*?)[\]]'
    def __init__(self, arguments):
        self._arguments = re.findall(re.compile(self.PATTERN, re.S), arguments) or []

    def get_value(self):
        return self._arguments
    value = property(get_value)
