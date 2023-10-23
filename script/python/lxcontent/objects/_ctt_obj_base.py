# coding:utf-8
import collections

import lxcontent.abstracts as ctt_abstracts


class Content(ctt_abstracts.AbsContent):
    PATHSEP = '.'

    def __init__(self, key=None, value=None):
        super(Content, self).__init__(key, value)


class Configure(ctt_abstracts.AbsContent):
    PATHSEP = '.'

    def __init__(self, key=None, value=None):
        super(Configure, self).__init__(key, value)


class Dict(ctt_abstracts.AbsContent):
    PATHSEP = '.'

    def __init__(self):
        super(Dict, self).__init__(
            value=collections.OrderedDict()
        )

    def get_content(self, key_path):
        key = key_path.split(self.PATHSEP)[-1]
        value = self.get(key_path)
        if isinstance(value, dict) is True:
            return Content(key, value)


class Property(object):
    def __init__(self, properties, key):
        self._properties = properties
        self._key = key

    @property
    def key(self):
        return self._key

    def get_value(self):
        return self._properties.get(self._key)

    value = property(get_value)

    @value.setter
    def value(self, value):
        self._properties.get(self._key, value)

    def __str__(self):
        return '{} = {}'.format(
            self._key, self.get_value()
        )


class Properties(ctt_abstracts.AbsContent):
    PATHSEP = '.'
    PROPERTY_CLS = Property

    def __init__(self, obj, raw=None):
        self._obj = obj
        #
        if raw is None:
            raw = collections.OrderedDict()
        super(Properties, self).__init__(value=raw)

    def get_property(self, key):
        return self.PROPERTY_CLS(self, key)
