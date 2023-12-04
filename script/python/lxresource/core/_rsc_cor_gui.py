# coding:utf-8
from ..core import _rsc_cor_base


class ResourceIcon(object):
    BRANCH = 'icons'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return _rsc_cor_base.ExtendResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def find_all_keys_at(cls, group_name):
        return _rsc_cor_base.ExtendResource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes={'.png', '.svg'}
        )


class RscFont(object):
    BRANCH = 'fonts'
    ICON_KEY_PATTERN = r'[@](.*?)[@]'

    @classmethod
    def get(cls, key):
        return _rsc_cor_base.ExtendResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def find_all_keys_at(cls, group_name):
        return _rsc_cor_base.ExtendResource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes={'.png', '.svg'}
        )
