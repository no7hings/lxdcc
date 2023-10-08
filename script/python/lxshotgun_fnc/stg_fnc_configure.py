# coding:utf-8
import os

import lxcontent.objects as ctt_objects


class Root(object):
    main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    icon = '{}/.icon'.format(main)
    data = '{}/.data'.format(main)


class Scheme(object):
    STEPS = ctt_objects.Configure(
        value='{}/step_configures.yml'.format(Root.data)
    )
    CHECKER_CONFIGURES = ctt_objects.Configure(
        value='{}/checker_configures.yml'.format(Root.data)
    )
