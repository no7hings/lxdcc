# coding:utf-8
from __future__ import print_function

import six

import sys

import platform

import os

import threading

import time

import types

import subprocess

import functools

import copy

import lxbasic.core as bsc_core

import lxcontent.core as ctt_core

import lxgui.core as gui_core

DccDialog = gui_core.GuiDialog


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
    def execute_with_result(cls, cmd, **sub_progress_kwargs):
        bsc_core.Log.trace_method_result(
            'sub-process',
            'start for: `{}`'.format(cmd)
        )
        bsc_core.SubProcessMtd.execute_with_result(
            cmd, **sub_progress_kwargs
        )
        bsc_core.Log.trace_method_result(
            'sub-process',
            'complete for: `{}`'.format(cmd)
        )

    @classmethod
    def set_run(cls, cmd):
        bsc_core.Log.trace_method_result(
            'sub-process',
            'execute for: `{}`'.format(cmd)
        )
        return bsc_core.SubProcessMtd.set_run(
            cmd
        )

    @classmethod
    def set_run_with_result_use_thread(cls, cmd, **sub_progress_kwargs):
        t_0 = threading.Thread(
            target=functools.partial(
                cls.execute_with_result,
                cmd=cmd,
                **sub_progress_kwargs
            )
        )
        t_0.start()
        # t_0.join()

    @classmethod
    def set_run_with_result_use_log(cls):
        pass


class DDlMonitor(object):
    @classmethod
    def set_create(cls, label, job_id, parent=None):
        import lxgui.proxy.widgets as prx_widgets

        import lxwarp.deadline.core as ddl_core

        w = prx_widgets.PrxMonitorWindow(parent=parent)
        w.set_window_title(
            '{}({})'.format(
                label, job_id
            )
        )
        button = w.get_status_button()
        j_m = ddl_core.DdlJobMonitor(job_id)
        button.set_statuses(j_m.get_task_statuses())
        button.set_initialization(j_m.get_task_count())
        j_m.logging.connect_to(w.set_logging)
        j_m.task_status_changed_at.connect_to(w.set_status_at)
        j_m.task_finished_at.connect_to(w.set_finished_at)
        j_m.set_start()

        w.connect_window_close_to(j_m.set_stop)

        w.set_window_show(size=(480, 240))


class CommandMonitor(object):
    @classmethod
    def set_create(cls, label, command, parent=None):
        def completed_fnc_(*args):
            w.set_status(w.ValidationStatus.Correct)
            w.close_window_later()

        def failed_fnc_(*args):
            w.set_status(w.ValidationStatus.Error)

        def finished_fnc_(*args):
            pass

        import lxgui.qt.core as gui_qt_core

        import lxgui.proxy.widgets as prx_widgets

        w = prx_widgets.PrxMonitorWindow(parent=parent)
        w.set_window_title(label)
        #
        status_button = w.get_status_button()
        c_t = bsc_core.TrdCommand(command)
        status_button.set_statuses([c_t.get_status()])
        status_button.set_initialization(1)
        c_t.status_changed.connect_to(lambda x: w.set_status_at(0, x))
        # c_t.finished.connect_to(lambda x: w.set_finished_at(0, x))
        c_t.logging.connect_to(w.set_logging)
        w.connect_window_close_to(c_t.set_stopped)
        #
        q_c_s = gui_qt_core.QtCommandSignals(w.widget)
        #
        c_t.completed.connect_to(q_c_s.completed.emit)
        c_t.finished.connect_to(q_c_s.finished.emit)
        c_t.failed.connect_to(q_c_s.failed.emit)
        #
        q_c_s.completed.connect(completed_fnc_)
        q_c_s.failed.connect(failed_fnc_)
        q_c_s.finished.connect(finished_fnc_)
        #
        c_t.start()

        w.set_window_show(size=(480, 240))
        return q_c_s


class System(object):
    @classmethod
    def get_user_name(cls):
        return bsc_core.SystemMtd.get_user_name()

    @classmethod
    def get_time(cls):
        return bsc_core.SystemMtd.get_time()

    @classmethod
    def get_time_tag(cls):
        return bsc_core.TimeMtd.get_time_tag()


class Environ(object):
    TD_ENABLE_KEY = 'LYNXI_TD_ENABLE'
    #
    TRUE = 'true'
    FALSE = 'false'

    def __init__(self):
        pass

    @classmethod
    def get_is_td_enable(cls):
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
        bsc_core.Log.trace_method_result(
            'environ set',
            u'key="{}", value="{}"'.format(key, value)
        )

    @classmethod
    def append(cls, key, value):
        if key in os.environ:
            v = os.environ[key]
            if value not in v:
                os.environ[key] += os.pathsep+value
                bsc_core.Log.trace_method_result(
                    'environ add',
                    u'key="{}", value="{}"'.format(key, value)
                )
        else:
            os.environ[key] = value
            bsc_core.Log.trace_method_result(
                'environ-set',
                u'key="{}", value="{}"'.format(key, value)
            )


class File(object):
    @classmethod
    def set_write(cls, file_path, raw):
        with bsc_core.LogContext.create('file write', 'file="{}"'.format(file_path)):
            bsc_core.StgFileOpt(
                file_path
            ).set_write(raw)

    @classmethod
    def set_read(cls, file_path):
        with bsc_core.LogContext.create('file read', 'file="{}"'.format(file_path)):
            return bsc_core.StgFileOpt(
                file_path
            ).set_read()


class AppLauncher(object):
    # TODO fix 9.9.9
    LOCAL_ROOT = '{}/packages/pglauncher/9.9.99'.format(bsc_core.SystemMtd.get_home_directory())
    SERVER_ROOT = '/l/packages/pg/prod/pglauncher/9.9.9'
    #
    PROJECT_CONFIGURE_DIRECTORY_PATTERN = '{root}/{project}_config'
    APP_CONFIGURE_FILE_PATTERN = '{root}/{project}_config/bin/config/{application}.yml'
    APP_CONFIGURE_FILE_PATTERNS = [
        '{root}/{project}_config/bin/config/{application}.yml',
        '{root}/{project}_config/config/{application}.yml'
    ]
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
        if bsc_core.StgPathOpt(self.LOCAL_ROOT).get_is_exists():
            self._root = bsc_core.StgPathMapper.map_to_current(self.LOCAL_ROOT)
        else:
            self._root = bsc_core.StgPathMapper.map_to_current(self.SERVER_ROOT)
        #
        self._kwargs = dict(
            root=self._root,
            project=kwargs['project'],
            application=kwargs['application']
        )

    @classmethod
    def get_server_root(cls):
        pass

    @classmethod
    def _get_application_configure_file_path_(cls, **kwargs):
        kwargs_ = copy.copy(kwargs)
        application = kwargs['application']
        if application in cls.APP_CONFIGURE_MAP_DICT:
            application_ = cls.APP_CONFIGURE_MAP_DICT[application]
            kwargs_['application'] = application_
        for i_p in cls.APP_CONFIGURE_FILE_PATTERNS:
            i_file_path = i_p.format(
                **kwargs_
            )
            if os.path.exists(i_file_path) is True:
                return i_file_path

    @classmethod
    def _set_cmd_run_(cls, *args):
        SubProcessRunner.set_run(
            ' '.join(['rez-env']+list(args))
        )

    @classmethod
    def _get_run_cmd_(cls, *args):
        return ' '.join(['rez-env']+list(args))

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
        if configure_file_path:
            bsc_core.Log.trace_method_result(
                'launcher-configure search',
                'project="{project}", application="{application}"'.format(
                    **kwargs
                )
            )
            configure = ctt_core.Content(value=configure_file_path)
            keys = configure.get_all_leaf_keys()
            for key in keys:
                i_run_args = configure.get(key)
                lis.extend(i_run_args)
        else:
            bsc_core.Log.trace_method_warning(
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

    # run methods
    @classmethod
    def _set_run_with_result_as_rez_(cls, *run_args, **sub_progress_kwargs):
        SubProcessRunner.execute_with_result(
            ' '.join(['rez-env']+list(run_args)),
            **sub_progress_kwargs
        )

    @classmethod
    def _set_run_with_result_use_thread_as_rez_(cls, *run_args, **sub_progress_kwargs):
        SubProcessRunner.set_run_with_result_use_thread(
            ' '.join(['rez-env']+list(run_args)),
            **sub_progress_kwargs
        )

    #
    def set_cmd_run_with_result_as_rez(self, extend_cmd, **sub_progress_kwargs):
        run_args = self.get_rez_packages()
        #
        run_args.append(extend_cmd)
        self._set_run_with_result_as_rez_(
            *run_args, **sub_progress_kwargs
        )

    def set_cmd_run_with_result(self, extend_cmd, **sub_progress_kwargs):
        self.set_cmd_run_with_result_as_rez(extend_cmd, **sub_progress_kwargs)

    def set_cmd_run_with_result_use_thread_as_rez(self, extend_cmd, **sub_progress_kwargs):
        run_args = self.get_rez_packages()
        #
        run_args.append(extend_cmd)
        self._set_run_with_result_use_thread_as_rez_(
            *run_args, **sub_progress_kwargs
        )

    def set_cmd_run_with_result_use_thread(self, extend_cmd, **sub_progress_kwargs):
        self.set_cmd_run_with_result_use_thread_as_rez(extend_cmd, **sub_progress_kwargs)

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

    def open_file(self, file_path):
        args = [
            '-- maya',
            r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_open_as_project(\\\"{}\\\")\")"'.format(
                file_path
            )
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
            cmd
        )

    def new_file(self, file_path):
        args = [
            '-- maya',
            r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.set_file_path_as_project(\\\"{}\\\", with_create_directory=True)\")"'.format(
                file_path
            )
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
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
            # r'-command "python(\"import lxmaya.dcc.dcc_objects as mya_dcc_objects; mya_dcc_objects.Scene.open_file(\\\"{}\\\")\")"'.format(
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
        cmd = ' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
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
        option_opt = bsc_core.ArgDictStringOpt(self._option)
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

    def open_file(self, file_path):
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

    def set_run(self):
        args = [
            '-- houdini',
        ]
        cmd = ' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
            cmd
        )

    def get_rez_packages(self):
        return AppLauncher(
            **self._kwargs
        ).get_rez_packages()


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

    def open_file(self, file_path):
        args = [
            '-- katana',
            '"{}"'.format(file_path)
        ]
        cmd = ' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
            cmd
        )

    def new_file(self, file_path):
        from lxkatana import ktn_configure

        create_args = [
            '-c'
            '"katana --script={} \"set_scene_new\" \"{}\""'.format(
                ktn_configure.Data.SCRIPT_FILE, file_path
            )
        ]
        cmd = ' '.join(create_args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_as_rez(
            cmd
        )
        self.open_file(file_path)

    def set_run(self):
        args = [
            '-- katana',
        ]
        cmd = ' '.join(args)
        #
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
            cmd
        )

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

    def open_file(self, file_path):
        # rez-env arnold_usd-6.1.0.1 arnold-6.1.0.1 aces pyside2 pgusd usd-20.11
        args = [
            # 'pgtk',
            # 'shotgun',
            'usd-20.11',
            #
            '-- usdview',
            '--render "GL" --camera "/renderCamera/defaultCamera/defaultCameraLeft/defaultCameraLeftShape"',
            '"{}"'.format(file_path),
        ]
        cmd = ' '.join(args)
        AppLauncher(**self._kwargs).set_cmd_run_with_result_use_thread_as_rez(
            cmd
        )


class DccModifier(object):
    @staticmethod
    def run_as_ignore(fnc):
        def fnc_(*args, **kw):
            # noinspection PyBroadException
            try:
                return fnc(*args, **kw)
            except Exception:
                bsc_core.ExceptionMtd.set_print()

        return fnc_

    @staticmethod
    def run_with_time_trace(fnc):
        def fnc_(*args, **kwargs):
            start_timestamp = time.time()
            #
            message = u'start function: "{}.{}" at {}'.format(
                fnc.__module__,
                fnc.__name__,
                time.strftime(
                    bsc_core.TimeMtd.TIME_FORMAT,
                    time.localtime(start_timestamp)
                )
            )
            bsc_core.SystemMtd.trace(message)

            _result = fnc(*args, **kwargs)

            end_timestamp = time.time()
            message = u'complete function: "{}.{}" at {} use {}s'.format(
                fnc.__module__,
                fnc.__name__,
                time.strftime(
                    bsc_core.TimeMtd.TIME_FORMAT,
                    time.localtime(end_timestamp)
                ),
                (end_timestamp-start_timestamp)
            )
            bsc_core.SystemMtd.trace(message)
            return _result

        return fnc_

    @staticmethod
    def run_with_result_trace(fnc):
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
                bsc_core.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is started'.format(
                        fnc_path
                    ),
                )
                #
                _result = fnc(*args, **kwargs)
                #
                bsc_core.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is completed'.format(
                        fnc_path
                    )
                )
                return _result
            except Exception:
                bsc_core.Log.trace_method_error(
                    'fnc run',
                    'fnc="{}" is error'.format(
                        fnc_path
                    )
                )
                bsc_core.ExceptionMtd.set_print()

        return fnc_

    @staticmethod
    def run_with_result_trace_extra(fnc):
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
                bsc_core.Log.trace_method_result(
                    'fnc run',
                    'fnc="{}" is started'.format(
                        fnc_path
                    ),
                )
                #
                _result = fnc(*args, **kwargs)
                #
                if _result is True:
                    bsc_core.Log.trace_method_result(
                        'fnc run',
                        'fnc="{}" is completed'.format(
                            fnc_path
                        )
                    )
                else:
                    bsc_core.Log.trace_method_warning(
                        'fnc run',
                        'fnc="{}" is failed'.format(
                            fnc_path
                        )
                    )
                return _result
            except Exception:
                bsc_core.Log.trace_method_error(
                    'fnc run',
                    'fnc="{}" is error'.format(
                        fnc_path
                    )
                )
                bsc_core.ExceptionMtd.set_print()

        return fnc_

    @staticmethod
    def run_with_exception_catch(fnc):
        def fnc_(*args, **kwargs):
            # noinspection PyBroadException
            try:
                _result = fnc(*args, **kwargs)
                return _result
            except Exception:
                import lxbasic.core as bsc_core
                bsc_core.LogException.trace()
                raise

        return fnc_


def get_is_ui_mode():
    if bsc_core.ApplicationMtd.get_is_maya():
        from lxmaya import ma_core
        return ma_core.get_is_ui_mode()
    elif bsc_core.ApplicationMtd.get_is_katana():
        from lxkatana import ktn_core
        return ktn_core.get_is_ui_mode()
    return False


if __name__ == '__main__':
    pass