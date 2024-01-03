# coding:utf-8


class ScpEnvironment(object):
    @classmethod
    def get_data(cls, task_id):
        if task_id:
            import lxbasic.shotgun.core as bsc_stg_core

            import lxresolver.core as rsv_core

            data = []

            resolver = rsv_core.RsvBase.generate_root()
            c = bsc_stg_core.StgConnector()
            dict_ = c.get_data_from_task_id(task_id)
            keys = resolver.VariantTypes.Constructs
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

