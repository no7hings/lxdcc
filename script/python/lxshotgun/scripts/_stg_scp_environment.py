# coding:utf-8
from lxbasic import bsc_core


class ScpEnvironment(object):
    @classmethod
    def get_data(cls, task_id):
        if task_id:
            import lxshotgun.objects as stg_objects

            import lxresolver.commands as rsv_commands

            data = []

            resolver = rsv_commands.get_resolver()
            c = stg_objects.StgConnector()
            dict_ = c.get_data_from_task_id(task_id)
            keys = resolver.VariantTypes.All
            for i_key in keys:
                i_env_key = 'PG_{}'.format(i_key.upper())
                #
                if i_key in dict_:
                    i_env_value = dict_[i_key]
                else:
                    i_env_value = ''
                #
                data.append(
                    (i_key, i_env_key, i_env_value)
                )
            return True, data
        return False, None

