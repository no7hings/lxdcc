# coding:utf-8
import os


class UsdProcess(object):
    PROCESS_KWARGS = dict(
        process_location='{}/.process'.format(os.path.dirname(__file__.replace('\\', '/')))
    )
    @classmethod
    def get_command(cls, option):
        run_kwargs = dict(cls.PROCESS_KWARGS)
        run_kwargs['option'] = option
        return 'rez-env lxdcc usd-20.11 -- lxdcc-python {process_location}/usd-file-process "{option}"'.format(
            **run_kwargs
        )
