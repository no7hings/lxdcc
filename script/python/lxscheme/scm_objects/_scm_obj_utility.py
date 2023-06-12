# coding:utf-8
from .. import scm_abstract


class Content(scm_abstract.AbsContentDef):
    def __init__(self, key, value):
        self._set_content_def_init_(key, value)

    def get_content(self, key_path, default_value=None):
        key = key_path.split(self.PATHSEP)[-1]
        value = self.get(key_path, default_value)
        return self.__class__(
            key, value
        )

    def _set_content_create_(self, key, value):
        return self.__class__(
            key, value
        )


class FileScheme(scm_abstract.AbsSchemeFileLoader):
    CONTENT_CLS = Content
    def __init__(self, *args):
        super(FileScheme, self).__init__(*args)
