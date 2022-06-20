# coding:utf-8
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


class RsvPermissionMtd(object):
    GROUP_ID_DICT = {
        'cg_grp': 20002,
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
    }
    MODEL_DICT = {
        "deny": "chmod -R +a group {group_id} deny dir_gen_write,std_delete,delete_child,object_inherit,container_inherit {path}",
        "allow": "chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit {path}",
        "read_only": "chmod -R +a group {group_id} allow dir_gen_read,dir_gen_execute,object_inherit,container_inherit {path}",
        'show_grp': "ls -led {}",
    }
    @classmethod
    def set_nas_cmd_run(cls, cmd):
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
            i_group_id = cls.GROUP_ID_DICT[i_group_name]
            i_path = bsc_core.StoragePathMtd.set_map_to_nas(i_step_directory_path)
            i_kwargs = dict(
                group_id=i_group_id,
                path=i_path
            )
            cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
                **i_kwargs
            )
            cls.set_nas_cmd_run(cmd)
    @classmethod
    def set_create(cls, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        r = rsv_commands.get_resolver()
        #
        step_directory_paths = r.get_rsv_entity_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            i_group_id = cls.GROUP_ID_DICT[i_group_name]
            i_path = bsc_core.StoragePathMtd.set_map_to_nas(i_step_directory_path)
            i_kwargs = dict(
                group_id=i_group_id,
                path=i_path
            )
            cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
                **i_kwargs
            )
            cls.set_nas_cmd_run(cmd)
    @classmethod
    def get_asset_task(cls, **kwargs):
        import lxresolver.commands as rsv_commands
        #
        r = rsv_commands.get_resolver()
        #
        step_directory_paths = r.get_rsv_entity_step_directory_paths(**kwargs)
        for i_step_directory_path in step_directory_paths:
            i_group_name = '{}_grp'.format(kwargs['step'])
            i_group_id = cls.GROUP_ID_DICT[i_group_name]
            i_path = bsc_core.StoragePathMtd.set_map_to_nas(i_step_directory_path)
            i_kwargs = dict(
                group_id=i_group_id,
                path=i_path
            )
            cmd = 'ls -led {path}'.format(
                **i_kwargs
            )
            cls.set_nas_cmd_run(cmd)
    @classmethod
    def set_crate_by_step(cls, step, path):
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        group = '{}_grp'.format(step)
        group_id = cls.GROUP_ID_DICT[group]
        kwargs = dict(
            group_id=group_id,
            path=path
        )
        cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
            **kwargs
        )
        cls.set_nas_cmd_run(cmd)
    @classmethod
    def set_crate_by_group(cls, group, path):
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        group_id = cls.GROUP_ID_DICT[group]
        kwargs = dict(
            group_id=group_id,
            path=path
        )
        cmd = 'chmod -R +a group {group_id} allow dir_gen_all,object_inherit,container_inherit "{path}"'.format(
            **kwargs
        )
        cls.set_nas_cmd_run(cmd)
    @classmethod
    def set_test(cls, path):
        path = bsc_core.StoragePathMtd.set_map_to_nas(path)
        kwargs = dict(
            group_id='srf_grp',
            path=path
        )
        cmd = 'chmod -R +a group {group_id} "{path}"'.format(
            **kwargs
        )
        cls.set_nas_cmd_run(cmd)


if __name__ == '__main__':
    # import lxresolver.commands as rsv_commands
    # r = rsv_commands.get_resolver()
    #
    # asset_args = [
    #     ('lib', 'flg', 'shl__cao_a')
    # ]
    #
    # task_args = [
    #     ('mod', 'modeling'),
    #     ('mod', 'mod_dynamic'),
    #     ('rig', 'rigging'),
    #     ('srf', 'surfacing')
    # ]
    #
    # for project, role, asset in asset_args:
    #     rsv_asset = r.get_rsv_entity(project=project, role=role, asset=asset)
    #     print rsv_asset
    # RsvPermissionMtd.set_entity_task_create(
    #     project='lib', role='flg', asset='shl__cao_a', step='srf', task='surfacing'
    # )
    RsvPermissionMtd.set_entity_task_create(
        project='cgm', role='chr', asset='nn_4y_test', step='srf', task='srf_anishading'
    )
