# coding:utf-8
import collections

import parse

from lxutil import utl_core

from lxbasic import bsc_core


class MakePassword(object):
    def __init__(self, key, s):
        self.key = key
        self.s = s

    def encrypt(self):
        b = bytearray(str(self.s).encode("utf-8"))
        n = len(b)
        c = bytearray(n * 2)
        j = 0
        for i in range(0, n):
            b1 = b[i]
            b2 = b1 ^ self.key
            c1 = b2 % 16
            c2 = b2 // 16
            c1 = c1 + 65
            c2 = c2 + 65
            c[j] = c1
            c[j + 1] = c2
            j = j + 2
        return c.decode("utf-8")

    def decrypt(self):
        c = bytearray(str(self.s).encode("utf-8"))
        n = len(c)
        if n % 2 != 0:
            return ""
        n = n // 2
        b = bytearray(n)
        j = 0
        for i in range(0, n):
            c1 = c[j]
            c2 = c[j + 1]
            j = j + 2
            c1 = c1 - 65
            c2 = c2 - 65
            b2 = c2 * 16 + c1
            b1 = b2 ^ self.key
            b[i] = b1
        try:
            return b.decode("utf-8")
        except:
            return "failed"


class AbsPermission(object):
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
        'plt_grp': 20024,
        'grm_grp': 20012,
        'rig_grp': 20013,
        'srf_grp': 20014,
        'set_grp': 20023,
        'edt_grp': 20028,
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
    @classmethod
    def _set_nas_cmd_run_(cls, cmd):
        import paramiko
        #
        utl_core.Log.set_module_result_trace(
            'nas-cmd-run',
            'command=`{}`'.format(cmd)
        )
        #
        password = MakePassword(120, 'KBHBOCCCMDMBKEBDCBKBLAKA')
        # paramiko.util.log_to_file('paramiko.log')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname='isilon.diezhi.local',
            username='root',
            password=password.decrypt().encode('utf-8'),
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        result = stdout.read()
        ssh.close()
        return result


class RsvPermissionMtd(AbsPermission):
    @classmethod
    def set_entity_task_create(cls, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        r = rsv_commands.get_resolver()
        #
        task_directory_paths = r.get_rsv_entity_task_directory_paths(**kwargs)
        for i_task_directory_path in task_directory_paths:
            bsc_core.StoragePathMtd.set_directory_create(i_task_directory_path)
            utl_core.Log.set_module_result_trace(
                'directory create',
                'directory="{}"'.format(i_task_directory_path)
            )
        #
        step_directory_paths = r.get_rsv_entity_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            if i_group_name in cls.GROUP_ID_QUERY:
                i_group_id = cls.GROUP_ID_QUERY[i_group_name]
                i_path = bsc_core.StoragePathMtd.set_map_to_nas(i_step_directory_path)
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=i_path
                )
                cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
                    **i_kwargs
                )
                cls._set_nas_cmd_run_(cmd)
    @classmethod
    def set_create(cls, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        r = rsv_commands.get_resolver()
        #
        step_directory_paths = r.get_rsv_entity_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            i_group_id = cls.GROUP_ID_QUERY[i_group_name]
            i_path = bsc_core.StoragePathMtd.set_map_to_nas(i_step_directory_path)
            i_kwargs = dict(
                group_id=i_group_id,
                path=i_path
            )
            cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
                **i_kwargs
            )
            cls._set_nas_cmd_run_(cmd)
    @classmethod
    def get_asset_task(cls, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        r = rsv_commands.get_resolver()
        #
        step_directory_paths = r.get_rsv_entity_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            i_group_id = cls.GROUP_ID_QUERY[i_group_name]
            i_path = bsc_core.StoragePathMtd.set_map_to_nas(i_step_directory_path)
            i_kwargs = dict(
                group_id=i_group_id,
                path=i_path
            )
            cmd = 'ls -led {path}'.format(
                **i_kwargs
            )
            cls._set_nas_cmd_run_(cmd)
    @classmethod
    def set_crate_by_step(cls, step, path):
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        group_name = '{}_grp'.format(step)
        group_id = bsc_core.SystemMtd.get_group_id(group_name)
        kwargs = dict(
            group_id=group_id,
            path=path
        )
        cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
            **kwargs
        )
        cls._set_nas_cmd_run_(cmd)
    @classmethod
    def set_crate_by_group(cls, group_name, path):
        group_id = bsc_core.SystemMtd.get_group_id(group_name)
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        kwargs = dict(
            group_id=group_id,
            path=path
        )
        cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
            **kwargs
        )
        cls._set_nas_cmd_run_(cmd)
    @classmethod
    def set_test(cls, path):
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        kwargs = dict(
            path=path
        )
        cmd = cls.CMD_QUERY['show_grp'].format(
            **kwargs
        )
        return cls._set_nas_cmd_run_(cmd)
    @classmethod
    def set_group_read_only(cls, group_name, path):
        group_id = bsc_core.SystemMtd.get_group_id(group_name)
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        kwargs = dict(
            group_id=group_id,
            path=path
        )

        cmd = 'chmod -R -a# 4 {}'.format(path)

        cls._set_nas_cmd_run_(cmd)

        cmd = cls.CMD_QUERY['read_only'].format(
            **kwargs
        )
        return cls._set_nas_cmd_run_(cmd)
    @classmethod
    def get_group_is_read_only(cls, group_name, path):
        pass


class PathGroupPermission(AbsPermission):
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

    def __init__(self, path):
        self._path = path
        self._nas_path = bsc_core.StoragePathMtd.set_map_to_nas(path)

    def get_all_group_data(self):
        return self._get_all_group_data_(
            self._nas_path
        )

    def get_is_read_only(self, group_name):
        group_data = self._get_all_group_data_(self._nas_path)
        if group_name in group_data:
            index, content = group_data[group_name]
            if 'dir_gen_read' in content:
                return True
        return False

    def set_read_only(self, group_name):
        group_data = self._get_all_group_data_(self._nas_path)
        if group_name in group_data:
            index, content = group_data[group_name]
            group_id = self.GROUP_ID_QUERY[group_name]
            kwargs = dict(
                group_id=group_id,
                path=self._nas_path,
                index=index
            )
            cmd = self.CMD_QUERY['remove_grp'].format(
                **kwargs
            )
            self._set_nas_cmd_run_(cmd)

            cmd = self.CMD_QUERY['read_only'].format(
                **kwargs
            )
            return self._set_nas_cmd_run_(cmd)
        else:
            group_id = self.GROUP_ID_QUERY[group_name]
            kwargs = dict(
                group_id=group_id,
                path=self._nas_path,
            )
            cmd = self.CMD_QUERY['read_only'].format(
                **kwargs
            )
            return self._set_nas_cmd_run_(cmd)

    def set_all_remove(self):
        group_data = self._get_all_group_data_(self._nas_path)
        for k, v in group_data.items():
            if k in self.GROUP_ID_QUERY:
                i_group_name = k
                i_index, i_content = v
                i_group_id = self.GROUP_ID_QUERY[i_group_name]
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=self._nas_path,
                    index=i_index
                )
                i_cmd = self.CMD_QUERY['remove_grp'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)

    def set_all_read_only(self):
        group_data = self._get_all_group_data_(self._nas_path)
        for k, v in group_data.items():
            if k in self.GROUP_ID_QUERY:
                i_group_name = k
                i_index, i_content = v
                i_group_id = self.GROUP_ID_QUERY[i_group_name]
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=self._nas_path,
                    index=i_index
                )
                i_cmd = self.CMD_QUERY['remove_grp'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)

                i_cmd = self.CMD_QUERY['read_only'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)

    def get_is_allow(self, group_name):
        group_data = self._get_all_group_data_(self._nas_path)
        if group_name in group_data:
            index, content = group_data[group_name]

    def set_allow(self, group_name):
        group_id = self.GROUP_ID_QUERY[group_name]
        kwargs = dict(
            group_id=group_id,
            path=self._nas_path
        )
        cmd = self.CMD_QUERY['allow'].format(
            **kwargs
        )
        return self._set_nas_cmd_run_(cmd)

    def set_file_allow(self, group_name):
        group_id = self.GROUP_ID_QUERY[group_name]
        group_data = self._get_all_group_data_(self._nas_path)
        if group_name in group_data:
            index, content = group_data[group_name]
            kwargs = dict(
                group_id=group_id,
                path=self._nas_path,
                index=index
            )
            i_cmd = self.CMD_QUERY['remove_grp'].format(
                **kwargs
            )
            self._set_nas_cmd_run_(i_cmd)

        kwargs = dict(
            group_id=group_id,
            path=self._nas_path
        )
        cmd = self.CMD_QUERY['file_allow'].format(
            **kwargs
        )
        return self._set_nas_cmd_run_(cmd)

    def set_file_all_allow(self):
        group_data = self._get_all_group_data_(self._nas_path)
        if 'cg_grp' not in group_data:
            return self.set_file_allow('cg_grp')

        for k, v in group_data.items():
            if k in self.GROUP_ID_QUERY:
                i_group_name = k
                i_index, i_content = v
                i_group_id = self.GROUP_ID_QUERY[i_group_name]
                i_kwargs = dict(
                    group_id=i_group_id,
                    path=self._nas_path,
                    index=i_index
                )
                i_cmd = self.CMD_QUERY['remove_grp'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)

                i_cmd = self.CMD_QUERY['file_allow'].format(
                    **i_kwargs
                )
                self._set_nas_cmd_run_(i_cmd)


if __name__ == '__main__':
    # print bsc_core.StoragePathMtd.get_group_name('/l/prod/cgm/publish/assets/prp/balloon/srf/surfacing/texture/eye.spec_clr.1001.tx/V-R8VE9R-3PKW7.eye.spec_clr.1001.tx')
    # print PathGroupPermission(
    #     '/l/prod/cgm/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v022'
    # ).get_all_group_data()

    # print PathGroupPermission(
    #     '/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/texture'
    # ).get_all_group_data()
    #
    # print PathGroupPermission(
    #     '/l/prod/cgm/publish/assets/chr/nn_4y/srf/srf_cfxshading/texture'
    # ).get_all_group_data()
    #


    print PathGroupPermission(
        '/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/nn_4y.srf.surfacing.v051'
    ).get_all_group_data()

    # files = bsc_core.DirectoryMtd.get_all_file_paths(
    #     '/l/prod/cgm/publish/assets/chr/nn_4y/srf/surfacing/texture'
    # )
    # for i in files:
    #     if not PathGroupPermission(
    #         i
    #     ).get_all_group_data():
    #         PathGroupPermission(
    #             i
    #         ).set_allow(
    #             'cg_group'
    #         )
