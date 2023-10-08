# coding:utf-8
from Deadline import DeadlineConnect

from lxbasic import bsc_configure, bsc_core

import lxcontent.objects as ctt_objects

from lxutil import utl_configure, utl_core

from lxdeadline import ddl_configure, ddl_core

from lxdeadline.objects import ddl_obj_abs

import threading

import json

THREAD_MAXIMUM = threading.Semaphore(1024)

CON = DeadlineConnect.DeadlineCon(
    ddl_configure.Util.HOST, ddl_configure.Util.PORT
)


class DdlContent(object):
    def __init__(self, obj, index, raw):
        self._obj = obj
        self._index = index
        self._raw = raw

    @property
    def index(self):
        return self._index

    @property
    def raw(self):
        return self._raw

    def get_stouts(self):
        return ddl_core.DdlContentRaw(self._raw).get_stouts()

    def __str__(self):
        return '{}(id="{}", index={})'.format(
            self.__class__.__name__,
            self._obj.id, self._index
        )


class AbsDdlObj(object):
    DDL_PROPERTIES_CLS = None
    DDL_PROPERTY_CLS = None
    #
    DDL_CONTENT_CLS = None

    def __init__(self, raw):
        self._ddl_properties = self.DDL_PROPERTIES_CLS(self, raw)

    @property
    def properties(self):
        return self._ddl_properties

    def get_property(self, key):
        value = self._ddl_properties.get(key)
        return self.DDL_PROPERTY_CLS(key, value)


class DdlLogQuery(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_objects.Properties
    DDL_PROPERTY_CLS = ctt_objects.Property

    def __init__(self, obj, index, raw):
        self._obj = obj
        self._index = index
        super(DdlLogQuery, self).__init__(raw)

    @property
    def index(self):
        return self._index

    def __str__(self):
        return '{}(id="{}", index={})'.format(
            self.__class__.__name__,
            self._obj.id, self._index
        )


class DdlTaskQuery(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_objects.Properties
    DDL_PROPERTY_CLS = ctt_objects.Property
    #
    DDL_CONTENT_CLS = DdlContent
    DDL_LOG_CLS = DdlLogQuery

    def __init__(self, job, index, raw):
        self._job = job
        self._job_id = job.id
        self._task_index = index
        self._task_id = '{}_{}'.format(self._job.id, self._task_index)
        super(DdlTaskQuery, self).__init__(raw)

    @property
    def index(self):
        return self._task_index

    @property
    def job(self):
        return self._job

    @property
    def id(self):
        return self._task_id

    def get_contents(self):
        lis = []
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/taskreports?JobID={}&TaskID={}&Data=allcontents".format(self._job_id, self._task_index)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_CONTENT_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def get_logs(self):
        lis = []
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/taskreports?JobID={}&TaskID={}&Data=log".format(self._job.id, self._task_index)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_LOG_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def set_requeue(self):
        return CON.Tasks.connectionProperties.__put__(
            "/api/tasks", json.dumps({"Command": "requeue", "JobID": self.job.id, "TaskList": [self._task_index]})
        )

    def get_status(self):
        return self.get('Stat')

    def get_progress(self):
        return self.get('Prog')

    def get(self, key):
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/tasks?JobID={}&TaskID={}".format(self._job_id, self._task_index)
        )
        if not _:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        return _[key]

    def __str__(self):
        return '{}(id={})'.format(
            self.__class__.__name__,
            self.id
        )

    def __repr__(self):
        return self.__str__()


class DdlJobQuery(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_objects.Properties
    DDL_PROPERTY_CLS = ctt_objects.Property
    #
    DDL_CONTENT_CLS = DdlContent
    DDL_LOG_CLS = DdlLogQuery
    #
    TASK_CLS = DdlTaskQuery

    def __init__(self, job_id):
        self._job_id = job_id
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/jobs?JobID={}".format(job_id)
        )
        if not _:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        #
        super(DdlJobQuery, self).__init__(_[0])

    def get_id(self):
        return self._job_id

    id = property(get_id)

    def get_tasks(self, task_indices=None):
        lis = []
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/tasks?JobID={}".format(self._job_id)
        )
        #
        if isinstance(_, dict) is False:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        #
        tasks_raw = _['Tasks']
        for task_index, task_raw in enumerate(tasks_raw):
            ddl_task = self.TASK_CLS(self, task_index, task_raw)
            lis.append(ddl_task)
        return lis

    def get_contents(self):
        lis = []
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/jobreports?JobID={}&Data=allcontents".format(self._job_id)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_CONTENT_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def get_logs(self):
        lis = []
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/jobreports?JobID={}&Data=log".format(self._job_id)
        )
        raws = _
        if raws:
            for id_, raw in enumerate(raws):
                obj = self.DDL_CONTENT_CLS(self, id_, raw)
                lis.append(obj)
        return lis

    def get_status(self):
        return self.get('Stat')

    def get_name(self):
        return self.properties.get('Props.Name')

    def get(self, key):
        _ = CON.Tasks.connectionProperties.__get__(
            "/api/jobs?JobID={}".format(self._job_id)
        )
        if not _:
            raise RuntimeError('ddl-task-id:="{}" is Non-exists'.format(self._job_id))
        return _[0][key]

    def set_requeue(self, task_indices=None):
        return [i.set_requeue() for i in self.get_tasks(task_indices)]

    def __str__(self):
        return '{}(id="{}")'.format(
            self.__class__.__name__,
            self.id
        )

    def __repr__(self):
        return self.__str__()


class DdlJobSender(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_objects.Properties
    DDL_PROPERTY_CLS = ctt_objects.Property
    #
    DDL_CONTENT_CLS = DdlContent
    #
    CONFIGURE_FILE_PATH = ddl_configure.Data.JOB_CONFIGURE_FILE

    def __init__(self):
        self._configure = ctt_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        super(DdlJobSender, self).__init__(self._configure.value)
        #
        self._option = self.properties.get_content('option')
        #
        self._info = self.properties.get_content('job.info')
        self._plug = self.properties.get_content('job.plug')
        #
        self._result = None

    @property
    def configure(self):
        return self._configure

    @property
    def option(self):
        return self._option

    @property
    def info(self):
        return self._info

    @property
    def plug(self):
        return self._plug

    def set_info_extra(self, raw):
        if isinstance(raw, dict):
            content = ctt_objects.Content(value=raw)
            for seq, k in enumerate(content._get_leaf_keys_()):
                self.info.set(
                    'ExtraInfoKeyValue{}'.format(seq),
                    '{}={}'.format(k, content.get(k))
                )

    def set_option(self, raw):
        if isinstance(raw, dict):
            for k in self.option.value:
                if k in raw:
                    self.option.set(k, raw[k])

    def set_submit(self):
        self._configure.set_flatten()
        return self._set_ddl_submit_()

    def _set_ddl_submit_(self):
        self._result = CON.Jobs.SubmitJob(self.info.value, self.plug.value)
        return self._result

    def get_is_submit(self):
        return self.get_id() is not None

    def get_group_name(self):
        return self.info.get('BatchName')

    def get_name(self):
        return self.info.get('Name')

    def get_result(self):
        return self._result

    def get_id(self):
        _ = self.get_result()
        if isinstance(_, dict):
            if '_task_id' in _:
                return _['_id']


class AbsDdlJobSender(AbsDdlObj):
    DDL_PROPERTIES_CLS = ctt_objects.Properties
    DDL_PROPERTY_CLS = ctt_objects.Property
    #
    DDL_CONTENT_CLS = DdlContent
    #
    CONFIGURE_FILE_PATH = None

    def __init__(self):
        super(AbsDdlJobSender, self).__init__(
            ctt_objects.Configure(value=self.CONFIGURE_FILE_PATH).value
        )
        #
        self._method = self.properties.get_content('method')
        #
        self._job_info = self.properties.get_content('job.info')
        self._job_plug = self.properties.get_content('job.plug')
        #
        self._result = None

    def get_method(self):
        return self._method

    method = property(get_method)

    def set_method(self, **kwargs):
        for k in self.properties.get('method'):
            if k in kwargs:
                self.properties.set(
                    'method.{}'.format(k),
                    kwargs[k]
                )

    def set_method_extra(self, **kwargs):
        for k in self.properties.get('method.extra'):
            if k in kwargs:
                self.properties.set(
                    'method.extra.{}'.format(k),
                    kwargs[k]
                )

    def get_job_info(self):
        return self._job_info

    job_info = property(get_job_info)

    @property
    def job_plug(self):
        return self._job_plug

    def set_job_info_extra(self, raw):
        if isinstance(raw, dict):
            content = ctt_objects.Content(value=raw)
            for seq, k in enumerate(content._get_leaf_keys_()):
                self.job_info.set(
                    'ExtraInfoKeyValue{}'.format(seq),
                    '{}={}'.format(k, content.get(k))
                )

    @utl_core.Modifier.time_trace
    def set_job_submit(self):
        self.properties.set_flatten()
        info = self.job_info.value
        plug = self.job_plug.value
        return self._set_job_submit_(info, plug)

    @utl_core.Modifier.time_trace
    def _set_job_submit_(self, info, plug):
        self._result = CON.Jobs.SubmitJob(info, plug)
        return self._result

    def get_job_is_submit(self):
        return self.get_job_id() is not None

    def get_job_group_name(self):
        return self.job_info.get('BatchName')

    def get_job_name(self):
        return self.job_info.get('Name')

    def get_job_result(self):
        return self._result

    def get_job_id(self):
        _ = self.get_job_result()
        if isinstance(_, dict):
            if '_id' in _:
                return _['_id']


# use for method
class DdlMethodJobSender(AbsDdlJobSender):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('deadline/method')

    def __init__(self, **kwargs):
        super(DdlMethodJobSender, self).__init__()
        self._ddl_method_cache_opt = ddl_core.DdlMethodCacheOpt(**kwargs)

    def get_cache_opt(self):
        return self._ddl_method_cache_opt


# use for rsv-task-method
class DdlRsvTaskMethodJobSender(DdlMethodJobSender):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('deadline/rsv-task-method')

    def __init__(self, **kwargs):
        super(DdlRsvTaskMethodJobSender, self).__init__(**kwargs)


class DdlRsvTaskRenderJobSender(DdlMethodJobSender):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file('deadline/rsv-task-render')

    def __init__(self, **kwargs):
        super(DdlRsvTaskRenderJobSender, self).__init__(**kwargs)


class Signal(object):
    def __init__(self, *args, **kwargs):
        pass


class SignalThread(threading.Thread):
    def __init__(self, target, args, kwargs):
        threading.Thread.__init__(self)
        self._fnc = target
        self._args = args
        self._kwargs = kwargs

    #
    def run(self):
        THREAD_MAXIMUM.acquire()
        self._fnc(*self._args, **self._kwargs)
        THREAD_MAXIMUM.release()


class SignalInstance(object):
    def __init__(self, *args, **kwargs):
        self._fncs = []
        self.__is_active = True

    def set_cancel(self):
        self.__is_active = False

    def connect_to(self, method):
        self._fncs.append(method)

    def send_emit(self, *args, **kwargs):
        if self.__is_active is True:
            if self._fncs:
                ts = [SignalThread(target=i_method, args=args, kwargs=kwargs) for i_method in self._fncs]
                for t in ts:
                    t.start()
                for t in ts:
                    t.join()


class DdlJobProcess(object):
    Status = bsc_configure.Status
    #
    TASK_STATUS = [
        Status.Unknown,
        Status.Unknown,
        Status.Waiting,
        Status.Suspended,
        Status.Running,
        Status.Completed,
        Status.Failed,
        Status.Unknown,
        Status.Waiting
    ]

    #
    def __init__(self, job_id):
        self._job_query = DdlJobQuery(job_id)
        self._job_id = self._job_query.get_id()
        self._job_name = self._job_query.get_name()
        self._task_queries = self._job_query.get_tasks()
        #
        self._time_interval = 1
        self._processing_time_cost = 0
        self._running_time_cost = 0
        self._waiting_time_cost = 0
        self._processing_time_maximum = 3600
        self._running_time_maximum = 3600
        self._waiting_time_maximum = 3600
        #
        self._is_disable = True
        #
        self._timer = None
        self._status = self.Status.Stopped
        self._sub_process_statuses = [self.Status.Stopped]*len(self._task_queries)
        #
        self.logging = SignalInstance(str)
        self.status_changed = SignalInstance(int)
        self.element_statuses_changed = SignalInstance(int)
        self.started = SignalInstance()
        self.waiting = SignalInstance(int)
        self.running = SignalInstance(int)
        self.processing = SignalInstance(int)
        self.suspended = SignalInstance()
        self.completed = SignalInstance()
        self.failed = SignalInstance()
        self.stopped = SignalInstance()
        self.error_occurred = SignalInstance(int)
        #
        self._status_update_methods = [
            # Unknown = 0
            self.__set_stopped_,
            # Active = 1
            self.__set_running_,
            # Suspended = 2
            self.__set_suspended_,
            # Completed = 3
            self.__set_completed_,
            # Failed = 4
            self.__set_failed_,
            # ?=5
            self.__set_stopped_,
            # Pending = 6
            self.__set_waiting_
        ]

    #
    def __set_status_update_method_run_(self):
        return self._status_update_methods[self._job_query.get_status()]()

    #
    def __set_started_(self):
        self._is_disable = False
        #
        self._status = self.Status.Started
        #
        self.__set_emit_send_(self.started)
        #
        self.__set_processing_time_update_()
        #
        self.__set_logging_(
            'ddl-job-id="{}", ddl-job-name="{}" is started'.format(
                self._job_id, self._job_name
            )
        )

    #
    def __set_emit_send_(self, signal, *args, **kwargs):
        # noinspection PyBroadException
        # signal.send_emit(*args, **kwargs)
        try:
            signal.send_emit(*args, **kwargs)
        except:
            self.__set_error_occurred_()
            raise

    # waiting
    def __set_waiting_(self):
        self._status = self.Status.Waiting
        #
        self.__set_emit_send_(self.waiting, self._waiting_time_cost)
        self.__set_emit_send_(self.processing, self._processing_time_cost)
        #
        self.__set_processing_time_update_()
        self.__set_waiting_time_update_()

    # running
    def __set_running_(self):
        self._status = self.Status.Running
        #
        self.__set_emit_send_(self.running, self._running_time_cost)
        self.__set_emit_send_(self.processing, self._processing_time_cost)
        #
        self.__set_processing_time_update_()
        self.__set_running_time_update_()

    #
    def __set_elements_running_(self):
        pre_element_status = str(self._sub_process_statuses)
        for index, i_task_query in enumerate(self._task_queries):
            i_task_status = self.TASK_STATUS[i_task_query.get_status()]
            if i_task_status is self.Status.Error:
                pass
            self._sub_process_statuses[index] = i_task_status
        if pre_element_status != str(self._sub_process_statuses):
            self.__set_element_statuses_changed_()

    #
    def __set_logging_(self, text):
        print text
        self.__set_emit_send_(self.logging, text)

    # status changed
    def __set_status_changed_(self):
        self.__set_emit_send_(self.status_changed, self._status)

    def __set_element_statuses_changed_(self):
        self.__set_emit_send_(self.element_statuses_changed, self._sub_process_statuses)

    def __set_suspended_(self):
        self._status = self.Status.Suspended
        #
        self.__set_emit_send_(self.suspended)
        #
        self.__set_logging_(
            'ddl-job-id="{}", ddl-job-name="{}" is suspended'.format(
                self._job_id, self._job_name
            )
        )

    def __set_completed_(self):
        self._status = self.Status.Completed
        #
        self.__set_emit_send_(self.completed)
        #
        self.__set_logging_(
            'ddl-job-id="{}", ddl-job-name="{}" is completed'.format(
                self._job_id, self._job_name
            )
        )

    def __set_failed_(self):
        self._is_disable = True
        #
        self._status = self.Status.Failed
        #
        self.__set_emit_send_(self.failed)
        #
        self.__set_logging_(
            'ddl-job-id="{}", ddl-job-name="{}" is failed'.format(
                self._job_id, self._job_name
            )
        )

    def __set_stopped_(self):
        self._is_disable = True
        #
        self._status = self.Status.Stopped
        self._sub_process_statuses = [self.Status.Stopped]*len(self._task_queries)
        #
        self.__set_emit_send_(self.stopped)
        #
        self.__set_logging_(
            'ddl-job-id="{}", ddl-job-name="{}" is stopped'.format(
                self._job_id, self._job_name
            )
        )

    #
    def __set_error_occurred_(self):
        self._is_disable = True
        #
        self._status = self.Status.Error
        #
        self.__set_logging_(
            'ddl-job-id="{}", ddl-job-name="{}" is error'.format(
                self._job_id, self._job_name
            )
        )

    #
    def __set_run_(self):
        if self._is_disable is False:
            pre_process_status = self._status
            #
            self.__set_status_update_method_run_()
            #
            if pre_process_status != self._status:
                self.__set_status_changed_()
            #
            self.__set_elements_running_()

    def __set_processing_time_update_(self):
        self._processing_time_cost += 1
        if self._processing_time_cost >= self._processing_time_maximum:
            self.__set_logging_(
                'ddl-job-id="{}", ddl-job-name="{}" is timeout'.format(
                    self._job_id, self._job_name
                )
            )
            self.__set_error_occurred_()
            return False
        #
        if self._timer is not None:
            self._timer.cancel()
        self._timer = threading.Timer(self._time_interval, self.__set_run_)
        self._timer.start()
        # self._timer.join()

    def __set_waiting_time_update_(self):
        self._waiting_time_cost += 1
        if self._waiting_time_cost >= self._waiting_time_maximum:
            self.__set_logging_(
                'ddl-job-id="{}", ddl-job-name="{}" waiting is timeout'.format(
                    self._job_id, self._job_name
                )
            )
            self.__set_error_occurred_()
            return False

    def __set_running_time_update_(self):
        self._running_time_cost += 1
        if self._running_time_cost >= self._running_time_maximum:
            self.__set_logging_(
                'ddl-job-id="{}", ddl-job-name="{}" running is timeout'.format(
                    self._job_id, self._job_name
                )
            )
            self.__set_error_occurred_()
            return False

    def get_running_time_maximum(self):
        return self._running_time_maximum

    def set_start(self):
        self.__set_started_()
        self.__set_status_changed_()

    def set_stop(self):
        self.__set_stopped_()
        #
        self.__set_status_changed_()
        self.__set_element_statuses_changed_()

    def get_is_started(self):
        return self._status == self.Status.Started

    def get_is_running(self):
        return self._status == self.Status.Running

    def get_is_completed(self):
        return self._status == self.Status.Completed

    def get_is_stopped(self):
        return self._status == self.Status.Stopped

    def get_running_time_cost(self):
        return self._running_time_cost

    def get_status(self):
        return self._status

    def get_element_statuses(self):
        return self._sub_process_statuses


class DdlJobMonitor(object):
    Status = bsc_configure.Status
    # Unknown = 0
    # Active = 1
    # Suspended = 2
    # Completed = 3
    # Failed = 4
    # Pending = 6
    JOB_STATUS = [
        Status.Unknown,
        Status.Started,
        Status.Suspended,
        Status.Completed,
        Status.Failed,
        Status.Unknown,
        Status.Waiting,
    ]
    # Unknown = 1
    # Queued = 2
    # Suspended = 3
    # Rendering = 4
    # Completed = 5
    # Failed = 6
    # 7
    # Pending = 8
    TASK_STATUS = [
        Status.Unknown,
        Status.Unknown,
        Status.Waiting,
        Status.Suspended,
        Status.Running,
        Status.Completed,
        Status.Failed,
        Status.Unknown,
        Status.Waiting
    ]

    #
    def __init__(self, job_id):
        self._job_query = DdlJobQuery(job_id)
        self._job_id = self._job_query.get_id()
        self._job_name = self._job_query.get_name()
        self._task_queries = self._job_query.get_tasks()

        self._timestamp_start = 0

        self.__is_active = True

        c = len(self._task_queries)
        self._job_status = self.Status.Started
        self._task_statuses = [self.Status.Started]*c
        self._task_progress = ['0 %']*c

        self.__timer = None
        self._timer_interval = 1

        self.running = SignalInstance(int)
        self.job_status_changed = SignalInstance(int)
        self.job_finished = SignalInstance(int)
        self.task_status_changed_at = SignalInstance(int, int)
        self.task_progress_changed_at = SignalInstance(int, str)
        self.task_finished_at = SignalInstance(int, int)
        self.logging = SignalInstance(str)

    def __set_loop_running_(self):
        if self.__is_active is True:
            # job
            pre_job_status = self._job_status
            self._job_status = self.JOB_STATUS[self._job_query.get_status()]
            if pre_job_status != self._job_status:
                self.__set_job_status_changed_(self._job_status)
            # task
            for index, i_task_query in enumerate(self._task_queries):
                # progress
                i_task_progress_pre = self._task_progress[index]
                i_task_progress = i_task_query.get_progress()
                if i_task_progress != i_task_progress_pre:
                    self._task_progress[index] = i_task_progress
                    self.__set_task_progress_at_(index, i_task_progress)
                # status
                i_task_status_pre = self._task_statuses[index]
                i_task_status = self.TASK_STATUS[i_task_query.get_status()]
                if i_task_status != i_task_status_pre:
                    self._task_statuses[index] = i_task_status
                    self.__set_task_status_changed_at_(index, i_task_status)
                    if i_task_status in [
                        self.Status.Completed,
                        self.Status.Failed,
                    ]:
                        self.__set_task_finished_at_(index, i_task_status)
            # check is finished
            if self._job_status not in [
                self.Status.Completed,
                self.Status.Failed,
            ]:
                self.__set_running_()
            else:
                self.__set_job_finished_(self._job_status)

    def __set_running_(self):
        self.__timer = threading.Timer(self._timer_interval, self.__set_loop_running_)
        self.__timer.setDaemon(True)
        self.__timer.start()

    def __set_logging_(self, text):
        result = bsc_core.LogMtd.get_result(text)
        self.logging.send_emit(
            result
        )
        print result

    def __set_job_status_changed_(self, status):
        if self.__is_active is True:
            self.job_status_changed.send_emit(status)
            self.__set_logging_(u'job status is change to "{}"'.format(str(status)))

    def __set_task_status_changed_at_(self, index, status):
        if self.__is_active is True:
            self.task_status_changed_at.send_emit(index, status)
            self.__set_logging_(u'task {} status is change to "{}"'.format(index, str(status)))

    def __set_task_progress_at_(self, index, progress):
        if self.__is_active is True:
            self.task_progress_changed_at.send_emit(index, progress)
            self.__set_logging_(u'task {} progress is changed to "{}"'.format(index, str(progress)))

    def __set_job_finished_(self, status):
        self.__is_active = False
        self.job_finished.send_emit(status)
        self.__set_logging_(u'job is finished')

    def __set_task_finished_at_(self, index, status):
        if self.__is_active is True:
            self.task_finished_at.send_emit(index, status)
            self.__set_logging_(u'task {} is finished'.format(index))

    def get_task_count(self):
        return len(self._task_queries)

    def get_task_statuses(self):
        return self._task_statuses

    def get_job_status(self):
        return self._job_status

    def set_start(self):
        self.__set_logging_(u'job id is "{}"'.format(self._job_id))
        self.__set_logging_(u'job is started')
        #
        self.__set_running_()

    def set_stop(self):
        if self.__is_active is True:
            self.__set_logging_(u'job is stopped')
            #
            if self.__timer is not None:
                self.__timer.cancel()
            #
            self.__is_active = False
            #
            self.running.set_cancel()
            self.job_status_changed.set_cancel()
            self.job_finished.set_cancel()
            self.task_status_changed_at.set_cancel()
            self.task_progress_changed_at.set_cancel()
            self.task_finished_at.set_cancel()
            self.logging.set_cancel()


class DdlMethodQuery(ddl_obj_abs.AbsDdlMethodQuery):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file(
        'deadline/query/method'
    )

    def __init__(self, *args, **kwargs):
        super(DdlMethodQuery, self).__init__(*args, **kwargs)


class DdlRsvTaskQuery(ddl_obj_abs.AbsDdlRsvTaskQuery):
    CONFIGURE_FILE_PATH = utl_configure.MainData.get_configure_file(
        'deadline/query/rsv-task'
    )

    def __init__(self, *args, **kwargs):
        super(DdlRsvTaskQuery, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    def test_0(*args):
        pass


    def test_1(*args):
        pass


    m = DdlJobMonitor('62cea962e127c60c888791c0')

    m.set_start()

    m.running.connect_to(test_0)

    m.job_status_changed.connect_to(test_1)
