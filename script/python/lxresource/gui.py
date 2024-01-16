# coding:utf-8
# resource
from . import base as rsc_cor_base


class RscExtendIcon(object):
    BRANCH = 'icons'

    @classmethod
    def get(cls, key, file_format=None):
        if file_format is not None:
            result = rsc_cor_base.StudioResource.get(
                '{}/{}.{}'.format(cls.BRANCH, key, file_format)
            )
            if result is not None:
                return result
        return rsc_cor_base.ExtendResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def find_all_keys_at(cls, group_name, ext_includes=None):
        return rsc_cor_base.ExtendResource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes=ext_includes or {'.png', '.svg'}
        )


class RscExtendFont(object):
    BRANCH = 'fonts'

    @classmethod
    def get(cls, key):
        return rsc_cor_base.ExtendResource.get(
            '{}/{}.*'.format(cls.BRANCH, key)
        )

    @classmethod
    def find_all_keys_at(cls, group_name):
        return rsc_cor_base.ExtendResource.find_all_file_keys_at(
            cls.BRANCH, group_name, ext_includes={'.png', '.svg'}
        )
