# coding:utf-8
import os

import enum

from lxutil import utl_configure


class Util(object):
    CONFIGURE = utl_configure.MainData.get_as_configure('deadline/main')
    #
    HOST = CONFIGURE.get('connection.host')
    PORT = CONFIGURE.get('connection.port')


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_ROOT = '{}/.data'.format(ROOT)
    #
    JOB_CONFIGURE_FILE = '{}/job-configure.yml'.format(DATA_ROOT)
    #
    METHOD_CONFIGURE_FILE = '{}/method-configure.yml'.format(DATA_ROOT)
    RSV_TASK_METHOD_CONFIGURE_FILE = '{}/rsv-task-method-configure.yml'.format(DATA_ROOT)
    #
    TASKS_JOB_CONFIGURE_PATH = '{}/tasks-job-configure.yml'.format(DATA_ROOT)


class JobStatus(enum.IntEnum):
    """
    Stat (Status)
    0 = Unknown
    1 = Active
    2 = Suspended
    3 = Completed
    4 = Failed
    6 = Pending
    """
    Unknown = 0
    Active = 1
    Suspended = 2
    Completed = 3
    Failed = 4
    Pending = 6


class TaskStatus(enum.IntEnum):
    """
    Stat (Status)
    1 = Unknown
    2 = Queued
    3 = Suspended
    4 = Rendering
    5 = Completed
    6 = Failed
    8 = Pending
    """
    Unknown = 1
    Queued = 2
    Suspended = 3
    Rendering = 4
    Completed = 5
    Failed = 6
    Pending = 8


class OnTaskTimeout(object):
    """
    Timeout (OnTaskTimeout)
    0 = Both
    1 = Error
    2 = Notify
    """
    KEY = 'Timeout'


class OnJobComplete(object):
    """
    OnComp (OnJobComplete)
    0 = Archive
    1 = Delete
    2 = Nothing
    """
    KEY = 'OnComp'


class ScheduledType(object):
    """
    Schd (ScheduledType)
    0 = None
    1 = Once
    2 = Daily
    """
    KEY = 'Schd'


if __name__ == '__main__':
    print JobStatus.Unknown
