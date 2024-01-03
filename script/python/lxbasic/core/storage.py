# coding:utf-8
import parse

import time

import six

import os

import collections

import xmlrpclib

import threading

import re

import fnmatch

import functools

import glob

import shutil

import json

import subprocess

import gzip

import zipfile

import uuid

import lxbasic.log as bsc_log

import lxcontent.core as ctt_core

from ..core import base as bsc_cor_base

from ..core import raw as bsc_cor_raw

from ..core import raw_for_dict as bsc_cor_raw_for_dict

from ..core import path as bsc_cor_path

from ..core import pattern as bsc_cor_pattern

from ..core import time_ as bsc_cor_time

from ..core import environ as bsc_cor_environ

from ..core import process as bsc_cor_process

from ..core import thread as bsc_cor_thread


class StgRpcMtd(object):
    RPC_SERVER = '10.10.206.117'
    RPC_PORT = 58888
    PATHSEP = '/'

    KEY = 'rpc'

    @classmethod
    def get_client(cls, port_addition=0):
        return xmlrpclib.ServerProxy(
            'http://{0}:{1}'.format(cls.RPC_SERVER, cls.RPC_PORT+port_addition)
        )

    @classmethod
    def create_directory(cls, directory_path, mode='775'):
        units = bsc_cor_path.PthNodeMtd.get_dag_component_paths(directory_path)
        units.reverse()
        list_ = []
        for i_path in units:
            if i_path != cls.PATHSEP:
                if os.path.exists(i_path) is False:
                    list_.append(i_path)
        #
        for i in list_:
            cls._create_directory_fnc_(i, mode)

    @classmethod
    def _create_directory_fnc_(cls, directory_path, mode='775'):
        key = 'rpc create directory'
        if os.path.exists(directory_path) is False:
            timeout = 25
            cost_time = 0
            start_time = time.time()
            clt = cls.get_client()
            clt.mkdir(directory_path, mode)
            p = os.path.dirname(directory_path)
            while os.path.exists(directory_path) is False:
                cost_time = int(time.time()-start_time)
                if cost_time > timeout:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            key,
                            'path="{}" is timeout, cost time {}s'.format(directory_path, cost_time)
                        )
                    )
                #
                if bsc_cor_base.SysBaseMtd.get_is_linux():
                    os.system('ls {} > /dev/null'.format(p))
                #
                time.sleep(1)
            #
            bsc_log.Log.trace_method_result(
                key,
                'path="{}" is cost time {}s'.format(directory_path, cost_time)
            )
            # noinspection PyArgumentEqualDefault
            cls.change_owner(
                directory_path,
                user='artist', group='artists'
            )
        return True

    @classmethod
    def delete(cls, file_path):
        if os.path.exists(file_path) is True:
            timeout = 25
            cost_time = 0
            start_time = time.time()
            clt = cls.get_client()
            clt.rm_file(file_path)
            # delete, check is exists
            p = os.path.dirname(file_path)
            while os.path.exists(file_path) is True:
                cost_time = int(time.time()-start_time)
                if cost_time > timeout:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            'rpc delete',
                            'path="{}" is timeout, cost time {}s'.format(file_path, cost_time)
                        )
                    )
                #
                if bsc_cor_base.SysBaseMtd.get_is_linux():
                    os.system('ls {} > /dev/null'.format(p))
                #
                time.sleep(1)
            #
            bsc_log.Log.trace_method_result(
                'rpc delete',
                'path="{}" is completed, cost time {}s'.format(file_path, cost_time)
            )

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        key = 'rpc copy to file'
        if replace is True:
            if os.path.exists(file_path_tgt):
                pass
        #
        if os.path.exists(file_path_tgt) is False:
            directory_path_tgt = os.path.dirname(file_path_tgt)
            if os.path.exists(directory_path_tgt) is False:
                cls.create_directory(directory_path_tgt)

            timeout = 25
            cost_time = 0
            start_time = time.time()
            clt = cls.get_client()
            clt.copyfile(file_path_src, file_path_tgt)
            p = os.path.dirname(file_path_tgt)
            while os.path.exists(file_path_tgt) is False:
                cost_time = int(time.time()-start_time)
                if cost_time > timeout:
                    raise RuntimeError(
                        bsc_log.Log.trace_method_error(
                            key,
                            'path="{}" is timeout, cost time {}s'.format(file_path_tgt, cost_time)
                        )
                    )
                if bsc_cor_base.SysBaseMtd.get_is_linux():
                    os.system('ls {} > /dev/null'.format(p))
                #
                time.sleep(1)
            # noinspection PyArgumentEqualDefault
            cls.change_owner(
                file_path_tgt,
                user='artist', group='artists'
            )
            # noinspection PyArgumentEqualDefault
            cls.change_mode(
                file_path_tgt,
                mode='775'
            )
            #
            bsc_log.Log.trace_method_result(
                key,
                'path="{} >> {}", cost time {}s'.format(file_path_src, file_path_tgt, cost_time)
            )

    @classmethod
    def change_mode(cls, path, mode='775'):
        key = 'rpc change mode'
        if os.path.exists(path) is True:
            clt = cls.get_client()
            clt.chmod(path, mode)
            #
            if bsc_cor_base.SysBaseMtd.get_is_linux():
                p = os.path.dirname(path)
                os.system('ls {} > /dev/null'.format(p))
            #
            bsc_log.Log.trace_method_result(
                key,
                'path="{}", mode="{}"'.format(path, mode)
            )

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        key = 'rpc change owner'
        if os.path.exists(path) is True:
            clt = cls.get_client()
            clt.chown(path, user, group)
            p = os.path.dirname(path)
            if bsc_cor_base.SysBaseMtd.get_is_linux():
                os.system('ls {} > /dev/null'.format(p))
            bsc_log.Log.trace_method_result(
                key,
                'path="{}", user="{}", group="{}"'.format(path, user, group)
            )


class StgSshMtd(object):
    GROUP_ID_QUERY = {
        'cg_group': 20002,
        # 'cg_grp': 20002,
        'ani_grp': 20017,
        'rlo_grp': 20025,
        'flo_grp': 20026,
        'art_grp': 20010,
        'stb_grp': 20027,
        'cfx_grp': 20015,
        'efx_grp': 20016,
        'dmt_grp': 20020,
        'lgt_grp': 20018,
        'mod_grp': 20011,
        'grm_grp': 20012,
        'rig_grp': 20013,
        'srf_grp': 20014,
        'set_grp': 20023,
        'plt_grp': 20024,
        'edt_grp': 20028,
        #
        'coop_grp': 20032,
        #
        'td_grp': 20004,
    }
    CMD_QUERY = {
        'deny': 'chmod -R +a group {group_id} deny dir_gen_write,std_delete,delete_child,object_inherit,container_inherit "{path}"',
        'allow': 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"',
        'read_only': 'chmod -R +a group {group_id} allow dir_gen_read,dir_gen_execute,object_inherit,container_inherit "{path}"',
        'read_only-0': 'chmod -R +a group {group_id} allow dir_gen_read,dir_gen_execute,object_inherit,container_inherit "{path}"',
        'show_grp': 'ls -led "{path}"',
        'remove_grp': 'chmod -R -a# {index} "{path}"',
        'file_allow': 'chmod -R +a group {group_id} allow file_gen_all,object_inherit,container_inherit "{path}"',
    }
    GROUP_PATTERN = r' {index}: group:DIEZHI\{group} {context}'
    USER_PATTERN = r' {index}: user:DIEZHI\{user} {context}'
    #
    HOST = 'isilon.diezhi.local'
    USER = 'root'

    # noinspection PyAugmentAssignment
    class MakePassword(object):
        def __init__(self, key, s):
            self.key = key
            self.s = s

        def encrypt(self):
            b = bytearray(str(self.s).encode("utf-8"))
            n = len(b)
            c = bytearray(n*2)
            j = 0
            for i in range(0, n):
                b1 = b[i]
                b2 = b1 ^ self.key
                c1 = b2%16
                c2 = b2//16
                c1 = c1+65
                c2 = c2+65
                c[j] = c1
                c[j+1] = c2
                j = j+2
            return c.decode("utf-8")

        def decrypt(self):
            c = bytearray(str(self.s).encode("utf-8"))
            n = len(c)
            if n%2 != 0:
                return ""
            n = n//2
            b = bytearray(n)
            j = 0
            for i in range(0, n):
                c1 = c[j]
                c2 = c[j+1]
                j = j+2
                c1 = c1-65
                c2 = c2-65
                b2 = c2*16+c1
                b1 = b2^self.key
                b[i] = b1
            # noinspection PyBroadException
            try:
                return b.decode("utf-8")
            except Exception:
                return "failed"

    @classmethod
    def _set_nas_cmd_run_(cls, cmd):
        # noinspection PyUnresolvedReferences
        import paramiko

        #
        bsc_log.Log.trace_method_result(
            'nas-cmd-run',
            'command=`{}`'.format(cmd)
        )
        #
        password = StgSshMtd.MakePassword(120, 'KBHBOCCCMDMBKEBDCBKBLAKA')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=cls.HOST,
            username=cls.USER,
            password=password.decrypt().encode('utf-8'),
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        result = stdout.read()
        ssh.close()
        return result

    @classmethod
    def _get_all_group_data_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        print result
        dict_ = collections.OrderedDict()
        if result is not None:
            for i in result.split('\n'):
                i_p = parse.parse(r' {index}: group:DIEZHI\{group} {context}', i)
                if i_p:
                    i_dict = i_p.named
                    if i_dict:
                        dict_[i_dict['group']] = (i_dict['index'], i_dict['context'])
        return dict_

    @classmethod
    def _get_all_group_data_1_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        print result
        list_ = []
        if result is not None:
            for i in result.split('\n'):
                i_p = parse.parse(cls.GROUP_PATTERN, i)
                if i_p:
                    i_dict = i_p.named
                    if i_dict:
                        list_.append(
                            (i_dict['group'], i_dict['index'], i_dict['context'])
                        )
        return list_

    @classmethod
    def _get_all_user_data_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        print result
        list_ = []
        if result is not None:
            for i in result.split('\n'):
                i_p = parse.parse(cls.USER_PATTERN, i)
                if i_p:
                    i_dict = i_p.named
                    if i_dict:
                        list_.append(
                            (i_dict['user'], i_dict['index'], i_dict['context'])
                        )
        return list_

    @classmethod
    def _get_all_data_(cls, nas_path):
        kwargs = dict(
            path=nas_path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        result = cls._set_nas_cmd_run_(cmd)
        print result
        list_ = []
        if result is not None:
            for i in result.split('\n'):
                i_p_0 = parse.parse(cls.USER_PATTERN, i)
                if i_p_0:
                    i_dict = i_p_0.named
                    if i_dict:
                        list_.append(
                            (i_dict['user'], i_dict['index'], i_dict['context'])
                        )
                else:
                    i_p_1 = parse.parse(cls.GROUP_PATTERN, i)
                    if i_p_1:
                        i_dict = i_p_1.named
                        if i_dict:
                            list_.append(
                                (i_dict['group'], i_dict['index'], i_dict['context'])
                            )
        return list_


class StgSshOpt(StgSshMtd):
    def __init__(self, path):
        self._path = path
        self._nas_path = bsc_cor_base.StgBaseMtd.set_map_to_nas(path)

    def remove_all_group(self):
        group_data = self._get_all_group_data_1_(self._nas_path)
        group_data.reverse()
        for i_group_name, i_index, i_content in group_data:
            if i_group_name in self.GROUP_ID_QUERY:
                i_kwargs = dict(
                    path=self._nas_path,
                    index=i_index
                )
                i_cmd = self.CMD_QUERY['remove_grp'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)

    def set_read_only_for_groups(self, group_names):
        for i_group_name in group_names:
            if i_group_name in self.GROUP_ID_QUERY:
                i_group_id = self.GROUP_ID_QUERY[i_group_name]
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=self._nas_path,
                )
                i_cmd = self.CMD_QUERY['read_only'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)

    def set_just_read_only_for(self, group_names):
        self.remove_all_group()
        self.remove_all_user()
        self.set_read_only_for_groups(group_names)

    def get_all_group_data(self):
        return self._get_all_group_data_1_(self._nas_path)

    def get_all_user_data(self):
        return self._get_all_user_data_(self._nas_path)

    def remove_all_user(self):
        user_data = self._get_all_user_data_(self._nas_path)
        user_data.reverse()
        for i_user_name, i_index, i_content in user_data:
            print i_user_name, i_index
            i_kwargs = dict(
                path=self._nas_path,
                index=i_index
            )
            i_cmd = self.CMD_QUERY['remove_grp'].format(
                **i_kwargs
            )
            self._set_nas_cmd_run_(i_cmd)

    def get_all_data(self):
        return self._get_all_data_(self._nas_path)


class StgUserMtd(object):
    @classmethod
    def get_windows_home(cls):
        return '{}/{}'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', 'c:/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_home(cls):
        return '{}'.format(
            os.environ.get('HOME', '/temp')
        )

    @classmethod
    def get_home(cls):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            return cls.get_windows_home()
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            return cls.get_linux_home()
        else:
            raise SystemError()

    @classmethod
    def get_windows_user_directory(cls):
        return '{}{}/.lynxi'.format(
            os.environ.get('HOMEDRIVE', 'c:'),
            os.environ.get('HOMEPATH', '/temp')
        ).replace('\\', '/')

    @classmethod
    def get_linux_user_directory(cls):
        return '{}/.lynxi'.format(
            os.environ.get('HOME', '/temp')
        )

    @classmethod
    def get_user_directory(cls):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            return cls.get_windows_user_directory()
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            return cls.get_linux_user_directory()
        else:
            raise SystemError()

    @classmethod
    def get_user_temporary_directory(cls, create=False):
        date_tag = bsc_cor_base.SysBaseMtd.get_date_tag()
        _ = '{}/temporary/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if create:
            bsc_cor_base.StgBaseMtd.create_directory(_)
        return _

    @classmethod
    def get_user_debug_directory(cls, tag=None, create=False):
        date_tag = bsc_cor_base.SysBaseMtd.get_date_tag()
        _ = '{}/debug/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if tag is not None:
            _ = '{}/{}'.format(_, tag)
        if create:
            bsc_cor_base.StgBaseMtd.create_directory(_)
        return _

    @classmethod
    def get_user_batch_exception_directory(cls, tag, create=False):
        date_tag = bsc_cor_base.SysBaseMtd.get_date_tag()
        _ = '{}/batch-exception-log/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if tag is not None:
            _ = '{}/{}'.format(_, tag)
        if create:
            bsc_cor_base.StgBaseMtd.create_directory(_)
        return _

    @classmethod
    def get_user_log_directory(cls):
        date_tag = bsc_cor_base.SysBaseMtd.get_date_tag()
        return '{}/log/{}.log'.format(
            cls.get_user_directory(), date_tag
        )

    @classmethod
    def get_user_history_cache_file(cls):
        return '{}/history.yml'.format(
            cls.get_user_directory()
        )

    @classmethod
    def get_user_session_directory(cls, create=False):
        date_tag = bsc_cor_base.SysBaseMtd.get_date_tag()
        _ = '{}/.session/{}'.format(
            cls.get_user_directory(), date_tag
        )
        if create:
            bsc_cor_base.StgBaseMtd.create_directory(_)
        return _

    @classmethod
    def get_user_session_file(cls, unique_id=None):
        directory_path = cls.get_user_session_directory()
        if unique_id is None:
            unique_id = bsc_cor_base.UuidMtd.generate_new()
        return '{}/{}.yml'.format(directory_path, unique_id)


class StgSystem(object):
    @classmethod
    def open_directory(cls, path):
        path = bsc_cor_raw.auto_encode(path)
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            cmd = 'explorer "{}"'.format(path.replace('/', '\\'))
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            cmd = 'gio open "{}"'.format(path)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(
                bsc_cor_process.PrcBaseMtd.execute, cmd
            )
        )
        t_0.setDaemon(True)
        t_0.start()

    @classmethod
    def open_directory_force(cls, path):
        path = bsc_cor_raw.auto_encode(path)
        if os.path.exists(path) is False:
            path = StgExtraMtd.get_exists_component(path)

        cls.open_directory(path)

    @classmethod
    def open_file(cls, path):
        if bsc_cor_base.SysBaseMtd.get_is_windows():
            cmd = 'explorer /select,"{}"'.format(path.replace('/', '\\'))
        elif bsc_cor_base.SysBaseMtd.get_is_linux():
            cmd = 'nautilus "{}" --select'.format(path)
        else:
            raise SystemError()

        t_0 = threading.Thread(
            target=functools.partial(
                bsc_cor_process.PrcBaseMtd.execute, cmd
            )
        )
        t_0.setDaemon(True)
        t_0.start()

    @classmethod
    def open(cls, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                cls.open_directory(path)
            elif os.path.isfile(path):
                cls.open_file(path)
        else:
            component = StgExtraMtd.get_exists_component(path)
            if component:
                cls.open_directory(component)


class StgExtraMtd(object):
    @classmethod
    def get_exists_component(cls, path):
        units = bsc_cor_path.PthNodeMtd.get_dag_component_paths(path)
        for i in units:
            if os.path.exists(i):
                return i

    @classmethod
    def get_paths_by_fnmatch_pattern(cls, pattern, sort_by='number'):
        _ = glob.glob(pattern) or []
        if _:
            # fix windows path
            if bsc_cor_base.SysBaseMtd.get_is_windows():
                _ = map(lambda x: x.replace('\\', '/'), _)
            if len(_) > 1:
                # sort by number
                if sort_by == 'number':
                    _.sort(key=lambda x: bsc_cor_raw.RawTextMtd.to_number_embedded_args(x))
        return _

    @classmethod
    def create_directory(cls, directory_path):
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)
            bsc_log.Log.trace_method_result(
                'create-directory',
                'directory="{}"'.format(directory_path)
            )


class StgPathLinkMtd(object):
    @classmethod
    def link_to(cls, path_src, path_tgt):
        if os.path.exists(path_tgt) is False:
            tgt_dir_path = os.path.dirname(path_tgt)
            src_rel_path = os.path.relpath(path_src, tgt_dir_path)
            os.symlink(src_rel_path, path_tgt)

    @classmethod
    def get_is_link_source_to(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        src_rel_path = os.path.relpath(path_src, tgt_dir_path)
        if os.path.islink(path_tgt):
            orig_src_rel_path = os.readlink(path_tgt)
            return src_rel_path == orig_src_rel_path
        return False

    @classmethod
    def get_rel_path(cls, path_src, path_tgt):
        tgt_dir_path = os.path.dirname(path_tgt)
        return os.path.relpath(path_src, tgt_dir_path)

    @classmethod
    def get_is_link(cls, path):
        return os.path.islink(path)

    @classmethod
    def get_link_source(cls, path_tgt):
        cur_path = path_tgt
        while True:
            if os.path.exists(cur_path):
                if os.path.islink(cur_path) is True:
                    cur_directory_path = os.path.dirname(cur_path)
                    os.chdir(cur_directory_path)
                    cur_path = os.path.abspath(os.readlink(cur_path))
                else:
                    break
            else:
                break
        return cur_path

    @classmethod
    def link_file_to(cls, path_src, path_tgt):
        if os.path.isfile(path_src):
            if os.path.islink(path_src):
                path_src = cls.get_link_source(path_src)
            #
            if os.path.exists(path_tgt) is False:
                tgt_dir_path = os.path.dirname(path_tgt)
                src_rel_path = os.path.relpath(path_src, tgt_dir_path)
                os.symlink(src_rel_path, path_tgt)


class StgDirectoryMtd(object):
    @classmethod
    def get_file_paths(cls, directory_path, ext_includes=None):
        list_ = []
        if os.path.isdir(directory_path):
            results = os.listdir(directory_path) or []
            for i_name in results:
                i_path = '{}/{}'.format(directory_path, i_name)
                if os.path.isfile(i_path):
                    if isinstance(ext_includes, (tuple, list)):
                        i_name_base, i_ext = os.path.splitext(i_name)
                        if i_ext not in ext_includes:
                            continue
                    #
                    list_.append(i_path)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def _get_file_paths(cls, directory_path, ext_includes=None):
        import scandir

        list_ = []
        # make sure is a directory
        if os.path.isdir(directory_path):
            if StgPathMtd.get_is_readable(directory_path) is True:
                for i in scandir.scandir(directory_path):
                    if i.is_file():
                        i_path = i.path
                        if isinstance(ext_includes, (tuple, list)):
                            i_base, i_ext = os.path.splitext(i_path)
                            if i_ext not in ext_includes:
                                continue
                        #
                        list_.append(i_path)
            else:
                bsc_log.Log.trace_error(
                    'unreadable directory: "{}"'.format(
                        directory_path
                    )
                )
        if list_:
            list_.sort()
        return list_

    @classmethod
    def get_file_paths__(cls, directory_path, ext_includes=None):
        if bsc_cor_base.SysBaseMtd.get_is_linux():
            return cls._get_file_paths(directory_path, ext_includes)
        else:
            return cls.get_file_paths(directory_path, ext_includes)

    @classmethod
    def get_all_file_paths(cls, directory_path, ext_includes=None):
        def rcs_fnc_(path_):
            _results = os.listdir(path_) or []
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isfile(_i_path):
                    if isinstance(ext_includes, (tuple, list)):
                        _i_name_base, _i_ext = os.path.splitext(_i_name)
                        if _i_ext not in ext_includes:
                            continue
                    #
                    list_.append(_i_path)
                elif os.path.isdir(_i_path):
                    rcs_fnc_(_i_path)

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def _get_all_file_paths(cls, directory_path, ext_includes=None):
        def rcs_fnc_(path_):
            if StgPathMtd.get_is_readable(path_) is True:
                for _i in scandir.scandir(path_):
                    _i_path = _i.path
                    if _i.is_file():
                        if isinstance(ext_includes, (tuple, list)):
                            _i_base, _i_ext = os.path.splitext(_i_path)
                            if _i_ext not in ext_includes:
                                continue
                        #
                        list_.append(_i_path)
                    elif _i.is_dir():
                        rcs_fnc_(_i_path)
            else:
                bsc_log.Log.trace_error(
                    'unreadable directory: "{}"'.format(
                        path_
                    )
                )

        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def get_all_file_paths__(cls, directory_path, ext_includes=None):
        if bsc_cor_base.SysBaseMtd.get_is_linux():
            return cls._get_all_file_paths(directory_path, ext_includes)
        else:
            return cls.get_all_file_paths(directory_path, ext_includes)

    @classmethod
    def get_directory_paths(cls, directory_path):
        list_ = []
        if os.path.isdir(directory_path):
            results = os.listdir(directory_path) or []
            # results.sort()
            for i_name in results:
                i_path = '{}/{}'.format(directory_path, i_name)
                if os.path.isdir(i_path):
                    list_.append(i_path)
        return list_

    @classmethod
    def _get_directory_paths(cls, directory_path):
        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            if StgPathMtd.get_is_readable(directory_path) is True:
                for i in scandir.scandir(directory_path):
                    if i.is_dir():
                        list_.append(i.path)
            else:
                bsc_log.Log.trace_error(
                    'unreadable directory: "{}"'.format(
                        directory_path
                    )
                )
        return list_

    @classmethod
    def get_directory_paths__(cls, directory_path):
        if bsc_cor_base.SysBaseMtd.get_is_linux():
            return cls._get_directory_paths(directory_path)
        else:
            return cls.get_directory_paths(directory_path)

    @classmethod
    def get_all_directory_paths(cls, directory_path):
        def rcs_fnc_(path_):
            _results = os.listdir(path_) or []
            for _i_name in _results:
                _i_path = '{}/{}'.format(path_, _i_name)
                if os.path.isdir(_i_path):
                    list_.append(_i_path)
                    rcs_fnc_(_i_path)

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def _get_all_directory_paths(cls, directory_path):
        def rcs_fnc_(path_):
            if StgPathMtd.get_is_readable(path_) is True:
                for _i in scandir.scandir(path_):
                    if _i.is_dir():
                        _i_path = _i.path
                        list_.append(_i_path)
                        rcs_fnc_(_i_path)
            else:
                bsc_log.Log.trace_error(
                    'unreadable directory: "{}"'.format(
                        path_
                    )
                )

        # noinspection PyUnresolvedReferences
        import scandir

        list_ = []
        if os.path.isdir(directory_path):
            rcs_fnc_(directory_path)
        if list_:
            list_.sort()
        return list_

    @classmethod
    def get_all_directory_paths__(cls, directory_path):
        if bsc_cor_base.SysBaseMtd.get_is_linux():
            return cls._get_all_directory_paths(directory_path)
        else:
            return cls.get_all_directory_paths(directory_path)

    @classmethod
    def get_file_relative_path(cls, directory_path, file_path):
        return os.path.relpath(file_path, directory_path)

    @classmethod
    def set_copy_to(cls, src_directory_path, directory_path_tgt, excludes=None):
        def copy_fnc_(src_file_path_, tgt_file_path_):
            shutil.copy2(src_file_path_, tgt_file_path_)
            bsc_log.Log.trace_method_result(
                'file copy',
                'file="{}" >> "{}"'.format(src_file_path_, tgt_file_path_)
            )

        #
        src_directory_path = src_directory_path
        file_paths = cls.get_all_file_paths__(src_directory_path)
        #
        threads = []
        for i_src_file_path in file_paths:
            i_local_file_path = i_src_file_path[len(src_directory_path):]
            #
            if isinstance(excludes, (tuple, list)):
                is_match = False
                for j in excludes:
                    if fnmatch.filter([i_local_file_path], j):
                        is_match = True
                        break
                #
                if is_match is True:
                    continue
            #
            i_tgt_file_path = directory_path_tgt+i_local_file_path
            if os.path.exists(i_tgt_file_path) is False:
                i_tgt_dir_path = os.path.dirname(i_tgt_file_path)
                if os.path.exists(i_tgt_dir_path) is False:
                    os.makedirs(i_tgt_dir_path)
                #
                i_thread = bsc_cor_thread.TrdFnc(
                    copy_fnc_, i_src_file_path, i_tgt_file_path
                )
                threads.append(i_thread)
                i_thread.start()
        #
        [i.join() for i in threads]

    @classmethod
    def get_file_paths_by_pattern__(cls, directory_path, name_pattern):
        path_pattern = '{}/{}'.format(directory_path, name_pattern)
        return fnmatch.filter(
            cls.get_file_paths__(directory_path), path_pattern
        )

    @classmethod
    def find_file_paths(cls, glob_pattern):
        return fnmatch.filter(
            cls.get_file_paths__(os.path.dirname(glob_pattern)), glob_pattern
        )


class StgDirectoryMtdForMultiply(object):
    @classmethod
    def get_all_multiply_file_dict(cls, directory_path, name_pattern):
        dic = collections.OrderedDict()
        _ = StgDirectoryMtd.get_all_file_paths__(directory_path)
        for i_file_path in _:
            i_opt = StgFileOpt(i_file_path)
            i_number_args = StgFileMtdForMultiply.get_number_args(
                i_opt.name, name_pattern
            )
            if i_number_args:
                i_pattern, i_numbers = i_number_args
                if len(i_numbers) == 1:
                    i_relative_path_dir_path = StgDirectoryMtd.get_file_relative_path(
                        directory_path, i_opt.directory_path
                    )
                    i_key = '{}/{}'.format(
                        i_relative_path_dir_path, i_pattern
                    )
                    dic.setdefault(
                        i_key, []
                    ).append(i_numbers[0])
        return dic


class StgFileMtd(object):
    @classmethod
    def get_directory(cls, file_path):
        return os.path.dirname(file_path)

    @classmethod
    def get_is_exists(cls, file_path):
        return os.path.isfile(file_path)

    @classmethod
    def get_ext(cls, file_path):
        return os.path.splitext(file_path)[-1]


class StgFileMtdForMultiply(object):
    """
    methods using for multiply file
    etc. "/tmp/image.1001.exr" convert to "/tmp/image.####.exr"
    """
    PATHSEP = bsc_cor_pattern.PtnMultiplyFileMtd.PATHSEP
    P = '[0-9]'
    CACHE = dict()

    @classmethod
    def get_number_args(cls, file_name, name_pattern):
        new_file_name = file_name
        args = bsc_cor_pattern.PtnMultiplyFileMtd.get_args(
            name_pattern
        )
        if args:
            re_pattern = bsc_cor_pattern.PtnMultiplyFileMtd.to_re_style(name_pattern)
            results = re.findall(re_pattern, file_name)
            if results:
                if len(args) > 1:
                    numbers = results[0]
                else:
                    numbers = results
                #
                for i, (i_key, i_count) in enumerate(args):
                    new_file_name = new_file_name.replace(
                        numbers[i], i_key, 1
                    )
                return new_file_name, map(int, numbers)

    @classmethod
    def merge_to(cls, file_paths, name_patterns):
        list_ = []
        for i_file_path in file_paths:
            i_file_path = cls.convert_to(i_file_path, name_patterns)
            if i_file_path not in list_:
                list_.append(i_file_path)
        return list_

    @classmethod
    def convert_to(cls, file_path, name_patterns):
        """
        use for convert "/tmp/image.1001.exr" to "/tmp/image.####.exr"
        :param file_path:
        :param name_patterns: list[str, ...]
        etc. *.####.{format}, ext like "exr", "jpg"
        :return:
        """
        file_opt = StgFileOpt(file_path)
        for i_name_pattern in name_patterns:
            i_name_pattern = i_name_pattern.format(
                **dict(format=file_opt.get_format())
            )
            if bsc_cor_pattern.PtnMultiplyFileMtd.get_is_valid(i_name_pattern):
                i_number_args = StgFileMtdForMultiply.get_number_args(
                    file_opt.name, i_name_pattern
                )
                if i_number_args:
                    i_file_name, _ = i_number_args
                    i_file_path = '{}/{}'.format(file_opt.directory_path, i_file_name)
                    return i_file_path
        return file_path

    @classmethod
    def to_glob_pattern(cls, name_base):
        if name_base in cls.CACHE:
            return cls.CACHE[name_base]
        #
        name_base_new = name_base
        for i_keyword, i_re_format, i_count in bsc_cor_pattern.PtnMultiplyFileMtd.RE_MULTIPLY_KEYS:
            i_results = re.finditer(i_re_format.format(i_keyword), name_base, re.IGNORECASE) or []
            for j_result in i_results:
                j_start, j_end = j_result.span()
                if i_count == -1:
                    s = cls.P
                else:
                    s = cls.P*i_count
                #
                name_base_new = name_base_new.replace(name_base[j_start:j_end], s, 1)
        cls.CACHE[name_base] = name_base_new
        return name_base_new

    @classmethod
    def get_exists_unit_paths(cls, file_path):
        if os.path.isfile(file_path):
            return [file_path]
        #
        name_base = os.path.basename(file_path)
        name_base_new = cls.to_glob_pattern(name_base)
        if name_base != name_base_new:
            directory_path = os.path.dirname(file_path)
            glob_pattern = cls.PATHSEP.join([directory_path, name_base_new])
            list_ = StgDirectoryMtd.find_file_paths(glob_pattern)
            return list_
        return []

    @classmethod
    def get_is_exists(cls, file_path):
        return not not cls.get_exists_unit_paths(file_path)


class StgPathMtd(bsc_cor_base.StgBaseMtd):
    @classmethod
    def get_parent(cls, path):
        return bsc_cor_path.PthNodeMtd.get_dag_parent_path(
            path
        )


class StgPathOpt(object):
    PATHSEP = '/'

    def __init__(self, path, cleanup=True):
        if cleanup is True:
            self._path = bsc_cor_base.StgBaseMtd.clear_pathsep_to(path)
        else:
            self._path = path
        #
        if self.get_is_windows():
            self._root = self._path.split(self.PATHSEP)[0]
        elif self.get_is_linux():
            self._root = self.PATHSEP
        else:
            self._root = '/'

        self.__gui = None

    def get_type_name(self):
        if self.get_is_file():
            return 'file'
        return 'directory'

    type_name = property(get_type_name)

    def get_type(self):
        return self.get_type_name()

    type = property(get_type)

    def get_path(self):
        return self._path

    path = property(get_path)

    def get_name(self):
        return os.path.basename(self.path)

    name = property(get_name)

    def get_root(self):
        return self._root

    root = property(get_root)

    @property
    def normcase_root(self):
        return os.path.normcase(self._root)

    @property
    def normcase_path(self):
        return os.path.normcase(self._path)

    def get_is_windows(self):
        return bsc_cor_base.StgBaseMtd.get_path_is_windows(self.get_path())

    def get_is_linux(self):
        return bsc_cor_base.StgBaseMtd.get_path_is_linux(self.get_path())

    def get_is_exists(self):
        return os.path.exists(self.get_path())

    def get_is_directory(self):
        return os.path.isdir(self.get_path())

    def get_is_file(self):
        return os.path.isfile(self.get_path())

    def open_in_system(self):
        if self.get_path():
            StgSystem.open(self.get_path())

    def get_modify_timestamp(self):
        return os.stat(self._path).st_mtime

    def get_modify_time_tag(self):
        return bsc_cor_time.TimestampOpt(
            self.get_modify_timestamp()
        ).get_as_tag()

    def get_user(self):
        return bsc_cor_base.StgBaseMtd.get_user(self.get_path())

    def get_access_timestamp(self):
        return os.stat(self._path).st_atime

    def get_timestamp_is_same_to(self, file_path):
        if file_path is not None:
            if self.get_is_exists() is True and self.__class__(file_path).get_is_exists() is True:
                return str(self.get_modify_timestamp()) == str(self.__class__(file_path).get_modify_timestamp())
            return False
        return False

    def get_is_readable(self):
        return os.access(self._path, os.R_OK)

    def get_is_writable(self):
        return os.access(self._path, os.W_OK)

    def map_to_current(self):
        self._path = bsc_cor_base.StgBasePathMapMtd.map_to_current(self._path)
        return self._path

    def set_modify_time(self, timestamp):
        # noinspection PyBroadException
        try:
            os.utime(self.get_path(), (timestamp, timestamp))
        except Exception:
            bsc_cor_base.ExceptionMtd.set_print()
            bsc_log.Log.trace_error(
                'change modify time failed'
            )

    def get_component_paths(self):
        return bsc_cor_path.PthNodeMtd.get_dag_component_paths(
            path=self.get_path(), pathsep=self.PATHSEP
        )

    def get_parent_path(self):
        return bsc_cor_path.PthNodeMtd.get_dag_parent_path(
            path=self.get_path(), pathsep=self.PATHSEP
        )

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_ancestors(self):
        return map(
            self.__class__, self.get_ancestor_paths()
        )

    def get_path_prettify(self):
        p = self.get_path()
        pathsep = self.PATHSEP
        #
        _ = p.split(pathsep)
        if len(_) > 6:
            if bsc_cor_base.StgBaseMtd.get_path_is_windows(p):
                return six.u('{0}{2}...{2}{1}'.format(pathsep.join(_[:3]), pathsep.join(_[-3:]), pathsep))
            elif bsc_cor_base.StgBaseMtd.get_path_is_linux(p):
                return six.u('{0}{2}...{2}{1}'.format(pathsep.join(_[:2]), pathsep.join(_[-3:]), pathsep))
            return p
        return p

    def set_gui(self, gui):
        self.__gui = gui

    def get_gui(self):
        return self.__gui

    def __str__(self):
        return self._path

    def __repr__(self):
        return self._path


class StgFileSearchOpt(object):
    KEY = 'file search'

    def __init__(self, ignore_name_case=False, ignore_ext_case=False, ignore_ext=False):
        self._ignore_name_case = ignore_name_case
        self._ignore_ext_case = ignore_ext_case
        self._ignore_ext = ignore_ext
        self._search_dict = collections.OrderedDict()

    def set_search_directories(self, directory_paths, below_enable=False):
        self._search_dict = collections.OrderedDict()
        for i in directory_paths:
            self.append_search_directory(i, below_enable=below_enable)
            bsc_log.Log.trace_method_result(
                self.KEY,
                'append search directory: "{}"'.format(i)
            )
        #
        self._set_key_sort_()

    def append_search_directory(self, directory_path, below_enable=False):
        if below_enable is True:
            _ = StgDirectoryMtd.get_all_file_paths__(directory_path)
        else:
            _ = StgDirectoryMtd.get_file_paths__(directory_path)

        for i in _:
            i_directory_path, i_name_base, i_ext = bsc_cor_base.StgBaseMtd.get_file_args(i)
            if self._ignore_name_case is True:
                i_name_base = i_name_base.lower()
            if self._ignore_ext_case is True:
                i_ext = i_ext.lower()
            # noinspection PyBroadException
            try:
                self._search_dict['{}/{}{}'.format(i_directory_path, i_name_base, i_ext)] = i
            except Exception:
                bsc_log.Log.trace_error(
                    'file "{}" is not valid'.format(i)
                )
        # sort
        self._set_key_sort_()

    def _set_key_sort_(self):
        self._search_dict = bsc_cor_raw_for_dict.DictMtd.sort_string_key_to(self._search_dict)

    def get_result(self, file_path_src):
        name_src = os.path.basename(file_path_src)
        name_base_src, ext_src = os.path.splitext(name_src)
        name_base_pattern = bsc_cor_pattern.PtnMultiplyFileMtd.to_fnmatch_style(name_base_src)

        if self._ignore_name_case is True:
            name_base_pattern = name_base_pattern.lower()

        if self._ignore_ext_case is True:
            ext_src = ext_src.lower()

        file_path_keys = self._search_dict.keys()

        match_pattern_0 = '*/{}{}'.format(name_base_pattern, ext_src)
        matches_0 = fnmatch.filter(
            file_path_keys, match_pattern_0
        )
        if matches_0:
            file_path_tgt = self._search_dict[matches_0[-1]]
            return file_path_tgt
        #
        if self._ignore_ext is True:
            match_pattern_1 = '*/{}.*'.format(name_base_pattern)
            matches_1 = fnmatch.filter(
                file_path_keys, match_pattern_1
            )
            if matches_1:
                file_path_tgt = self._search_dict[matches_1[-1]]
                return file_path_tgt


class StgDirectoryOpt(StgPathOpt):
    def __init__(self, path):
        super(StgDirectoryOpt, self).__init__(path)

    def create_dag_fnc(self, path):
        return self.__class__(path)

    def set_create(self):
        bsc_cor_base.StgBaseMtd.create_directory(
            self.path
        )

    def get_file_paths(self, ext_includes=None):
        return StgDirectoryMtd.get_file_paths__(
            self.path, ext_includes
        )

    def get_files(self, ext_includes=None):
        return map(
            StgFileOpt, self.get_file_paths(ext_includes)
        )

    def get_all_file_paths(self, ext_includes=None):
        return StgDirectoryMtd.get_all_file_paths__(
            self.path, ext_includes
        )

    def get_all_directory_paths(self):
        return StgDirectoryMtd.get_all_directory_paths__(
            self._path
        )

    def get_all_directories(self):
        return map(
            self.__class__, self.get_all_directory_paths()
        )

    def get_child_names(self):
        return os.listdir(self.get_path()) or []

    def get_directory_paths(self):
        return StgDirectoryMtd.get_directory_paths__(
            self._path
        )

    def set_copy_to_directory(self, directory_path_tgt, replace=False):
        directory_path_src = self.path
        file_paths_src = self.get_all_file_paths()
        #
        for index, i_file_path_src in enumerate(file_paths_src):
            i_relative_file_path = i_file_path_src[len(directory_path_src):]
            i_file_path_tgt = directory_path_tgt+i_relative_file_path
            #
            i_file_opt_src = StgFileOpt(i_file_path_src)
            i_file_opt_tgt = StgFileOpt(i_file_path_tgt)
            if i_file_opt_tgt.get_is_exists() is False:
                # create target directory first
                i_file_opt_tgt.create_directory()
                #
                bsc_cor_thread.TrdMethod.set_wait()
                bsc_cor_thread.TrdMethod.set_start(
                    i_file_opt_src.set_copy_to_file, index,
                    i_file_path_tgt, replace=replace
                )

    def get_is_exists(self):
        return self.get_is_directory()


class StgDirectoryOptExtra(object):
    def __init__(self, directory_path):
        self._path = directory_path

    def get_path(self):
        return self._path

    path = property(get_path)

    def set_open(self):
        if os.path.exists(self.path):
            if bsc_cor_base.SysBaseMtd.get_is_windows():
                os.startfile(
                    self.path.replace(u'/', os.sep)
                )
            elif bsc_cor_base.SysBaseMtd.get_is_linux():
                subprocess.Popen(
                    u'nautilus "{}" --select'.format(self.path),
                    shell=True
                )

    def get_is_exists(self):
        return os.path.exists(self.path)

    def get_all_file_path(self, ext_includes=None):
        return StgDirectoryMtd.get_all_file_paths__(
            self.path, ext_includes
        )

    def set_create(self):
        bsc_cor_base.StgBaseMtd.create_directory(
            self._path
        )


class StgFileOpt(StgPathOpt):
    def __init__(self, file_path, file_type=None):
        super(StgFileOpt, self).__init__(file_path)
        self._file_type = file_type

    def get_directory_path(self):
        return os.path.dirname(self.path)

    directory_path = property(get_directory_path)

    def get_type(self):
        return self.ext

    type = property(get_type)

    def get_path_base(self):
        return os.path.splitext(self.path)[0]

    @property
    def path_base(self):
        return os.path.splitext(self.path)[0]

    def get_name(self):
        return os.path.basename(self.path)

    name = property(get_name)

    def get_name_base(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    name_base = property(get_name_base)

    def get_ext(self):
        if self._file_type is not None:
            return self._file_type
        return os.path.splitext(self.path)[-1]

    ext = property(get_ext)

    def get_format(self):
        return self.get_ext()[1:]

    def get_is_match_name_pattern(self, name_pattern):
        _ = fnmatch.filter([self.name], name_pattern)
        if _:
            return True
        return False

    def set_read(self):
        if os.path.exists(self.path):
            if self.get_ext() in {'.json'}:
                with open(self.path) as j:
                    raw = json.load(j, object_pairs_hook=collections.OrderedDict)
                    j.close()
                    return raw
            elif self.get_ext() in {'.yml'}:
                with open(self.path) as y:
                    raw = ctt_core.ContentYamlBase.load(y)
                    y.close()
                    return raw
            else:
                with open(self.path) as f:
                    raw = f.read()
                    f.close()
                    return raw

    def set_write(self, raw):
        directory = os.path.dirname(self.path)
        if os.path.isdir(directory) is False:
            # noinspection PyBroadException
            try:
                os.makedirs(directory)
            except Exception:
                bsc_cor_base.ExceptionMtd.set_print()
        if self.ext in {'.json'}:
            with open(self.path, 'w') as j:
                json.dump(
                    raw,
                    j,
                    indent=4
                )
        elif self.ext in {'.yml'}:
            with open(self.path, 'w') as y:
                ctt_core.ContentYamlBase.dump(
                    raw,
                    y,
                    indent=4,
                    default_flow_style=False,
                )
        elif self.ext in {'.png'}:
            with open(self.path, 'wb') as f:
                f.write(raw)
        else:
            with open(self.path, 'w') as f:
                if isinstance(raw, six.text_type):
                    raw = raw.encode('utf-8')
                f.write(raw)

    def append(self, text):
        with open(self.path, 'a+') as f:
            text = bsc_cor_raw.auto_encode(text)
            f.write('{}\n'.format(text))
            f.close()

    def create_directory(self):
        bsc_cor_base.StgBaseMtd.create_directory(
            self.get_directory_path()
        )

    def set_directory_repath_to(self, directory_path_tgt):
        return self.__class__(
            u'{}/{}'.format(
                directory_path_tgt, self.get_name()
            )
        )

    def set_directory_repath_to_join_uuid(self, directory_path_tgt):
        directory_path_src = self.get_directory_path()
        uuid_key = bsc_cor_base.UuidMtd.generate_by_text(directory_path_src)
        return self.__class__(
            u'{}/{}/{}'.format(
                directory_path_tgt, uuid_key, self.get_name()
            )
        )

    def set_ext_repath_to(self, ext_tgt):
        return self.__class__(
            u'{}{}'.format(
                self.get_path_base(), ext_tgt
            )
        )

    def set_copy_to_file(self, file_path_tgt, replace=False):
        if replace is True:
            if os.path.exists(file_path_tgt):
                os.remove(file_path_tgt)
        #
        file_path_src = self.path
        if file_path_src == file_path_tgt:
            return
        #
        if os.path.exists(file_path_tgt) is False:
            directory_path_tgt = os.path.dirname(file_path_tgt)
            if os.path.exists(directory_path_tgt) is False:
                # noinspection PyBroadException
                try:
                    os.makedirs(directory_path_tgt)
                except Exception:
                    pass
            # noinspection PyBroadException
            try:
                shutil.copy2(file_path_src, file_path_tgt)
            except Exception:
                bsc_cor_base.ExceptionMtd.set_print()

    def set_copy_to_directory(self, directory_path_tgt, replace=False):
        file_path_tgt = u'{}/{}'.format(
            directory_path_tgt, self.name
        )
        self.set_copy_to_file(
            file_path_tgt, replace=replace
        )

    def get_render_file_path(self):
        return '{directory}/.temporary/render/{time_tag}.{name_base}{ext}'.format(
            **dict(
                directory=self.get_directory_path(),
                name_base=self.get_name_base(),
                time_tag=self.get_modify_time_tag(),
                ext=self.get_ext()
            )
        )

    def get_size(self):
        if os.path.isfile(self.path):
            return os.path.getsize(self.path)
        return 0

    def get_tag_as_36(self):
        timestamp = self.get_modify_timestamp()
        time_tag = bsc_cor_raw.RawIntegerOpt(int(timestamp*10)).set_encode_to_36()
        size = self.get_size()
        size_tag = bsc_cor_raw.RawIntegerOpt(int(size)).set_encode_to_36()
        return '{}{}'.format(time_tag, size_tag)

    @classmethod
    def new_file_fnc(cls):
        pass

    def get_is_exists(self):
        return self.get_is_file()


# compress
class StgGzipFileOpt(StgFileOpt):
    def __init__(self, *args, **kwargs):
        super(StgGzipFileOpt, self).__init__(*args, **kwargs)

    def set_read(self):
        if self.get_is_file() is True:
            with gzip.GzipFile(
                    mode='rb',
                    fileobj=open(self.path, 'rb')
            ) as g:
                if self.get_ext() in {'.yml'}:
                    raw = ctt_core.ContentYamlBase.load(g)
                    g.close()
                    return raw

    def set_write(self, raw):
        if os.path.isdir(self.directory_path) is False:
            os.makedirs(self.directory_path)
        # noinspection PyArgumentEqualDefault
        with gzip.GzipFile(
                filename=self.name+self.ext,
                mode='wb',
                compresslevel=9,
                fileobj=open(self.path, 'wb')
        ) as g:
            if self.get_ext() in ['.yml']:
                ctt_core.ContentYamlBase.dump(
                    raw,
                    g,
                    indent=4,
                    default_flow_style=False,
                )


class StgZipFileOpt(StgFileOpt):
    def __init__(self, file_path):
        super(StgZipFileOpt, self).__init__(file_path)

    def get_element_names(self):
        if self.get_is_exists() is True:
            file_path = self.get_path()
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as z:
                    return z.namelist()
        return []

    def extract_element_to(self, element_name, element_file_path):
        if self.get_is_exists() is True:
            file_path = self.get_path()
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path) as z:
                    directory_path = os.path.dirname(element_file_path)
                    f = z.extract(element_name, directory_path)
                    os.rename(f, element_file_path)


class StgRarFileOpt(StgFileOpt):
    def __init__(self, file_path):
        super(StgRarFileOpt, self).__init__(file_path)

    def get_element_names(self):
        from unrar import rarfile

        file_path = self.get_path()
        if rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path) as r:
                return r.namelist()
        return []

    def extract_element_to(self, element_name, element_file_path):
        from unrar import rarfile

        file_path = self.get_path()
        if rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path) as r:
                directory_path = os.path.dirname(element_file_path)
                f = r.extract(element_name, directory_path)
                os.rename(f, element_file_path)

    def extract_all_elements_to(self, directory_path):
        from unrar import rarfile

        file_path = self.get_path()
        if rarfile.is_rarfile(file_path):
            with rarfile.RarFile(file_path) as r:
                r.extractall(directory_path)


# temp
class StgTmpBaseMtd(object):
    ROOT = '/l/temp'

    @classmethod
    def get_user_directory(cls, tag):
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(
            u'{root}/temporary/{tag}/{date_tag}-{user}'.format(
                **dict(
                    root=cls.ROOT,
                    date_tag=bsc_cor_base.SysBaseMtd.get_date_tag(),
                    user=bsc_cor_base.SysBaseMtd.get_user_name(),
                    tag=tag
                )
            )
        )

    @classmethod
    def get_cache_directory(cls, tag):
        return bsc_cor_base.StgBasePathMapMtd.map_to_current(
            u'{root}/temporary/{tag}/{user}'.format(
                **dict(
                    root=cls.ROOT,
                    user=bsc_cor_base.SysBaseMtd.get_user_name(),
                    tag=tag
                )
            )
        )

    @classmethod
    def get_save_region(cls, unique_id):
        number = abs(uuid.UUID(unique_id).int)
        return bsc_cor_raw.RawIntegerOpt(number%4096).set_encode_to_36()


class StgTmpThumbnailMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path_(cls, file_path, width=128, ext='.jpg'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.thumbnail/{}/{}/{}{}'.format(
            directory_path, region, key, width, ext
        )

    @classmethod
    def generate_for_qt_resize(cls, file_path, width=128, ext='.jpg'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.qt-thumbnail/{}/{}/{}{}'.format(
            directory_path, region, key, width, ext
        )


class StgTmpYamlMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path(cls, file_path, tag='untitled'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.yml/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.yml'
        )


class StgTmpTextMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path(cls, file_path, tag='untitled'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.txt/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.txt'
        )


class StgTmpInfoMtd(object):
    @classmethod
    def get_key(cls, file_path):
        return bsc_cor_base.UuidMtd.generate_by_file(file_path)

    @classmethod
    def get_file_path(cls, file_path, tag='untitled'):
        directory_path = bsc_cor_environ.EnvBaseMtd.get_temporary_root()
        key = cls.get_key(file_path)
        region = StgTmpBaseMtd.get_save_region(key)
        return '{}/.info/{}/{}/{}{}'.format(
            directory_path, tag, region, key, '.txt'
        )


class StgPathPermissionDefaultMtd(object):
    @classmethod
    def create_directory(cls, path, mode):
        StgPathMtd.create_directory(path)

    @classmethod
    def change_mode(cls, path, mode):
        pass

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        pass

    @classmethod
    def lock(cls, path):
        StgSshOpt(
            path
        ).set_just_read_only_for(
            ['cg_group', 'coop_grp']
        )

    @classmethod
    def unlock(cls, path):
        pass

    @classmethod
    def delete(cls, path):
        os.remove(path)

    @classmethod
    def lock_all_directories(cls, path):
        StgSshOpt(
            path
        ).set_just_read_only_for(
            ['cg_group', 'coop_grp']
        )

    @classmethod
    def unlock_all_directories(cls, path):
        pass

    @classmethod
    def lock_all_files(cls, path):
        pass

    @classmethod
    def unlock_all_files(cls, path):
        pass

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        StgFileOpt(file_path_src).set_copy_to_file(
            file_path_tgt, replace=replace
        )


class StgPathPermissionNewMtd(StgPathPermissionDefaultMtd):
    @classmethod
    def create_directory(cls, path, mode):
        StgRpcMtd.create_directory(path)

    @classmethod
    def change_mode(cls, path, mode):
        StgRpcMtd.change_mode(path, mode)

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        StgRpcMtd.change_owner(path, user, group)

    @classmethod
    def lock(cls, path):
        StgRpcMtd.change_mode(
            path, '555'
        )

    @classmethod
    def unlock(cls, path):
        StgRpcMtd.change_mode(
            path, '775'
        )

    @classmethod
    def delete(cls, path):
        StgRpcMtd.delete(
            path
        )

    @classmethod
    def lock_all_directories(cls, path):
        StgRpcMtd.change_mode(
            path, '555'
        )
        ds = StgDirectoryMtd.get_all_directory_paths__(
            path
        )
        for i in ds:
            StgRpcMtd.change_mode(
                i, '555'
            )

    @classmethod
    def unlock_all_directories(cls, path):
        StgRpcMtd.change_mode(
            path, '775'
        )
        ds = StgDirectoryMtd.get_all_directory_paths__(
            path
        )
        for i in ds:
            StgRpcMtd.change_mode(
                i, '775'
            )

    @classmethod
    def lock_all_files(cls, path):
        fs = StgDirectoryMtd.get_all_file_paths__(
            path
        )
        for i in fs:
            StgRpcMtd.change_mode(
                i, '555'
            )

    @classmethod
    def unlock_all_files(cls, path):
        StgRpcMtd.change_mode(
            path, '775'
        )
        ds = StgDirectoryMtd.get_all_file_paths__(
            path
        )
        for i in ds:
            StgRpcMtd.change_mode(
                i, '775'
            )

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        if StgPathPermissionBaseMtd.get_scheme(file_path_src) == 'default':
            StgPathPermissionDefaultMtd.copy_to_file(file_path_src, file_path_tgt)
            cls.change_owner(file_path_tgt)
            cls.change_mode(file_path_tgt, '775')
        else:
            StgRpcMtd.copy_to_file(
                file_path_src, file_path_tgt, replace=replace
            )


class StgPathPermissionBaseMtd(object):
    SCHEME_MAPPER = dict(
        windows={
            'default': ['l:', 'L:'],
            'new': ['z:', 'Z:', 'x:', 'X:']
        },
        linux={
            'default': ['/l'],
            'new': ['/production', '/job']
        }
    )
    MAP_DICT = {
        i: k for k, v in SCHEME_MAPPER[bsc_cor_base.SysBaseMtd.get_platform()].items() for i in v
    }
    METHOD_DICT = dict(
        default=StgPathPermissionDefaultMtd,
        new=StgPathPermissionNewMtd
    )

    @classmethod
    def get_mode(cls, user, group, other):
        query = [
            '---',  # 0
            '--x',  # 1
            '-w-',  # 2
            '-wx',  # 3
            'r--',  # 4
            'r-x',  # 5
            'rw-',  # 6
            'rwx',  # 7
        ]
        return str(query.index(user))+str(query.index(group))+str(query.index(other))

    @classmethod
    def get_scheme(cls, path):
        for k, v in cls.MAP_DICT.items():
            if path.startswith(k+'/'):
                return v
        return 'default'

    @classmethod
    def get_method(cls, path):
        """
print StgPathPermissionBaseMtd.get_method(
    '/l/prod'
)
print StgPathPermissionBaseMtd.get_method(
    '/production/shows'
)
        :param path:
        :return:
        """
        return cls.METHOD_DICT[cls.get_scheme(path)]


class StgPathPermissionMtd(object):
    def __init__(self, path):
        self._path = path

    @classmethod
    def create_directory(cls, path, mode='775'):
        StgPathPermissionBaseMtd.get_method(
            path
        ).create_directory(path, mode)

    @classmethod
    def change_owner(cls, path, user='artist', group='artists'):
        StgPathPermissionBaseMtd.get_method(
            path
        ).change_owner(path, user, group)

    @classmethod
    def change_mode(cls, path, mode):
        StgPathPermissionBaseMtd.get_method(
            path
        ).change_mode(path, mode)

    @classmethod
    def lock(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).lock(path)

    @classmethod
    def unlock(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).unlock(path)

    @classmethod
    def delete(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).delete(path)

    @classmethod
    def lock_all_directories(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).lock_all_directories(path)

    @classmethod
    def unlock_all_directories(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).unlock_all_directories(path)

    @classmethod
    def lock_all_files(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).lock_all_files(path)

    @classmethod
    def unlock_all_files(cls, path):
        StgPathPermissionBaseMtd.get_method(
            path
        ).unlock_all_files(path)

    @classmethod
    def copy_to_file(cls, file_path_src, file_path_tgt, replace=False):
        StgPathPermissionBaseMtd.get_method(
            file_path_tgt
        ).copy_to_file(file_path_src, file_path_tgt, replace)


class StgTextureMtd(object):
    @classmethod
    def get_is_udim(cls, path):
        n = os.path.basename(path)
        return not not re.finditer(r'<udim>', n, re.IGNORECASE)

    @classmethod
    def get_udim_region_args(cls, path):
        """
        print StgTextureMtd.get_udim_region_args(
            '/data/e/workspace/lynxi/test/maya/vertex-color/test.1002.jpg'
        )
        print StgTextureMtd.get_udim_region_args(
            '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg'
        )
        """
        d = os.path.dirname(path)
        n = os.path.basename(path)
        if os.path.isfile(path):
            return [(path, '1001')]
        r = re.finditer(r'<udim>', n, re.IGNORECASE) or []
        if r:
            list_ = []
            g_n = p_n = n
            for i_result in r:
                i_start, i_end = i_result.span()
                g_n = g_n.replace(n[i_start:i_end], '[0-9][0-9][0-9][0-9]', 1)
                p_n = p_n.replace(n[i_start:i_end], '{region}', 1)
            g_p = '/'.join([d, g_n])
            p_p = '/'.join([d, p_n])
            results = StgDirectoryMtd.find_file_paths(g_p)
            for i_result in results:
                i_p = parse.parse(
                    p_p, i_result
                )
                i_region = i_p['region']
                list_.append((i_result, i_region))
            return list_
        return []

    @classmethod
    def get_unit_paths(cls, path):
        """
        print StgTextureMtd.get_unit_paths(
            '/data/e/workspace/lynxi/test/maya/vertex-color/test.1001.jpg'
        )
        print StgTextureMtd.get_unit_paths(
            '/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg'
        )
        """
        if os.path.isfile(path):
            return [path]
        d = os.path.dirname(path)
        n = os.path.basename(path)
        r = re.finditer(r'<udim>', n, re.IGNORECASE) or []
        if r:
            g_n = n
            for i_result in r:
                i_start, i_end = i_result.span()
                g_n = g_n.replace(n[i_start:i_end], '[0-9][0-9][0-9][0-9]', 1)
            g_p = '/'.join([d, g_n])
            return StgDirectoryMtd.find_file_paths(g_p)
        return []


class StgTextureOpt(StgFileOpt):
    def __init__(self, *args, **kwargs):
        super(StgTextureOpt, self).__init__(*args, **kwargs)

    def get_units(self):
        return map(
            self.__class__, StgTextureMtd.get_unit_paths(self.get_path())
        )

    def get_unit_paths(self):
        return StgTextureMtd.get_unit_paths(self.get_path())

    def get_udim_region_args(self):
        return StgTextureMtd.get_udim_region_args(self.get_path())
