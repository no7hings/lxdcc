# coding:utf-8
import os

import collections

import fnmatch

import parse

import re

import glob

import platform

import lxbasic.core as bsc_core
import six


class RsvConfigure(object):
    MainKeys = [
        'builtin',
        'variant',
        'main',
        'framework',
        'project',
        'storage',
        'dcc'
    ]
    MainSchemes = [
        'default',
        'new'
    ]

    @classmethod
    def get_raw(cls, scheme):
        raw = collections.OrderedDict()
        for i_key in cls.MainKeys:
            i_file = bsc_core.ResourceContent.get_yaml('resolver/{}/{}'.format(scheme, i_key))
            if i_file is not None:
                i_raw = bsc_core.StgFileOpt(i_file).set_read() or {}
                raw.update(i_raw)
        return raw

    @classmethod
    def get_basic_raw(cls):
        return cls.get_raw('basic')

    @classmethod
    def get_all_default_raws(cls):
        list_ = []
        for i_scheme in cls.MainSchemes:
            i_raw = cls.get_raw(i_scheme)
            list_.append(i_raw)
        return list_


class RsvUtil(object):

    URL_PATTERN = 'url://resolver?{parameters}'

    @classmethod
    def _get_parameter_by_url_(cls, url):
        dic = {}
        p = parse.parse(
            cls.URL_PATTERN, url, case_sensitive=True
        )
        if p:
            parameters = p['parameters']
            results = parameters.split('&')
            for result in results:
                if result:
                    key, value = result.split('=')
                    dic[key] = value
            if 'file' in dic:
                k = dic['file']
                keyword = '{}-file'.format(k)
                dic['keyword'] = keyword
        else:
            raise TypeError(u'url: "{}" is Non-available')
        return dic


if __name__ == '__main__':
    print RsvConfigure.get_basic_raw()
