# coding:utf-8
import lxobj.core_objects as core_objects

from lxresolver import rsv_configure, rsv_abstract

from lxresolver.objects import _rsv_obj_stack

from lxbasic.objects import _bsc_obj_raw


class RsvVersionKey(rsv_abstract.AbsRsvVersionKey):
    def __init__(self, *args, **kwargs):
        super(RsvVersionKey, self).__init__(*args, **kwargs)


class RsvPattern(rsv_abstract.AbsRsvPattern):
    def __init__(self, *args, **kwargs):
        super(RsvPattern, self).__init__(*args, **kwargs)


class RsvMatcher(rsv_abstract.AbsRsvMatcher):
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    #
    RSV_PATTERN_CLASS = RsvPattern
    #
    RSV_VERSION_KEY_CLASS = RsvVersionKey
    def __init__(self, *args, **kwargs):
        super(RsvMatcher, self).__init__(*args, **kwargs)


class RsvUnit(rsv_abstract.AbsRsvUnit):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvUnit, self).__init__(*args, **kwargs)


class RsvTag(rsv_abstract.AbsRsvTag):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvTag, self).__init__(*args, **kwargs)


class RsvResource(rsv_abstract.AbsRsvResource):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvResource, self).__init__(*args, **kwargs)


class RsvStep(rsv_abstract.AbsRsvStep):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvStep, self).__init__(*args, **kwargs)


class RsvTask(rsv_abstract.AbsRsvTask):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvTask, self).__init__(*args, **kwargs)


class RsvTaskVersion(rsv_abstract.AbsRsvTaskVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvTaskVersion, self).__init__(*args, **kwargs)


class RsvUnitVersion(rsv_abstract.AbsRsvUnitVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvUnitVersion, self).__init__(*args, **kwargs)


class RsvProject(rsv_abstract.AbsRsvProject):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    #
    RSV_MATCHER_CLASS = RsvMatcher
    RSV_PATTERN_CLASS = RsvPattern
    #
    RSV_OBJ_STACK_CLASS = _rsv_obj_stack.EntityStack
    #
    RSV_TAG_CLASS = RsvTag
    RSV_ENTITY_CLASS = RsvResource
    RSV_STEP_CLASS = RsvStep
    RSV_TASK_CLASS = RsvTask
    RSV_TASK_VERSION_CLASS = RsvTaskVersion
    #
    RSV_UNIT_CLASS = RsvUnit
    RSV_UNIT_VERSION_CLASS = RsvUnitVersion
    def __init__(self, *args, **kwargs):
        super(RsvProject, self).__init__(*args, **kwargs)


class RsvRoot(rsv_abstract.AbsRsvRoot):
    PATHSEP = '/'
    #
    FILE_PATH = rsv_configure.Data.RESOLVER_BASIC_CONFIGURE_PATH
    #
    OBJ_UNIVERSE_CLASS = core_objects.ObjUniverse
    #
    RSV_PROJECT_STACK_CLASS = _rsv_obj_stack.ProjectStack
    RSV_PROJECT_CLASS = RsvProject

    RSV_VERSION_KEY_CLASS = RsvVersionKey
    def __init__(self):
        super(RsvRoot, self).__init__()


if __name__ == '__main__':
    print(
        RsvMatcher._get_match_patterns_(
            '{project}/{role}/{step}/{task}',
            dict(
                project='lib',
                role=['sdr', 'gmt'],
                step=['mod', 'srf'],
                test=['a', 'b', 'c']
            )
        )
    )
