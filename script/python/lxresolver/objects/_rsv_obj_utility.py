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
    RSV_VERSION_CLASS = RsvVersionKey
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


class RsvEntity(rsv_abstract.AbsRsvEntity):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvEntity, self).__init__(*args, **kwargs)


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


class RsvVersion(rsv_abstract.AbsRsvVersion):
    PATHSEP = '/'
    #
    PROPERTIES_CLASS = _bsc_obj_raw.Properties
    def __init__(self, *args, **kwargs):
        super(RsvVersion, self).__init__(*args, **kwargs)


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
    RSV_ENTITY_CLASS = RsvEntity
    RSV_STEP_CLASS = RsvStep
    RSV_TASK_CLASS = RsvTask
    RSV_VERSION_CLASS = RsvVersion
    #
    RSV_UNIT_CLASS = RsvUnit
    def __init__(self, *args, **kwargs):
        super(RsvProject, self).__init__(*args, **kwargs)


class Resolver(rsv_abstract.AbsResolver):
    PATHSEP = '/'
    #
    FILE_PATH = rsv_configure.Data.RESOLVER_BASIC_CONFIGURE_PATH
    #
    OBJ_UNIVERSE_CLASS = core_objects.ObjUniverse
    #
    RSV_PROJECT_STACK_CLASS = _rsv_obj_stack.ProjectStack
    RSV_PROJECT_CLASS = RsvProject
    def __init__(self):
        super(Resolver, self).__init__()


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
