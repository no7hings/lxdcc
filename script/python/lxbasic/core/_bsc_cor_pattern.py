# coding:utf-8
from ._bsc_cor_utility import *


class PtnMultiplyFileMtd(object):
    RE_UDIM_KEYS = [
        (r'<udim>', r'{}', 4),
    ]
    #
    RE_SEQUENCE_KEYS = [
        # keyword, re_format, count
        (r'#', r'{}', -1),
        # maya
        (r'<f>', r'{}', 4),
        # katana, etc, "test.(0001-0600)%04d.exr"
        (r'(\()[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](\))(%04d)', r'{}', 4),
        # houdini, etc, "test.$F.exr"
        (r'$F', r'\{}[^\d]', 4),
    ]
    # houdini
    for i in range(4):
        RE_SEQUENCE_KEYS.append(
            (r'$F0{}'.format(i+1), r'\{}', i+1)
        )
    # katana
    for i in range(4):
        RE_SEQUENCE_KEYS.append(
            (r'%0{}d'.format(i+1), r'{}', i+1)
        )
    #
    RE_MULTIPLY_KEYS = RE_UDIM_KEYS + RE_SEQUENCE_KEYS
    PATHSEP = '/'
    @classmethod
    def to_fnmatch_style(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        new_name_base = pattern
        for i_k, i_f, i_c in re_keys:
            i_r = re.finditer(i_f.format(i_k), pattern, re.IGNORECASE) or []
            for j in i_r:
                j_start, j_end = j.span()
                if i_c == -1:
                    s = '[0-9]'
                    new_name_base = new_name_base.replace(pattern[j_start:j_end], s, 1)
                else:
                    s = '[0-9]'*i_c
                    new_name_base = new_name_base.replace(pattern[j_start:j_end], s, 1)
        return new_name_base
    @classmethod
    def to_re_style(cls, pattern):
        pattern_ = pattern
        args = PtnMultiplyFileMtd.get_args(pattern)
        for i, (i_key, i_count) in enumerate(args):
            pattern_ = pattern_.replace(
                i_key, r'[PATTERN-PLACEHOLDER-{}]'.format(i), 1
            )
        #
        re_pattern_ = fnmatch.translate(pattern_)
        for i, (i_key, i_count) in enumerate(args):
            re_pattern_ = re_pattern_.replace(
                r'[PATTERN-PLACEHOLDER-{}]'.format(i),
                r'(\d{{{}}})'.format(i_count)
            )
        return re_pattern_

    @classmethod
    def get_args(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        key_args = []
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), pattern, re.IGNORECASE) or []
            if results:
                if i_c == -1:
                    i_count = len(results)
                    i_key = i_count * i_k
                else:
                    i_count = i_c
                    i_key = i_k
                #
                key_args.append(
                    (i_key, i_count)
                )
        return key_args
    @classmethod
    def get_is_valid(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), pattern, re.IGNORECASE) or []
            if results:
                return True
        return False


class PtnParseMtd(object):
    RE_KEY_PATTERN = r'[{](.*?)[}]'
    @classmethod
    def get_keys(cls, pattern):
        lis_0 = re.findall(re.compile(cls.RE_KEY_PATTERN, re.S), pattern)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1
    @classmethod
    def get_value(cls, key, variants):
        if '.' in key:
            key_ = key.split('.')[0]
            if key_ in variants:
                value_ = variants[key_]
                exec('{} = \'{}\''.format(key_, value_))
                return eval(key)
        if key in variants:
            return variants[key]
    @classmethod
    def set_update(cls, pattern, **kwargs):
        if pattern is not None:
            keys = cls.get_keys(pattern)
            variants = kwargs
            s = pattern
            if keys:
                for i_k in keys:
                    i_v = cls.get_value(i_k, variants)
                    if i_v is not None and i_v != '*':
                        s = s.replace('{{{}}}'.format(i_k), i_v)
            return s
        return pattern
    @classmethod
    def get_as_fnmatch(cls, pattern, variants=None):
        if pattern is not None:
            keys = re.findall(re.compile(cls.RE_KEY_PATTERN, re.S), pattern)
            s = pattern
            if keys:
                for i_k in keys:
                    i_v = '*'
                    if isinstance(variants, dict):
                        if i_k in variants:
                            i_v = variants[i_k]
                    s = s.replace('{{{}}}'.format(i_k), i_v)
            return s
        return pattern


class PtnParseOpt(object):
    def __init__(self, p, key_format=None):
        self._variants = {}
        self._pattern = p

        if isinstance(key_format, dict):
            self._key_format = key_format
        else:
            self._key_format = {}

        self._fnmatch_pattern = PtnParseMtd.get_as_fnmatch(
            self._pattern, self._key_format
        )
    @property
    def pattern(self):
        return self._pattern
    @property
    def fnmatch_pattern(self):
        return self._fnmatch_pattern

    def get_keys(self):
        return PtnParseMtd.get_keys(
            self._pattern
        )
    keys = property(get_keys)

    def get_value(self):
        return self._pattern

    def set_update(self, **kwargs):
        keys = self.get_keys()
        for k, v in kwargs.items():
            if k in keys:
                self._variants[k] = v
        #
        self._pattern = PtnParseMtd.set_update(
            self._pattern, **kwargs
        )
        self._fnmatch_pattern = PtnParseMtd.get_as_fnmatch(
            self._pattern, self._key_format
        )

    def set_update_to(self, **kwargs):
        return self.__class__(
            PtnParseMtd.set_update(
                self._pattern, **kwargs
            )
        )

    def get_matches(self):
        list_ = []
        paths = glob.glob(
            PtnParseMtd.get_as_fnmatch(
                self._pattern, self._key_format
            )
        ) or []
        for i_path in paths:
            i_p = parse.parse(
                self._pattern, i_path
            )
            if i_p:
                i_r = i_p.named
                if i_r:
                    i_r.update(self._variants)
                    i_r['result'] = i_path
                    list_.append(i_r)
        return list_

    def get_variants(self, result):
        i_p = parse.parse(
            self._pattern, result
        )
        if i_p:
            i_r = i_p.named
            if i_r:
                i_r.update(self._variants)
                i_r['result'] = result
                return i_r

    def _get_exists_results_(self):
        return glob.glob(
            self._fnmatch_pattern
        ) or []

    def get_exists_results(self, **kwargs):
        p = self.set_update_to(**kwargs)
        return glob.glob(
            p._fnmatch_pattern
        ) or []

    def set_key_format(self, key, value):
        self._key_format[key] = value

    def __str__(self):
        return self._pattern
