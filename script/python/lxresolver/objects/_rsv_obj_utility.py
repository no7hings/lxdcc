# coding:utf-8
import lxuniverse.objects as unv_objects

import lxresolver.abstracts as rsv_abstracts

from lxresolver.objects import _rsv_obj_stack, _rsv_obj_launcher

from lxbasic.objects import _bsc_obj_raw


class RsvVersionKey(rsv_abstracts.AbsRsvVersionKey):
    def __init__(self, *args, **kwargs):
        super(RsvVersionKey, self).__init__(*args, **kwargs)


class RsvMatchPattern(rsv_abstracts.AbsRsvPattern):
    def __init__(self, *args, **kwargs):
        super(RsvMatchPattern, self).__init__(*args, **kwargs)


class RsvMatcher(rsv_abstracts.AbsRsvMatcher):
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    #
    RSV_MATCH_PATTERN_CLASS = RsvMatchPattern
    #
    RSV_VERSION_KEY_CLASS = RsvVersionKey
    def __init__(self, *args, **kwargs):
        super(RsvMatcher, self).__init__(*args, **kwargs)


class RsvUnit(rsv_abstracts.AbsRsvUnit):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvUnit, self).__init__(*args, **kwargs)


class RsvTag(rsv_abstracts.AbsRsvTag):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvTag, self).__init__(*args, **kwargs)


class RsvResource(rsv_abstracts.AbsRsvResource):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvResource, self).__init__(*args, **kwargs)


class RsvStep(rsv_abstracts.AbsRsvStep):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvStep, self).__init__(*args, **kwargs)


class RsvTask(rsv_abstracts.AbsRsvTask):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvTask, self).__init__(*args, **kwargs)


class RsvTaskVersion(rsv_abstracts.AbsRsvTaskVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvTaskVersion, self).__init__(*args, **kwargs)


class RsvUnitVersion(rsv_abstracts.AbsRsvUnitVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvUnitVersion, self).__init__(*args, **kwargs)


class RsvProject(rsv_abstracts.AbsRsvProject):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    #
    RSV_MATCHER_CLASS = RsvMatcher
    RSV_MATCH_PATTERN_CLASS = RsvMatchPattern
    #
    RSV_OBJ_STACK_CLASS = _rsv_obj_stack.EntityStack
    #
    RSV_TAG_CLASS = RsvTag
    RSV_RESOURCE_CLASS = RsvResource
    RSV_STEP_CLASS = RsvStep
    RSV_TASK_CLASS = RsvTask
    RSV_TASK_VERSION_CLASS = RsvTaskVersion
    #
    RSV_UNIT_CLASS = RsvUnit
    RSV_UNIT_VERSION_CLASS = RsvUnitVersion
    #
    RSV_APP_DEFAULT_CLASS = _rsv_obj_launcher.RsvAppDefault
    RSV_APP_NEW_CLASS = _rsv_obj_launcher.RsvAppNew
    def __init__(self, *args, **kwargs):
        super(RsvProject, self).__init__(*args, **kwargs)


class RsvRoot(rsv_abstracts.AbsRsvRoot):
    PATHSEP = '/'
    #
    OBJ_UNIVERSE_CLASS = unv_objects.ObjUniverse
    #
    RSV_PROJECT_STACK_CLASS = _rsv_obj_stack.ProjectStack
    RSV_PROJECT_CLASS = RsvProject

    RSV_VERSION_KEY_CLASS = RsvVersionKey
    def __init__(self):
        super(RsvRoot, self).__init__()


if __name__ == '__main__':
    pass
