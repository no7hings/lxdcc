# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw


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
        # katana, etc. "test.(0001-0600)%04d.exr"
        (r'(\()[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](\))(%04d)', r'{}', 4),
        # houdini, etc. "test.$F.exr"
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
    RE_MULTIPLY_KEYS = RE_UDIM_KEYS+RE_SEQUENCE_KEYS
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
                    i_key = i_count*i_k
                else:
                    i_count = i_c
                    i_key = i_k
                #
                key_args.append(
                    (i_key, i_count)
                )
        return key_args
    @classmethod
    def get_is_valid(cls, p):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), p, re.IGNORECASE) or []
            if results:
                return True
        return False


class PtnVersion(object):
    VERSION_ZFILL_COUNT = 3
    PATTERN = 'v{}'.format('[0-9]'*VERSION_ZFILL_COUNT)

    def __init__(self, text):
        self._validation_(text)
        #
        self._text = text
        self._number = int(text[-self.VERSION_ZFILL_COUNT:])

    @classmethod
    def _validation_(cls, text):
        if not fnmatch.filter([text], cls.PATTERN):
            raise TypeError(
                'version: "{}" is Non-match "{}"'.format(text, cls.PATTERN)
            )

    @classmethod
    def get_is_valid(cls, text):
        return not not fnmatch.filter([text], cls.PATTERN)

    def get_number(self):
        return self._number

    number = property(get_number)

    @classmethod
    def get_default(cls):
        return 'v{}'.format(str(1).zfill(cls.VERSION_ZFILL_COUNT))

    def __str__(self):
        return self._text

    def __iadd__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        self._number += int(other)
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self

    def __isub__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        if self._number >= other:
            self._number -= int(other)
        else:
            self._number = 0
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self


class PtnParseMtd(object):
    RE_KEY_PATTERN = r'[{](.*?)[}]'

    @classmethod
    def get_keys(cls, p):
        lis_0 = re.findall(re.compile(cls.RE_KEY_PATTERN, re.S), p)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1

    @classmethod
    def get_value(cls, key, variants):
        if '.' in key:
            key_ = key.split('.')[0]
            if key_ in variants:
                value_ = variants[key_]
                exec ('{} = \'{}\''.format(key_, value_))
                return eval(key)
        if key in variants:
            return variants[key]

    @classmethod
    def set_update(cls, p, **kwargs):
        if p is not None:
            keys = cls.get_keys(p)
            variants = kwargs
            s = p
            if keys:
                for i_k in keys:
                    i_v = cls.get_value(i_k, variants)
                    if i_v is not None and i_v != '*':
                        s = s.replace('{{{}}}'.format(i_k), i_v)
            return s
        return p

    @classmethod
    def get_as_fnmatch(cls, p, variants=None):
        if p is not None:
            keys = re.findall(re.compile(cls.RE_KEY_PATTERN, re.S), p)
            s = p
            if keys:
                for i_k in keys:
                    i_v = '*'
                    if isinstance(variants, dict):
                        if i_k in variants:
                            i_v = variants[i_k]
                    s = s.replace('{{{}}}'.format(i_k), i_v)
            return s
        return p


class PtnFnmatch(object):
    CACHE = dict()
    CACHE_MAX = 100
    @classmethod
    def to_re_style(cls, pat):
        i, n = 0, len(pat)
        res = ''
        while i < n:
            c = pat[i]
            i += 1
            if c == '*':
                res += '.*'
            elif c == '?':
                res += '.'
            elif c == '[':
                j = i
                if j < n and pat[j] == '!':
                    j += 1
                if j < n and pat[j] == ']':
                    j += 1
                while j < n and pat[j] != ']':
                    j += 1
                if j >= n:
                    res += '\\['
                else:
                    stuff = pat[i:j].replace('\\', '\\\\')
                    i = j+1
                    if stuff[0] == '!':
                        stuff = '^'+stuff[1:]
                    elif stuff[0] == '^':
                        stuff = '\\'+stuff
                    res = '%s[%s]'%(res, stuff)
            else:
                res = res+re.escape(c)
        return res
    @classmethod
    def get_is_valid(cls, ptn):
        return ptn != cls.to_re_style(ptn)
    @classmethod
    def filter(cls, texts, p):
        list_ = []
        try:
            re_pat = cls.CACHE[p]
        except KeyError:
            res = fnmatch.translate(p)
            if len(cls.CACHE) >= cls.CACHE_MAX:
                cls.CACHE.clear()
            cls.CACHE[p] = re_pat = re.compile(res, re.IGNORECASE)
        #
        match = re_pat.match
        for i_text in texts:
            if match(i_text):
                list_.append(i_text)
        return list_


class PtnParseOpt(object):
    def __init__(self, p, key_format=None):
        self._pattern_origin = p
        self._variants = {}
        self._pattern = p

        self._key_format = key_format or {}

        self._fnmatch_pattern_origin = PtnParseMtd.get_as_fnmatch(
            self._pattern_origin, self._key_format
        )
        self._fnmatch_pattern = PtnParseMtd.get_as_fnmatch(
            self._pattern, self._key_format
        )
    def get_pattern(self):
        return self._pattern
    pattern = property(get_pattern)

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

    def get_matches(self, sort=False):
        list_ = []
        paths = glob.glob(
            PtnParseMtd.get_as_fnmatch(
                self._pattern, self._key_format
            )
        ) or []
        if sort is True:
            paths = _bsc_cor_raw.RawTextsOpt(paths).sort_by_number()
        #
        if self.get_keys():
            for i_path in paths:
                i_p = parse.parse(
                    self._pattern, i_path, case_sensitive=True
                )
                if i_p:
                    i_r = i_p.named
                    if i_r:
                        i_r.update(self._variants)
                        i_r['result'] = i_path
                        i_r['pattern'] = self._pattern_origin
                        list_.append(i_r)
        else:
            for i_path in paths:
                i_r = dict(result=i_path)
                i_r.update(self._variants)
                list_.append(i_r)
        return list_

    def get_is_matched(self, result):
        return not not fnmatch.filter(
            [result], self._fnmatch_pattern
        )

    def get_variants(self, result):
        i_p = parse.parse(
            self._pattern, result, case_sensitive=True
        )
        if i_p:
            i_r = i_p.named
            if i_r:
                i_r.update(self._variants)
                i_r['result'] = result
                return i_r
        return self._variants

    def _get_exists_results_(self):
        return glob.glob(
            self._fnmatch_pattern
        ) or []

    def get_exists_results(self, **kwargs):
        p = self.set_update_to(**kwargs)
        return glob.glob(
            p._fnmatch_pattern
        ) or []

    def get_match_results(self, sort=False):
        paths = glob.glob(
            PtnParseMtd.get_as_fnmatch(
                self._pattern, self._key_format
            )
        ) or []
        if sort is True:
            paths = _bsc_cor_raw.RawTextsOpt(paths).sort_by_number()
        return paths

    def set_key_format(self, key, value):
        self._key_format[key] = value

    def get_latest_version(self, version_key):
        ms = self.get_matches(sort=True)
        if ms:
            l_m = ms[-1]
            return l_m[version_key]
        return PtnVersion.get_default()

    def get_new_version(self, version_key):
        ms = self.get_matches(sort=True)
        if ms:
            l_m = ms[-1]
            l_v = l_m[version_key]
            l_v_p = PtnVersion(l_v)
            l_v_p += 1
            return str(l_v_p)
        return PtnVersion.get_default()

    def __str__(self):
        return self._pattern
