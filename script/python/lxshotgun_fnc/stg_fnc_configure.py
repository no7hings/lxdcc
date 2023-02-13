# coding:utf-8
import os

from lxscheme.scm_objects import _scm_obj_utility


class Root(object):
    main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    icon = '{}/.icon'.format(main)
    data = '{}/.data'.format(main)


class Scheme(object):
    STEPS = _scm_obj_utility.FileScheme(
        '{}/step_configures.yml'.format(Root.data)
    )
    CHECKER_CONFIGURES = _scm_obj_utility.FileScheme(
        '{}/checker_configures.yml'.format(Root.data)
    )
