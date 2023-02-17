# coding:utf-8
import fnmatch

from lxbasic import bsc_core

import lxbasic.objects as bsc_objects

from lxsession import ssn_configure


class SsnHookMtd(object):
    @classmethod
    def set_cmd_run(cls, cmd):
        import urllib
        #
        from lxbasic import bsc_core
        #
        unique_id = bsc_core.UuidMtd.get_new()
        #
        hook_yml_file_path = bsc_core.StgUserMtd.get_user_session_file(unique_id=unique_id)
        #
        bsc_core.StgFileOpt(hook_yml_file_path).set_write(
            dict(
                user=bsc_core.SystemMtd.get_user_name(),
                tiame=bsc_core.TimeMtd.get_time(),
                cmd=cmd,
            )
        )
        #
        urllib.urlopen(
            'http://{host}:{port}/cmd-run?uuid={uuid}'.format(
                **dict(
                    host=ssn_configure.Hook.HOST,
                    port=ssn_configure.Hook.PORT,
                    uuid=unique_id
                )
            )
        )


class SsnHookEngineMtd(object):
    CONFIGURE = bsc_objects.Configure(
        value=bsc_core.CfgFileMtd.get_yaml('session/hook-engine')
    )
    CONFIGURE.set_flatten()
    @classmethod
    def get_all(cls):
        return cls.CONFIGURE.get_branch_keys('command') or []
    @classmethod
    def get_command(cls, hook_engine, **kwargs):
        _ = cls.CONFIGURE.get(
            'command.{}'.format(hook_engine)
        )
        return _.format(**kwargs)


class SsnHookFileMtd(object):
    BRANCH = 'hooks'
    @classmethod
    def get_python(cls, key):
        return bsc_core.RscFileMtd.get(
            '{}/{}.py'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_yaml(cls, key):
        return bsc_core.RscFileMtd.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_command(cls, key):
        return bsc_core.RscFileMtd.get(
            '{}/{}.yml'.format(cls.BRANCH, key)
        )
    @classmethod
    def get_full_key(cls, key):
        return
    #
    @classmethod
    def get_hook_abs_path(cls, src_key, tgt_key):
        """
        for i in ['../shotgun/shotgun-create', '../maya/geometry-export', '../maya/look-export']:
            print SsnHookFileMtd.get_hook_abs_path(
                'rsv-task-methods/asset/usd/usd-create', i
            )

        rsv-task-methods/asset/shotgun/shotgun-create
        rsv-task-methods/asset/maya/geometry-export
        rsv-task-methods/asset/maya/look-export

        :param src_key: str(<hook-key>)
        :param tgt_key: str(<hook-key>)
        :return: str(<hook-key>)
        """
        if fnmatch.filter([tgt_key], '.*'):
            s_0 = tgt_key.split('.')[-1].strip()
            c_0 = tgt_key.count('.')
            ss_1 = src_key.split('/')
            c_1 = len(ss_1)
            if c_0 < c_1:
                return '{}{}'.format('/'.join(ss_1[:-c_0]), s_0)
            elif c_0 == c_1:
                return s_0
            else:
                raise ValueError(
                    'count of sep "." out of range'
                )
        return tgt_key
    @classmethod
    def get_extra_file(cls, key):
        directory_path = bsc_core.EnvironMtd.get_session_root()
        region = bsc_core.StgTmpBaseMtd.get_save_region(key)
        return '{}/.session/extra/{}/{}{}'.format(
            directory_path, region, key, '.yml'
        )
    @classmethod
    def set_extra_data_save(cls, raw):
        key = bsc_core.UuidMtd.get_new()
        file_path = cls.get_extra_file(key)
        bsc_core.StgFileOpt(file_path).set_write(raw)
        return key
    @classmethod
    def get_extra_data(cls, key):
        file_path = cls.get_extra_file(key)
        return bsc_core.StgFileOpt(file_path).set_read()


class SsnOptionHookFileMtd(SsnHookFileMtd):
    BRANCH = 'option-hooks'


class SsnHookServerMtd(object):
    @classmethod
    def get_key(cls, **kwargs):
        return bsc_core.UuidMtd.get_by_string(
            bsc_core.ArgDictStringMtd.to_string(**kwargs)
        )
    @classmethod
    def get_file_path(cls, **kwargs):
        directory_path = bsc_core.EnvironMtd.get_session_root()
        key = cls.get_key(**kwargs)
        region = bsc_core.StgTmpBaseMtd.get_save_region(key)
        return '{}/.session/option-hook/{}/{}{}'.format(
            directory_path, region, key, '.yml'
        )
