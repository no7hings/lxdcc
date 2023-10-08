# coding:utf-8


class MayaProcess(object):
    @classmethod
    def get_command(cls, option):
        import lxbasic.objects as bsc_objects

        c = bsc_objects.PackageContextNew(
            ' '.join(['lxdcc', 'maya', 'maya@2019.2', 'usd', 'mtoa@4.2.1.1'])
        ).get_command(
            args_execute=[
                (
                    r'-- maya -batch -command '
                    r'"python('
                    r'\"importlib=__import__(\\\"importlib\\\");'
                    r'ssn_commands=importlib.import_module(\\\"lxsession.commands\\\");'
                    r'ssn_commands.set_option_hook_execute(option=\\\"{hook_option}\\\")\")"'
                ).format(
                    hook_option='option_hook_key="dcc-process/maya-process"&'+option
                )
            ],
        )
        return c


class PythonProcess(object):
    @classmethod
    def generate_command(cls, option):
        from lxbasic import bsc_core

        import lxbasic.objects as bsc_objects

        c = bsc_objects.PackageContextNew(
            ' '.join(['lxdcc', 'usd'])
        ).get_command(
            args_execute=[
                r'-- lxdcc-python {process_file} "{option}"'.format(
                    process_file=bsc_core.RscFileMtd.get('python-process/usd-script.py'), option=option
                )
            ],
        )
        return c


if __name__ == '__main__':
    print PythonProcess.generate_command(
        'method=test'
    )
