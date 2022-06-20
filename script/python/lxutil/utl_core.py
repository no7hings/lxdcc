# coding:utf-8
from __future__ import print_function

import sys

import platform

import os

import glob

import threading

import time

import collections

import yaml

import json

import getpass

import types

import subprocess

import re

import fnmatch

import functools

import copy

from lxscheme.scm_objects import _scm_obj_utility

from lxutil import utl_configure

from lxbasic import bsc_configure, bsc_core

import lxbasic.objects as bsc_objects

QT_LOG_RESULT_TRACE_METHOD = None
QT_LOG_WARNING_TRACE_METHOD = None
QT_LOG_ERROR_TRACE_METHOD = None
#
LOG_WRITE_METHOD = None
#
QT_PROGRESS_CREATE_METHOD = None


class _Pattern(object):
    def __init__(self, pattern):
        self._pattern = pattern
        self._fnmatch_pattern = self._get_fnmatch_pattern_(self._pattern)
    @classmethod
    def _get_fnmatch_pattern_(cls, variant):
        if variant is not None:
            re_pattern = re.compile(r'[{](.*?)[}]', re.S)
            #
            keys = re.findall(re_pattern, variant)
            s = variant
            if keys:
                for key in keys:
                    s = s.replace('{{{}}}'.format(key), '*')
            return s
        return variant
    @property
    def format(self):
        return self._pattern
    @property
    def pattern(self):
        return self._fnmatch_pattern


class Log(object):
    DEFAULT_CODING = sys.getdefaultencoding()
    print(
        'lynxi logger is initialization, default coding is "{}"'.format(DEFAULT_CODING)
    )
    # reload(sys)
    # if hasattr(sys, 'setdefaultencoding'):
    #     sys.setdefaultencoding('utf-8')
    #
    PRINT_ENABLE = True
    def __init__(self, file_path):
        self._file_path = file_path
    @classmethod
    def get_active_prettify_time(cls):
        return time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    @classmethod
    def set_trace(cls, *args, **kwargs):
        text = args[0]
        if text:
            text = u'{} {}'.format(cls.get_active_prettify_time(), text)
            #
            print_method = kwargs.get('print_method')
            if isinstance(print_method, (types.FunctionType, types.MethodType)):
                print_method(text)
            # else:
            if cls.PRINT_ENABLE is True:
                # noinspection PyBroadException
                try:
                    print(text.encode('utf-8'))
                except:
                    pass
            #
            if isinstance(LOG_WRITE_METHOD, (types.FunctionType, types.MethodType)):
                # noinspection PyCallingNonCallable
                LOG_WRITE_METHOD(text)
            return text
    @classmethod
    def set_result_trace(cls, *args):
        text = args[0]
        return cls.set_trace(
            u'''        | {}'''.format(text),
            print_method=QT_LOG_RESULT_TRACE_METHOD,
            write_method=LOG_WRITE_METHOD
        )
    @classmethod
    def set_module_result_trace(cls, *args):
        module = args[0]
        texts = args[1:]
        return cls.set_result_trace(
            u'''<{}> {}'''.format(module, u''.join(texts))
        )
    @classmethod
    def set_warning_trace(cls, *args):
        text = args[0]
        return cls.set_trace(
            u'''warning | {}'''.format(text),
            print_method=QT_LOG_WARNING_TRACE_METHOD,
            write_method=LOG_WRITE_METHOD
        )
    @classmethod
    def set_module_warning_trace(cls, *args):
        module = args[0]
        texts = args[1:]
        return cls.set_warning_trace(
            u'''<{}> {}'''.format(module, u''.join(texts))
        )
    @classmethod
    def set_error_trace(cls, *args):
        text = args[0]
        return cls.set_trace(
            u''' error  | {}'''.format(text),
            print_method=QT_LOG_ERROR_TRACE_METHOD,
            write_method=LOG_WRITE_METHOD
        )
    @classmethod
    def set_module_error_trace(cls, *args):
        module = args[0]
        texts = args[1:]
        return cls.set_error_trace(
            u'''<{}> {}'''.format(module, u''.join(texts))
        )
    @classmethod
    def set_log_write(cls, file_path, text):
        if file_path is not None:
            with open(file_path, 'a+') as log:
                log.writelines(u'{}\n'.format(text))
                log.close()
    @classmethod
    def set_progress_create(cls, *args):
        pass
    @classmethod
    def set_progress_update(cls, *args):
        pass
    @classmethod
    def set_progress_stop(cls, *args):
        pass
    @classmethod
    def get_trace(cls, *args):
        text = args[0]
        ts = text.split('\n')
        pattern_0 = _Pattern(
            (
                '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                ' [0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
                ' {status} | {content}'
            )
        )
        lines = fnmatch.filter(
            ts, pattern_0.pattern
        )
        return '\n'.join(lines)


class ModuleResultLog(object):
    def __init__(self, module, result):
        self._module = module
        self._result = result

    def __enter__(self):
        Log.set_module_result_trace(
            self._module, self._result, ' is started'
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Log.set_module_result_trace(
            self._module, self._result, ' is completed'
        )


def module_resulter_log(module, result):
    return ModuleResultLog(module, result)


class Progress(object):
    PROGRESSES = []
    @classmethod
    def set_create(cls, maximum, label=None):
        if QT_PROGRESS_CREATE_METHOD is not None:
            # noinspection PyCallingNonCallable
            ps = QT_PROGRESS_CREATE_METHOD(maximum, label=label)
            [cls.PROGRESSES.append(i) for i in ps]
            return ps
        return []
    @classmethod
    def set_update(cls, ps):
        for p in ps:
            p.set_update()
    @classmethod
    def set_stop(cls, ps):
        for p in ps:
            p.set_stop()
            cls.PROGRESSES.remove(p)


class GuiProgressesRunner(object):
    def __init__(self, maximum, label=None):
        self._maximum = maximum
        self._value = 0
        self._label = label
        if isinstance(QT_PROGRESS_CREATE_METHOD, (types.FunctionType, types.MethodType)):
            self._ps = QT_PROGRESS_CREATE_METHOD(maximum, label=label)
        else:
            self._ps = []
        #
        if self._label is not None:
            self._log_progress_runner = LogProgressRunner(
                maximum=self._maximum,
                label=self._label
            )
        else:
            self._log_progress_runner = None

    def set_update(self):
        for p in self._ps:
            p.set_update()
        #
        if self._log_progress_runner is not None:
            self._log_progress_runner.set_update()

    def set_stop(self):
        for p in self._ps:
            p.set_stop()
        #
        if self._log_progress_runner is not None:
            self._log_progress_runner.set_stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_stop()


def gui_progress(maximum, label=None):
    return GuiProgressesRunner(maximum, label)


class LogProgressRunner(object):
    def __init__(self, maximum, label, use_as_progress_bar=False):
        self._maximum = maximum
        self._value = 0
        self._label = label
        self._use_as_progress_bar = use_as_progress_bar
        #
        self._start_timestamp = bsc_core.SystemMtd.get_timestamp()
        self._pre_timestamp = bsc_core.SystemMtd.get_timestamp()
        #
        Log.set_module_result_trace(
            self._label,
            'is started'
        )

    def set_update(self, sub_label=None):
        self._value += 1
        cur_timestamp = bsc_core.SystemMtd.get_timestamp()
        cost_timestamp = cur_timestamp - self._pre_timestamp
        self._pre_timestamp = cur_timestamp
        #
        percent = float(self._value) / float(self._maximum)
        #
        if self._use_as_progress_bar is True:
            Log.set_module_result_trace(
                u'{}'.format(self._label),
                u'is running {} {}%, cost time {}'.format(
                    self._get_progress_bar_string_(percent),
                    '%3d' % (percent*100),
                    bsc_core.IntegerMtd.second_to_time_prettify(cost_timestamp),

                )
            )
        else:
            Log.set_module_result_trace(
                u'{}'.format(self._label),
                u'is running {}%, cost time {}'.format(
                    '%3d' % (percent*100),
                    bsc_core.IntegerMtd.second_to_time_prettify(cost_timestamp),
                )
            )
    @classmethod
    def _get_progress_bar_string_(cls, percent):
        c = 20
        p = int(percent*c)
        p = max(p, 1)
        return u'{}{}'.format(
            p*u'■', (c-p)*u'□'
        )

    def set_stop(self):
        self._value = 0
        self._maximum = 0
        #
        cost_timestamp = bsc_core.SystemMtd.get_timestamp() - self._start_timestamp
        Log.set_module_result_trace(
            self._label,
            'is completed, cost time {}'.format(
                bsc_core.IntegerMtd.second_to_time_prettify(cost_timestamp),
            )
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_stop()


def log_progress(maximum, label, use_as_progress_bar=False):
    return LogProgressRunner(maximum, label, use_as_progress_bar)


def log_progress_bar(maximum, label, use_as_progress_bar=True):
    return LogProgressRunner(maximum, label, use_as_progress_bar)


class DialogWindow(object):
    GuiStatus = bsc_configure.GuiStatus
    @classmethod
    def set_create(
        cls,
        label,
        content=None,
        content_text_size=10,
        window_size=(480, 160),
        yes_method=None,
        yes_label=None,
        yes_visible=True,
        #
        no_method=None,
        no_label=None,
        no_visible=True,
        #
        cancel_fnc=None,
        cancel_label=None,
        cancel_visible=True,
        #
        button_size=160,
        status=None,
        use_as_error=False,
        use_as_warning=False,
        show=True,
        use_exec=True,
        options_configure=None,
        use_thread=True
    ):
        import lxutil_gui.proxy.widgets as prx_widgets
        #
        if use_exec is True:
            w = prx_widgets.PrxDialogWindow1()
        else:
            w = prx_widgets.PrxDialogWindow0()
        #
        w.set_use_thread(use_thread)
        w.set_window_title(label)
        w.set_content(content)
        w.set_content_font_size(content_text_size)
        w.set_definition_window_size(window_size)
        if yes_label is not None:
            w.set_yes_label(yes_label)
        if yes_method is not None:
            w.set_yes_method_add(yes_method)
        w.set_yes_visible(yes_visible)
        #
        if no_label is not None:
            w.set_no_label(no_label)
        if no_method is not None:
            w.set_no_method_add(no_method)
        w.set_no_visible(no_visible)
        #
        if cancel_label is not None:
            w.set_cancel_label(cancel_label)
        if cancel_fnc is not None:
            w.set_cancel_method_add(cancel_fnc)
        w.set_cancel_visible(cancel_visible)
        #
        if status is not None:
            w.set_window_title('[ {} ] {}'.format(str(status).split('.')[-1], label))
            w.set_status(status)
        #
        if options_configure is not None:
            w.set_options_group_enable()
            w.set_options_create_by_configure(options_configure)
        #
        if show is True:
            w.set_window_show()
        return w


class WaitWindow(object):
    pass


class ExceptionCatcher(object):
    GuiStatus = bsc_configure.GuiStatus
    @classmethod
    def _get_window_(cls):
        from lxutil_gui.proxy import utl_gui_prx_core
        #
        import lxutil_gui.proxy.widgets as prx_widgets
        #
        w_cls = prx_widgets.PrxTipWindow
        _0 = utl_gui_prx_core.get_gui_proxy_by_class(w_cls)
        if _0:
            return _0[0]
        #
        _1 = prx_widgets.PrxTipWindow()
        #
        _1.set_window_title('Exception')
        _1.set_definition_window_size((640, 320))
        _1.set_window_show()
        return _1
    @classmethod
    def set_create(cls, use_window=True):
        import sys
        #
        import traceback
        #
        exc_texts = []
        value = ''
        exc_type, exc_value, exc_stack = sys.exc_info()
        if exc_type:
            value = '{}: "{}"'.format(exc_type.__name__, exc_value.message)
            for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                i_file_path, i_line, i_fnc, i_fnc_line = stk
                exc_texts.append(
                    '    file "{}" line {} in {}\n        {}'.format(i_file_path, i_line, i_fnc, i_fnc_line)
                )
            #
            if use_window is True:
                w = cls._get_window_()
                #
                w.set_status(cls.GuiStatus.Error)
                w.set_content_add('*'*72)
                label = '{}'.format(exc_type.__name__)
                w.set_content_add('traceback:')
                Log.set_module_error_trace('exception-catch', label)
                #
                [w.set_content_add(i) for i in exc_texts]
                [Log.set_error_trace(i) for i in exc_texts]
                #
                w.set_content_add(value)
                Log.set_error_trace(value)
                return w
        else:
            print(u'\n'.join(exc_texts))
            print(value)
    @classmethod
    def set_create_for_execute(cls, use_window=True):
        pass


class LogCatcher(object):
    def set_create(self):
        pass


class SubProcessRunner(object):
    if platform.system().lower() == 'windows':
        # noinspection PyUnresolvedReferences
        NO_WINDOW = subprocess.STARTUPINFO()
        NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        NO_WINDOW = None
    #
    def __init__(self):
        pass
    @classmethod
    def set_run_with_result(cls, cmd, clear_environ=False):
        Log.set_module_result_trace(
            'sub-progress run with result',
            u'command=`{}` is started'.format(cmd)
        )
        bsc_core.SubProcessMtd.set_run_with_result(
            cmd, clear_environ
        )
        # Log.set_module_result_trace(
        #     'sub-progress run with result',
        #     u'command=`{}` is completed'.format(cmd)
        # )
    @classmethod
    def set_run(cls, cmd):
        Log.set_module_result_trace(
            'sub-progress run',
            u'command=`{}`'.format(cmd)
        )
        return bsc_core.SubProcessMtd.set_run(
            cmd
        )
    @classmethod
    def set_run_with_log(cls, name, cmd):
        import lxutil_gui.proxy.widgets as prx_widgets
        #
        w = prx_widgets.PrxProcessWindow()
        w.set_window_show()
        #
        w.set_process_name(name)
        w.set_process_cmd(cmd)
        w.set_process_start()
    @classmethod
    def set_run_with_result_use_thread(cls, cmd, clear_environ=False):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.set_run_with_result,
                cmd=cmd,
                clear_environ=clear_environ
            )
        )
        t_0.start()
        # t_0.join()
    @classmethod
    def set_run_with_result_use_log(cls):
        pass


class Icon(object):
    ROOT_PATH = utl_configure.Root.icon
    ICON_KEY_PATTERN = r'[@](.*?)[@]'
    @classmethod
    def get(cls, icon_name, ext='.svg'):
        glob_pattern = '{}/{}.*'.format(cls.ROOT_PATH, icon_name)
        results = glob.glob(glob_pattern) or []
        if results:

            return bsc_core.StoragePathOpt(results[-1]).get_path()
    @classmethod
    def get_katana_obj(cls):
        return cls.get('application/katana', ext='.png')
    @classmethod
    def get_port(cls):
        return cls.get('attribute')
    @classmethod
    def _get_file_path_(cls, icon_key):
        _ = re.findall(re.compile(cls.ICON_KEY_PATTERN, re.S), icon_key)
        if _:
            glob_pattern = '{}/{}.*'.format(cls.ROOT_PATH, _[0])
            results = glob.glob(glob_pattern) or []
            if results:
                return results[-1]


class IconFile(object):
    def get_by_icon_key(self, icon_key):
        pass


class FileIcon(object):
    ROOT_PATH = utl_configure.Root.icon
    @classmethod
    def get(cls, icon_name):
        """
        :param icon_name: str
        :return:
        """
        dir_path = '{}/file'.format(cls.ROOT_PATH)
        glob_pattern = '{}/{}.*'.format(dir_path, icon_name)
        glob_results = glob.glob(glob_pattern)
        if glob_results:
            return glob_results[0]
    @classmethod
    def get_default(cls):
        dir_path = '{}/file'.format(cls.ROOT_PATH)
        return '{}/file.svg'.format(dir_path)
    @classmethod
    def get_root(cls):
        return Icon.get('file/root')
    @classmethod
    def get_folder(cls):
        return Icon.get('file/folder')
    @classmethod
    def get_image(cls):
        return Icon.get('file/image')
    @classmethod
    def get_houdini(cls):
        return Icon.get('file/houdini')
    @classmethod
    def get_maya(cls):
        return Icon.get('file/ma')
    @classmethod
    def get_by_file_ext(cls, ext):
        return Icon.get('file/{}'.format(ext[1:]))


class MayaIcon(object):
    pass


class HoudiniIcon(object):
    pass


class Scheme(object):
    UTILITY_TOOL_TD = _scm_obj_utility.FileScheme(
        '{}/utility/tool/td_configures.yml'.format(utl_configure.Root.DATA)
    )
    # maya tool
    MAYA_TOOL_TD = _scm_obj_utility.FileScheme(
        '{}/maya/tool/td_configures.yml'.format(utl_configure.Root.DATA)
    )
    # houdini tool
    HOUDINI_TOOL_TD = _scm_obj_utility.FileScheme(
        '{}/houdini/tool/td_configures.yml'.format(utl_configure.Root.DATA)
    )
    # katana tool
    KATANA_TOOL_TD = _scm_obj_utility.FileScheme(
        '{}/katana/tool/td_configures.yml'.format(utl_configure.Root.DATA)
    )


class OrderedYamlMtd(object):
    @classmethod
    def set_dump(cls, raw, stream=None, Dumper=yaml.SafeDumper, object_pairs_hook=collections.OrderedDict, **kwargs):
        class _Cls(Dumper):
            pass
        # noinspection PyUnresolvedReferences
        def _fnc(dumper_, data_):
            return dumper_.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data_.items(),
            )

        _Cls.add_representer(object_pairs_hook, _fnc)
        return yaml.dump(raw, stream, _Cls, **kwargs)
    @classmethod
    def set_load(cls, stream, Loader=yaml.SafeLoader, object_pairs_hook=collections.OrderedDict):
        class _Cls(Loader):
            pass
        # noinspection PyArgumentList
        def _fnc(loader_, node_):
            loader_.flatten_mapping(node_)
            return object_pairs_hook(loader_.construct_pairs(node_))
        # noinspection PyUnresolvedReferences
        _Cls.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _fnc)
        return yaml.load(stream, _Cls)


class System(object):
    TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
    TIME_TAG_FORMAT = u'%Y_%m%d_%H%M_%S'
    @classmethod
    def get_user_name(cls):
        return getpass.getuser()
    @classmethod
    def get_platform(cls):
        if cls.get_is_windows():
            return 'windows'
        elif cls.get_is_linux():
            return 'linux'
        raise TypeError()
    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'
    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'
    @classmethod
    def get_time(cls):
        timestamp = time.time()
        return time.strftime(
            cls.TIME_FORMAT,
            time.localtime(timestamp)
        )
    @classmethod
    def get_time_tag(cls):
        return bsc_core.SystemMtd.get_time_tag()
    @classmethod
    def get_application(cls):
        return Application.get_current()


class Environ(object):
    TD_ENABLE_KEY = 'LYNXI_TD_ENABLE'
    DATA_PATH_KEY = 'LYNXI_DATA_PATH'
    #
    TRUE = 'true'
    FALSE = 'false'
    def __init__(self):
        pass
    @classmethod
    def get_td_enable(cls):
        _ = cls.get(cls.TD_ENABLE_KEY)
        if _ == cls.TRUE:
            return True
        return False
    @classmethod
    def set_td_enable(cls, boolean):
        if boolean is True:
            cls.set(cls.TD_ENABLE_KEY, cls.TRUE)
        else:
            cls.set(cls.TD_ENABLE_KEY, cls.FALSE)
    @classmethod
    def get(cls, key):
        return os.environ.get(key)
    @classmethod
    def get_as_array(cls, key):
        _ = os.environ.get(key) or ''
        return _.split(os.pathsep)
    @classmethod
    def set(cls, key, value):
        os.environ[key] = value
        Log.set_module_result_trace(
            'environ set',
            u'key="{}", value="{}"'.format(key, value)
        )
    @classmethod
    def set_add(cls, key, value):
        if key in os.environ:
            v = os.environ[key]
            if value not in v:
                os.environ[key] += os.pathsep + value
                Log.set_module_result_trace(
                    'environ add',
                    u'key="{}", value="{}"'.format(key, value)
                )
        else:
            os.environ[key] = value
            Log.set_module_result_trace(
                'environ-set',
                u'key="{}", value="{}"'.format(key, value)
            )


class Platform(object):
    @classmethod
    def get_current(cls):
        if cls.get_is_windows():
            return 'windows'
        elif cls.get_is_linux():
            return 'linux'
        raise TypeError()
    @staticmethod
    def get_is_linux():
        return platform.system() == 'Linux'
    @staticmethod
    def get_is_windows():
        return platform.system() == 'Windows'


class Application(object):
    @classmethod
    def get_is_maya(cls):
        _ = os.environ.get('MAYA_APP_DIR')
        if _:
            return True
        return False
    @classmethod
    def get_is_houdini(cls):
        _ = os.environ.get('HIP')
        if _:
            return True
        return False
    @classmethod
    def get_is_katana(cls):
        _ = os.environ.get('KATANA_ROOT')
        if _:
            return True
        return False
    @classmethod
    def get_is_dcc(cls):
        for i in [cls.get_is_maya(), cls.get_is_houdini(), cls.get_is_katana()]:
            if i is True:
                return True
        return False
    @classmethod
    def get_current(cls):
        if cls.get_is_maya():
            return bsc_configure.Application.Maya
        elif cls.get_is_houdini():
            return bsc_configure.Application.Houdini
        elif cls.get_is_katana():
            return bsc_configure.Application.Katana
        return bsc_configure.Application.Python


class File(object):
    @classmethod
    def set_write(cls, file_path, raw):
        Log.set_module_result_trace(
            'file write',
            u'file="{}" is started'.format(file_path)
        )
        directory = os.path.dirname(file_path)
        if os.path.isdir(directory) is False:
            os.makedirs(directory)
        ext = os.path.splitext(file_path)[-1]
        if ext in ['.json']:
            with open(file_path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif ext in ['.yml']:
            with open(file_path, 'w') as y:
                bsc_core.OrderedYamlMtd.set_dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                )
        else:
            with open(file_path, 'w') as f:
                f.write(raw)
        #
        Log.set_module_result_trace(
            'file write',
            u'file="{}" is completed'.format(file_path)
        )
    @classmethod
    def set_read(cls, file_path):
        if os.path.exists(file_path):
            ext = os.path.splitext(file_path)[-1]
            if ext in ['.json']:
                with open(file_path) as j:
                    return json.load(j, object_pairs_hook=collections.OrderedDict)
            elif ext in ['.yml']:
                with open(file_path) as y:
                    return bsc_core.OrderedYamlMtd.set_load(y)


class PathMapper(object):
    def __init__(self, file_path):
        self._raw = File.set_read(file_path)
        if System.get_is_windows():
            p = 'windows'
        elif System.get_is_linux():
            p = 'linux'
        else:
            raise TypeError()
        #
        self._windows_dict = self._get_mapper_dict_('windows')
        self._linux_dict = self._get_mapper_dict_('linux')
        #
        self._current_dict = self._get_mapper_dict_(p)

    def __contains__(self, item):
        return item in self._current_dict

    def __getitem__(self, item):
        return self._current_dict[item]

    def _get_mapper_dict_(self, platform_):
        dic = collections.OrderedDict()
        raw_platform = self._raw[platform_]
        for k, v in raw_platform.items():
            for i in v:
                dic[i] = k
        return dic


class Path(object):
    PATHSEP = '/'
    #
    PATH_MAPPER = PathMapper(
        file_path=utl_configure.Data.PATH_MAPPER_CONFIGURE_PATH
    )
    @classmethod
    def set_map_to_platform(cls, path):
        if path is not None:
            if System.get_is_windows():
                return cls.set_map_to_windows(path)
            elif System.get_is_linux():
                return cls.set_map_to_linux(path)
            return bsc_core.StoragePathOpt(path).__str__()
        return path
    @classmethod
    def set_map_to_windows(cls, path):
        path = bsc_core.StoragePathOpt(path).__str__()
        if bsc_core.StoragePathMtd.get_path_is_linux(path):
            mapper_dict = cls.PATH_MAPPER._windows_dict
            for src_root, tgt_root in mapper_dict.items():
                if path.startswith(src_root):
                    return tgt_root + path[len(src_root):]
            return path
        return path
    @classmethod
    def set_map_to_linux(cls, path):
        path = bsc_core.StoragePathOpt(path).__str__()
        if bsc_core.StoragePathMtd.get_path_is_windows(path):
            mapper_dict = cls.PATH_MAPPER._linux_dict
            for src_root, tgt_root in mapper_dict.items():
                if path.startswith(src_root):
                    return tgt_root + path[len(src_root):]
            return path
        return path
    @classmethod
    def _str_to_number_embedded_args_(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def _get_stg_paths_by_parse_pattern_(cls, glob_pattern, sort_by='number'):
        _ = glob.glob(glob_pattern) or []
        if _:
            # fix windows path
            if platform.system() == 'Windows':
                _ = [i.replace('\\', '/') for i in _]
            if len(_) > 1:
                # sort by number
                if sort_by == 'number':
                    _.sort(key=lambda x: cls._str_to_number_embedded_args_(x))
        return _


class AppLauncher(object):
    LOCAL_ROOT = '{}/packages/pglauncher/9.9.99'.format(bsc_core.SystemMtd.get_user_directory_path())
    SERVER_ROOT = '/l/packages/pg/prod/pglauncher/9.9.9'
    #
    PROJECT_CONFIGURE_DIRECTORY_PATTERN = '{root}/{project}_config'
    APP_CONFIGURE_FILE_PATTERN = '{root}/{project}_config/bin/config/{application}.yml'
    BIN_PATTERN = '{root}/{project}_config/bin/{application}'
    APP_CONFIGURE_MAP_DICT = {
        'usdview': 'usd_view'
    }
    def __init__(self, **kwargs):
        """
        :param kwargs:
            project: <project-name>
            application: <application-name>
        """
        if bsc_core.StoragePathOpt(self.LOCAL_ROOT).get_is_exists():
            self._root = Path.set_map_to_platform(self.LOCAL_ROOT)
        else:
            self._root = Path.set_map_to_platform(self.SERVER_ROOT)
        #
        self._kwargs = dict(
            root=self._root,
            project=kwargs['project'],
            application=kwargs['application']
        )
    @classmethod
    def _get_application_configure_file_path_(cls, **kwargs):
        kwargs_ = copy.copy(kwargs)
        application = kwargs['application']
        if application in cls.APP_CONFIGURE_MAP_DICT:
            application_ = cls.APP_CONFIGURE_MAP_DICT[application]
            kwargs_['application'] = application_
        return cls.APP_CONFIGURE_FILE_PATTERN.format(
            **kwargs_
        )
    @classmethod
    def _set_cmd_run_(cls, *args):
        SubProcessRunner.set_run(
            ' '.join(['rez-env'] + list(args))
        )
    @classmethod
    def _get_run_cmd_(cls, *args):
        return ' '.join(['rez-env'] + list(args))
    @classmethod
    def _set_run_with_result_(cls, *args):
        SubProcessRunner.set_run_with_result(
            ' '.join(['rez-env'] + list(args))
        )
    @classmethod
    def _set_run_with_result_use_thread_(cls, *args):
        SubProcessRunner.set_run_with_result_use_thread(
            ' '.join(['rez-env'] + list(args)),
            clear_environ=True
        )

    def get_rez_packages(self):
        lis = []
        kwargs = copy.copy(self._kwargs)
        application = self._kwargs['application']
        if application == 'python':
            kwargs['application'] = 'maya'
        elif application == 'shotgun':
            kwargs['application'] = 'maya'
        elif application == 'usd':
            kwargs['application'] = 'maya'
        elif application == 'gui':
            kwargs['application'] = 'maya'
        elif application == 'rv':
            kwargs['application'] = 'maya'
        elif application == 'rv-movie-convert':
            kwargs['application'] = 'maya'
        elif application == 'lynxi':
            return ['lxdcc']
        #
        configure_file_path = self._get_application_configure_file_path_(**kwargs)
        if os.path.exists(configure_file_path):
            Log.set_module_result_trace(
                'launcher-configure search',
                'project="{project}", application="{application}"'.format(
                    **kwargs
                )
            )
            configure = bsc_objects.Configure(value=configure_file_path)
            keys = configure.get_leaf_keys()
            for key in keys:
                i_run_args = configure.get(key)
                lis.extend(i_run_args)
        else:
            Log.set_module_warning_trace(
                'launcher-configure search',
                'file="{}" is non-exists'.format(
                    configure_file_path
                )
            )
            return AppLauncher(
                project='default',
                application=application
            ).get_rez_packages()
        return lis

    def set_cmd_run(self, command=None):
        run_args = self.get_rez_packages()
        #
        run_args.append(command)
        self._set_cmd_run_(*run_args)

    def get_run_cmd(self, *args):
        run_args = self.get_rez_packages()
        #
        run_args.append(' '.join(args))
        return self._get_run_cmd_(*run_args)

    def set_cmd_run_with_result(self, command=None):
        run_args = self.get_rez_packages()
        #
        run_args.append(command)
        self._set_run_with_result_(*run_args)

    def set_cmd_run_with_result_use_thread(self, cmd):
        run_args = self.get_rez_packages()
        #
        run_args.append(cmd)
        self._set_run_with_result_use_thread_(*run_args)

    def get_configure_exists(self):
        pass


class MayaLauncher(object):
    # Flags:
    # -v                       prints the product version and cut number
    # -batch                   for batch mode
    # -prompt                  for interactive non-gui mode
    # -proj [dir]              look for files in the specified project dir
    # -command [mel command]   runs the specified command on startup
    # -file [file]             opens the specified file
    # -script [file]           sources the specified file on startup
    # -log [file]              copies stdout and stderr messages to the specified file
    # -hideConsole              hide Console Window
    #                              (use complete file name)
    # -recover                 recover the last journal file
    #                              (use 'Render -help' for more options)
    # -optimizeRender [file] [outfile]
    #                          optimize maya file efficient for rendering
    #                              purposes, and put result in outfile
    #                              (use 'maya -optimizeRender -help' for more options)
    # -archive [file]          displays a list of files required to archive the specified scene
    # -noAutoloadPlugins       do not auto-load any plug-ins.
    # -3                       enable Python 3000 compatibility warnings
    # -help                    prints this message
    def __init__(self, **kwargs):
        """
        :param kwargs:
            project: <project-name>
        """
        self._kwargs = kwargs
        self._kwargs['application'] = 'maya'

    def set_file_open(self, file_path):
        args = [
            '-- maya',
            r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_open_as_project(\\\"{}\\\")\")"'.format(
                file_path
            )
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread(
            cmd
        )

    def set_file_new(self, file_path):
        args = [
            '-- maya',
            r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_path_as_project(\\\"{}\\\", with_create_directory=True)\")"'.format(
                file_path
            )
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread(
            cmd
        )

    def get_file_open_cmd(self, file_path):
        args = [
            # 'pgtk',
            # 'shotgun',
            #
            '-- maya',
            '-file',
            '"{}"'.format(file_path),
            # r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_open(\\\"{}\\\")\")"'.format(
            #     file_path
            # )
        ]
        return AppLauncher(**self._kwargs).get_run_cmd(
            *args
        )

    def set_command_run(self, command):
        args = [
            # 'pgtk',
            # 'shotgun',
            #
            '-- maya -batch -command',
            command
        ]
        cmd = r' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run(
            cmd
        )

    def set_run(self):
        args = [
            '-- maya',
        ]
        cmd = r' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread(
            cmd
        )

    def get_rez_packages(self):
        return AppLauncher(
            **self._kwargs
        ).get_rez_packages()


class MayaArnoldRenderCommand(object):
    """
Render -help -r arnold

Usage: Render [options] filename
       where "filename" is a Maya ASCII or a Maya binary file.

Common options:
  -help              Print help
  -test              Print Mel commands but do not execute them
  -verb              Print Mel commands before they are executed
  -keepMel           Keep the temporary Mel file
  -listRenderers     List all available renderers
  -renderer string   Use this specific renderer
  -r string          Same as -renderer
  -proj string       Use this Maya project to load the file
  -log string        Save output into the given file
  -rendersetuptemplate string Apply a render setup template to your scene before command line rendering.  Only templates exported via File > Export All in the Render Setup editor are supported.  Render setting presets and AOVs are imported from the template.  Render settings and AOVs are reloaded after the template if the -rsp and -rsa flags are used in conjunction with this flag.
  -rst string        Same as -rendersetuptemplate
  -rendersettingspreset string Apply the scene Render Settings from this template file before command line rendering.  This is equivalent to performing File > Import Scene Render Settings in the Render Setup editor, then batch rendering.
  -rsp string        Same as -rendersettingspreset
  -rendersettingsaov string Import the AOVs from this json file before command line rendering.
  -rsa string        Same as -rendersettingsaov

Specific options for renderer "arnold": Arnold renderer

General purpose flags:
  -rd path                    Directory in which to store image files
  -im filename                Image file output name
  -rt int                     Render type (0 = render, 1 = export ass, 2 = export and kick)
  -lic boolean                Turn licensing on or off
  -of format                  Output image file format. See the Render Settings window to
        find available formats
  -fnc int                    File Name Convention: any of name, name.ext, ... See the
        Render Settings window to find available options. Use namec and
        namec.ext for Multi Frame Concatenated formats. As a shortcut,
        numbers 1, 2, ... can also be used

Frame numbering options
  -s float                    Starting frame for an animation sequence
  -e float                    End frame for an animation sequence
  -b float                    By frame (or step) for an animation sequence
  -skipExistingFrames boolean Skip frames that are already rendered (if true) or force rendering all frames (if false)
  -pad int                    Number of digits in the output image frame file name
                    extension

Render Layers and Passes
  -rl boolean|name(s)         Render each render layer separately
  -rp boolean|name(s)         Render passes separately. 'all' will render all passes
  -sel boolean|name(s)        Selects which objects, groups and/or sets to render
  -l boolean|name(s)          Selects which display and render layers to render

Camera options
  -cam name                   Specify which camera to be rendered
  -rgb boolean                Turn RGB output on or off
  -alpha boolean              Turn Alpha output on or off
  -depth boolean              Turn Depth output on or off
  -iip                        Ignore Image Planes. Turn off all image planes before
                    rendering

Resolution options
  -x int                      Set X resolution of the final image
  -y int                      Set Y resolution of the final image
  -percentRes float           Renders the image using percent of the resolution
  -ard float                  Device aspect ratio for the rendered image
  -reg int                    Set render region

Samples options
  -ai:as int                  Set anti-aliasing samples
  -ai:hs int                  Set indirect diffuse samples
  -ai:gs int                  Set indirect specular samples
  -ai:rs int                  Set transmission samples
  -ai:bssrdfs int             Number of SSS Samples.

Sample Clamping
  -ai:cmpsv boolean           Enable sample clamping.
  -ai:aovsc boolean           Sample campling affects AOVs.
  -ai:aasc float              Sample max value.
  -ai:iasc float              Sample max value for indirect rays.

Depth options
  -ai:td int                  Set total depth.
  -ai:dif int                 Set indirect diffuse depth.
  -ai:glo int                 Set indirect specular depth.
  -ai:rfr int                 Set transmission depth.
  -ai:vol int                 Set volume GI depth.
  -ai:atd int                 Set auto-transparency depth.

Motion blur
  -ai:mben boolean            Enable motion blur.
  -ai:mbdf boolean            Enable object deformation motion blur.
  -ai:mbcen boolean           Enable camera motion blur.
  -ai:mbrt int                Position. (0 - Start On Frame, 1 - Center On Frame, 2 - End On Frame, 3 - Custom)
  -ai:mbfr float              Shutter Length.
  -ai:mbstart float           Motion Start.
  -ai:mbend float             Motion End.
  -ai:mbms int                Number of motion steps.

Lights
  -ai:llth float              Low light threshold value.
  -ai:ll int                  Light linking mode. (0 - None, 1 - Maya Light Links)
  -ai:sl int                  Shadow linking mode. (0 - None, 1 - Follows Light Linking, 2 - Maya Shadow Links)

Subdivision
  -ai:mxsb int                Maximum subdivision level.

Render Settings
  -ai:threads int             Set the number of threads.
  -ai:bscn int                Bucket Scanning. (0 - Top, 1 - Bottom, 2 - Left, 3 - Right, 4 - Random, 5 - Woven, 6 - Spiral, 7 - Hilbert)
  -ai:bsz int                 Bucket Size.
  -ai:bass boolean            Binary Ass Export.
  -ai:exbb boolean            Export Bounding box.
  -ai:aerr boolean            Abort on Error.
  -ai:alf boolean             Abort on License Fail.
  -ai:slc boolean             Skip License Check.
  -ai:device int              Render Device ( 0 - CPU , 1 - GPU )
  -ai:manGpuSel boolean        Turn on/off Manual GPU Selection
  -ai:gpu int                 Index of the GPU used for the render ( Works in conjunction with manGpuSel and can set a single GPU to render)
  -ai:enas boolean            Enable Adaptive Sampling.
  -ai:maxaa int               AA Samples Max.
  -ai:aath float              AA Adaptive Threshold.
  -ai:uopt string             User Options.
  -ai:port int                Set the Command Port for the Batch Progress Driver
  -ai:ofn string              Original file name.

Textures
  -ai:txamm boolean           Enable texture auto mipmap.
  -ai:txaun boolean           Accept untiled textures.
  -ai:txett boolean           Use existing tiled textures.
  -ai:txaum boolean           Accept unmipped textures.
  -ai:txat int                Auto tile size.
  -ai:txmm float              Maximum texture cache memory. (MB)
  -ai:txmof int               Maximum number of opened textures.
  -ai:txpfs boolean           Per file texture stats.
  -ai:txdb float              Deprecated parameter.
  -ai:txgb float              Deprecated parameter.

Feature Overrides
  -ai:foop boolean            Ignore operators.
  -ai:fotx boolean            Ignore textures.
  -ai:fosh boolean            Ignore shaders.
  -ai:foat boolean            Ignore atmosphere.
  -ai:folt boolean            Ignore lights.
  -ai:fosw boolean            Ignore shadows.
  -ai:fosd boolean            Ignore subdivision.
  -ai:fodp boolean            Ignore displacement.
  -ai:fobp boolean            Ignore bump.
  -ai:fosm boolean            Ignore smoothing.
  -ai:fomb boolean            Ignore motion blur.
  -ai:fosss boolean           Ignore SSS.
  -ai:fodof boolean           Ignore DOF.

Search Path
  -ai:sppg string             Plugins search path.
  -ai:sppr string             Procedurals search path.
  -ai:spsh string             Plugin search path.
  -ai:sptx string             Textures search path.

Log
  -ai:lfn string              Log filename.
  -ai:ltc boolean             Log to Console.
  -ai:ltf boolean             Log to File.
  -ai:lve int                 Verbosity level. (0 - Errors, 1 - Warnings, 2 - Info, 3 - Debug)
  -ai:lmw int                 Maximum number of warnings.
  -ai:mti boolean             MtoA Translation Info.
  -ai:ste boolean             Enable Stats.
  -ai:stf string              Stats Filename .
  -ai:stm int                 Stats Mode
  -ai:pfe boolean             Enable profile.
  -ai:pff string              Profile Filename.

Mel callbacks
  -preRender string           add Mel code executed before rendering
  -postRender string          add Mel code executed after rendering
  -preLayer string            add Mel code executed before each render layer
  -postLayer string           add Mel code executed after each render layer
  -preFrame string            add Mel code executed before each frame
  -postFrame string           add Mel code executed after each frame
  -insertPreRender string     insert Mel code executed before rendering
  -insertPostRender string    insert Mel code executed after rendering
  -insertPreLayer string      insert Mel code executed before each render layer
  -insertPostLayer string     insert Mel code executed after each render layer
  -insertPreFrame string      insert Mel code executed before each frame
  -insertPostFrame string     insert Mel code executed after each frame

 *** Remember to place a space between option flags and their arguments. ***
Any boolean flag will take the following values as TRUE: on, yes, true, or 1.
Any boolean flag will take the following values as FALSE: off, no, false, or 0.

    e.g. -s 1 -e 10 -x 512 -y 512 -cam persp -as 4 -hs 2 -dif 2 file.
    """
    def __init__(self, option):
        self._option = option

    def get(self):
        option_opt = bsc_core.KeywordArgumentsOpt(self._option)
        cmd = r'-- Render -r arnold -rd {render_directory} -cam {camera} -rt 0 -ai:lve 3 -s {start_frame} -e {end_frame} {file} '.format(
            **option_opt.value
        )
        return [cmd]


class HoudiniLauncher(object):
    def __init__(self, **kwargs):
        """
        :param kwargs:
            project: <project-name>
        """
        self._kwargs = kwargs
        self._kwargs['application'] = 'houdini'

    def set_file_open(self, file_path):
        pass

    def set_command_run(self, command):
        args = [
            # 'pgtk',
            # 'shotgun',
            #
            '-- hython',
            command
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run(
            cmd
        )


class KatanaLauncher(object):
    """
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      --batch               Launch Katana in batch mode.
      --script=SCRIPT       Run a script inside Katana, without ui.
      --shell               Run a console interactive session inside Katana,
                            without ui.
      --asset=ASSET         Load Katana script from asset.
      --ocio=OCIO           Specify --ocio <OCIO_CONFIG_PATH> to override the ocio
                            environment before starting up. Otherwise, $OCIO is
                            obeyed.
      --profile             Run Katana in profiling mode. In batch mode profiling
                            starts running immediately, in all other modes it can
                            be started and stopped on demand via the Runtime
                            Python API: runtime.StartProfilingSession() and
                            runtime.EndProfilingSession().
      --force-profile       Force profiling to start immediately. In batch mode
                            this is equivalent as --profile, in all other modes
                            this will start profiling on startup, rather than let
                            it be started during the session on demand.
      --profiling-dir=PROFILING_DIR
                            Specifies the directory where the profiling files will
                            be saved if Katana is running in profiling mode. If
                            not specified, then the Katana session temporary
                            directory will be used. This directory is also used
                            for files generated by Profiling Renders.
      -V LEVEL, --verbose=LEVEL
                            The level of verbosity of logging informational
                            messages. Defaults to 1. Set to 0 to suppress most
                            informational messages.

      Batch Options:
        These options only apply when launching Katana in batch mode.

        --katana-file=KATANA_FILE
                            The Katana file to render.
        -t <range>[,<range>]..., --t=<range>[,<range>]...
                            The frame range for which to render the specified
                            nodes (or the currently viewed node if no --render-
                            node arguments are given). A range should be either a
                            single frame number, or start & end frame numbers
                            separated by a dash. Multiple ranges can be separated
                            by commas, for example: -t 1000,1200-1400,1600
        --threads2d=THREADS2D
                            The number of 2D render threads to be used by the 2D
                            nodes in Katana (default = number of procs + 1).
        --threads3d=THREADS3D
                            The number of 3D render threads to be used by the
                            render process (default = renderer's default.
        --render-node=NodeName[@timerange][=path] or nodeRef:NodeName/ref.param.path
                            The node to render.  The optional "@timerange" limits
                            the frames that this node renders on; the optional
                            "=path" sets the output path this node will render to.
                            The nodeRef form allows you to specify the path to a
                            string parameter that evaluates to the name of a node
                            in the scene.
        --render-views=RENDER_VIEWS
                            List of views to render (example: main,left,right).
        --crop-rect=CROP_RECT
                            The crop window to render (as
                            <left>,<bottom>,<width>,<height>).
        --tile-render=TILE_RENDER
                            Render tile of a 'Render' node.
                            (xIndex,yIndex,xTotal,yTotal)
        --tile-stitch       Stitch together rendered tiles and exit.
        --tile-cleanup      Delete tiles after successful tile stitch.
        --reuse-render-process
                            Iterate over the sequence of frames and export Op tree
                            files for all frames, then start the render process
                            only once on a sequence of exported Op tree files.
        --prerender-publish=PRERENDER_PUBLISH
                            Set up asset management and dump pass info base on
                            batch arguments (specify filename for dumping pass
                            info).
        --make-lookfilebake-scripts=LOOKFILEBAKE_SCRIPT_DIR
                            Write Python scripts for running a lookfilebake on the
                            cue.
        --postrender-publish=POSTRENDER_PUBLISH
                            Set up asset management and dump pass info base on
                            batch arguments (specify filename for dumping pass
                            info).
        --versionup         Version up assets when publishing to the asset
                            management system.
        --render-internal-dependencies
                            Render any dependencies that generate no external
                            (shottree) outputs of their own.
        --render-explicit-version=RENDER_EXPLICIT_VERSION
                            Set render nodes to output to an explicit output
                            version number.
        --var=GRAPH_STATE_VARIABLE
                            Override value of global Graph State Variable in
                            Katana project, e.g. --var myVariableName=newValue

      UI Options:
        These options only apply when launching an interactive UI session of
        Katana.

        -l LAYOUT, --layout=LAYOUT
                            Start up with layout LAYOUT.
        --render-port=RENDERPORT
                            Socket port to listen for render buckets.
        -c, --crash         Load the crash file.

    """
    def __init__(self, **kwargs):
        """
        :param kwargs:
            project: <project-name>
        """
        self._kwargs = kwargs
        self._kwargs['application'] = 'katana'

    def set_file_open(self, file_path):
        args = [
            '-- katana',
            '"{}"'.format(file_path)
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread(
            cmd
        )

    def set_run(self):
        args = [
            '-- katana',
        ]
        cmd = r' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread(
            cmd
        )

    def set_file_new(self, file_path):
        from lxkatana import ktn_configure
        create_args = [
            '-c'
            '"katana --script={} \"set_scene_new\" \"{}\""'.format(
                ktn_configure.Data.SCRIPT_FILE, file_path
            )
        ]
        cmd = ' '.join(create_args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result(
            cmd
        )
        self.set_file_open(file_path)

    def get_rez_packages(self):
        return AppLauncher(
            **self._kwargs
        ).get_rez_packages()


class UsdViewLauncher(object):
    def __init__(self, **kwargs):
        """
        :param kwargs:
            project: <project-name>
        """
        self._kwargs = kwargs
        self._kwargs['application'] = 'usdview'

    def set_file_open(self, file_path):
        args = [
            # 'pgtk',
            # 'shotgun',
            #
            '-- usdview',
            '--render "GL" --camera "/renderCamera/defaultCamera/defaultCameraLeft/defaultCameraLeftShape"',
            '"{}"'.format(file_path),
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run(
            cmd
        )


class RvLauncher(object):
    PACKAGE_PATH = '/l/packages/pg/prod/pgrv'
    def __init__(self, **kwargs):
        """
        :param kwargs:
            project: <project-name>
        """
        self._args = [
            'pgrv',
        ]

    def get_local_bin(self):
        # run_args = copy.copy(self._args)
        platform_ = bsc_core.SystemMtd.get_platform()
        return self._get_local_bin_(platform_)
    @classmethod
    def _get_local_bin_(cls, platform_):
        if platform_ == bsc_core.SystemMtd.Platform.Windows:
            bins = Path._get_stg_paths_by_parse_pattern_(
                'C:/Program Files/Shotgun/*/bin/rvio_hw.exe'
            )
            if bins:
                return bins[0]
        elif platform_ == bsc_core.SystemMtd.Platform.Linux:
            bins = Path._get_stg_paths_by_parse_pattern_(
                '/opt/rv/bin/rv'
            )
            if bins:
                return bins[0]

    def set_file_open(self, file_path):
        run_args = copy.copy(self._args)
        if bsc_core.SystemMtd.get_is_windows():
            bins = Path._get_stg_paths_by_parse_pattern_(
                'C:/Program Files/Shotgun/*/bin/rvio_hw.exe'
            )
            if bins:
                run_args += [
                    '--',
                    '"{}"'.format('pgrv'),
                    '"{}"'.format(file_path)
                ]
            else:
                return
        elif bsc_core.SystemMtd.get_is_linux():
            bins = Path._get_stg_paths_by_parse_pattern_(
                '/opt/rv/bin/rv'
            )
            if bins:
                run_args += [
                    '--',
                    bins[0],
                    '"{}"'.format(file_path)
                ]
            else:
                return
        #
        AppLauncher._set_run_with_result_use_thread_(
            *run_args
        )

    def set_image_convert_to_mov(self, image_file_path, mov_file_path):
        local_bin = self.get_local_bin()
        if local_bin is not None:
            pass


class History(object):
    if System.get_is_windows():
        FILE_PATH = '{}/history.yml'.format(
            bsc_configure.UserDirectory.WINDOWS
        )
    elif System.get_is_linux():
        FILE_PATH = '{}/history.yml'.format(
            bsc_configure.UserDirectory.LINUX
        )
    else:
        raise SystemError()
    @classmethod
    def set_append(cls, key, value):
        f_o = bsc_core.StoragePathOpt(cls.FILE_PATH)
        if f_o.get_is_exists() is False:
            bsc_core.StorageFileOpt(cls.FILE_PATH).set_write(
                {}
            )
        #
        if f_o.get_is_exists() is True:
            configure = bsc_objects.Configure(
                value=f_o.path
            )
            values = configure.get(key) or []
            if value in values:
                values.remove(value)
            #
            values.append(value)
            configure.set(key, values)
            configure.set_save_to(cls.FILE_PATH)
            return True
        return False
    @classmethod
    def set_extend(cls, key, values):
        f_o = bsc_core.StoragePathOpt(cls.FILE_PATH)
        if f_o.get_is_exists() is False:
            bsc_core.StorageFileOpt(cls.FILE_PATH).set_write(
                {}
            )
        #
        if f_o.get_is_exists() is True:
            configure = bsc_objects.Configure(
                value=f_o.path
            )
            exists_values = configure.get(key) or []
            #
            for i_value in values:
                if i_value not in exists_values:
                    #
                    exists_values.append(i_value)
            #
            configure.set(key, exists_values)
            configure.set_save_to(cls.FILE_PATH)
            return True
        return False
    @classmethod
    def get(cls, key):
        f_o = bsc_core.StoragePathOpt(cls.FILE_PATH)
        if f_o.get_is_exists() is True:
            configure = bsc_objects.Configure(
                value=f_o.path
            )
            return configure.get(key) or []
        return []
    @classmethod
    def get_latest(cls, key):
        f_o = bsc_core.StoragePathOpt(cls.FILE_PATH)
        if f_o.get_is_exists() is True:
            configure = bsc_objects.Configure(
                value=f_o.path
            )
            _ = configure.get(key) or []
            if _:
                return _[-1]


class SchemeHistories(object):
    def __init__(self, scheme_key):
        if System.get_is_windows():
            self._file_path = '{}/scheme/{}.yml'.format(
                bsc_configure.UserDirectory.WINDOWS,
                scheme_key
            )
        elif System.get_is_linux():
            self._file_path = '{}/scheme/{}.yml'.format(
                bsc_configure.UserDirectory.LINUX,
                scheme_key
            )
        else:
            raise SystemError()
        #
        f_o = bsc_core.StoragePathOpt(self._file_path)
        if f_o.get_is_exists() is False:
            bsc_core.StorageFileOpt(self._file_path).set_write(
                {}
            )

        self._configure = bsc_objects.Configure(
            value=f_o.path
        )


class OslShaderMtd(object):
    @classmethod
    def set_katana_ui_template_create(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StorageFileOpt(output_file_path)
        info = bsc_core.OslShaderMtd.get_info(file_path)
        if info:
            j2_template = utl_configure.Jinja.ARNOLD.get_template('katana-ui-template.j2')
            raw = j2_template.render(
                **info
            )
            # print(raw)
            output_file_opt.set_write(raw)
    @classmethod
    def set_maya_ui_template_create(cls, file_path, output_file_path):
        output_file_opt = bsc_core.StorageFileOpt(output_file_path)
        info = bsc_core.OslShaderMtd.get_info(file_path)
        if info:
            j2_template = utl_configure.Jinja.ARNOLD.get_template('maya-ui-template.j2')
            raw = j2_template.render(
                **info
            )
            output_file_opt.set_write(raw)


class HookMtd(object):
    @classmethod
    def set_cmd_run(cls, cmd):
        import urllib
        #
        from lxbasic import bsc_core
        #
        unique_id = bsc_core.UuidMtd.get_new()
        #
        hook_yml_file_path = bsc_core.SystemMtd.get_user_session_file_path(unique_id=unique_id)
        #
        bsc_core.StorageFileOpt(hook_yml_file_path).set_write(
            dict(
                user=bsc_core.SystemMtd.get_user_name(),
                tiame=bsc_core.SystemMtd.get_time(),
                cmd=cmd,
            )
        )
        #
        urllib.urlopen(
            'http://{host}:{port}/cmd-run?uuid={uuid}'.format(
                **dict(
                    host=utl_configure.Hook.HOST,
                    port=utl_configure.Hook.PORT,
                    uuid=unique_id
                )
            )
        )


def _plf__get_is_windows_():
    return platform.system() == 'Windows'


def _plf__get_is_linux_():
    return platform.system() == 'Linux'


def _app__get_is_maya_():
    _ = os.environ.get('MAYA_APP_DIR')
    if _:
        return True
    return False


def _app__get_is_houdini_():
    _ = os.environ.get('HIP')
    if _:
        return True
    return False


def _debug_(fnc):
    def fnc_(*args, **kw):
        # noinspection PyBroadException
        try:
            return fnc(*args, **kw)
        except Exception:
            bsc_core.ExceptionMtd.set_print()
    return fnc_


def _print_time_(fnc):
    def fnc_(*args, **kwargs):
        start_timestamp = time.time()
        #
        message = u'start function: "{}.{}" at {}'.format(
            fnc.__module__,
            fnc.__name__,
            time.strftime(
                System.TIME_FORMAT,
                time.localtime(start_timestamp)
            )
        )
        print(message)

        _fnc = fnc(*args, **kwargs)

        end_timestamp = time.time()
        message = u'complete function: "{}.{}" at {} use {}s'.format(
            fnc.__module__,
            fnc.__name__,
            time.strftime(
                System.TIME_FORMAT,
                time.localtime(end_timestamp)
            ),
            (end_timestamp - start_timestamp)
        )
        print(message)
        return _fnc
    return fnc_


def _run_ignore_(fnc):
    def fnc_(*args, **kwargs):
        if isinstance(fnc, types.FunctionType):
            fnc_path = '{}'.format(
                fnc.__name__
            )
        elif isinstance(fnc, types.MethodType):
            fnc_path = '{}.{}'.format(
                fnc.__class__.__name__, fnc.__name__
            )
        else:
            raise TypeError()
        # noinspection PyBroadException
        try:
            Log.set_module_result_trace(
                'fnc run',
                'fnc="{}" is started'.format(
                    fnc_path
                ),
            )
            #
            _result = fnc(*args, **kwargs)
            #
            Log.set_module_result_trace(
                'fnc run',
                'fnc="{}" is completed'.format(
                    fnc_path
                )
            )
        except:
            Log.set_module_error_trace(
                'fnc run',
                'fnc="{}" is error'.format(
                    fnc_path
                )
            )
            bsc_core.ExceptionMtd.set_print()
    return fnc_


def _print_fnc_completion_with_result_(fnc):
    def fnc_(*args, **kwargs):
        if isinstance(fnc, types.FunctionType):
            fnc_path = '{}'.format(
                fnc.__name__
            )
        elif isinstance(fnc, types.MethodType):
            fnc_path = '{}.{}'.format(
                fnc.__class__.__name__, fnc.__name__
            )
        else:
            raise TypeError()
        # noinspection PyBroadException
        try:
            Log.set_module_result_trace(
                'fnc run',
                'fnc="{}" is started'.format(
                    fnc_path
                ),
            )
            #
            _result = fnc(*args, **kwargs)
            #
            if _result is True:
                Log.set_module_result_trace(
                    'fnc run',
                    'fnc="{}" is completed'.format(
                        fnc_path
                    )
                )
            else:
                Log.set_module_warning_trace(
                    'fnc run',
                    'fnc="{}" is failed'.format(
                        fnc_path
                    )
                )
        except:
            Log.set_module_error_trace(
                'fnc run',
                'fnc="{}" is error'.format(
                    fnc_path
                )
            )
            bsc_core.ExceptionMtd.set_print()
    return fnc_


class Resources(object):
    ENVIRON_KEY = 'LYNXI_RESOURCES'
    @classmethod
    def get_search_paths(cls):
        return Environ.get_as_array(
            cls.ENVIRON_KEY
        )
    @classmethod
    def get(cls, sub_key):
        for i_path in cls.get_search_paths():
            i_path_opt = bsc_core.StoragePathOpt(i_path)
            if i_path_opt.get_is_exists() is True:
                i_glob_pattern = '{}/{}'.format(i_path_opt.path, sub_key)
                i_results = Path._get_stg_paths_by_parse_pattern_(
                    i_glob_pattern
                )
                if i_results:
                    return i_results[0]
    @classmethod
    def get_all(cls, sub_key):
        for i_path in cls.get_search_paths():
            i_path_opt = bsc_core.StoragePathOpt(i_path)
            if i_path_opt.get_is_exists() is True:
                i_glob_pattern = '{}/{}'.format(i_path_opt.path, sub_key)
                i_results = Path._get_stg_paths_by_parse_pattern_(
                    i_glob_pattern
                )
                return i_results


if __name__ == '__main__':
    KatanaLauncher(project='cgm').set_file_new(
        '/l/prod/cgm/work/assets/prp/car_b/mod/modeling/katana/car_b.mod.modeling.v001.katana'
    )
