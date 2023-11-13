# coding:utf-8
import functools

import lxresource.core as rsc_core

import lxbasic.session.core as bsc_ssn_core


class Hook(object):
    @classmethod
    def get_args(cls, key):
        _ = rsc_core.RscHook.get_args(
                key
            )
        if _:
            hook_type, hook_key, hook_configure, yaml_file_path, python_file_path, shell_file_path = _
            if hook_type in {
                'python-command', 'shell-command'
            }:
                session = bsc_ssn_core.CommandSession(
                    type=hook_type,
                    hook=hook_key,
                    configure=hook_configure
                )
            else:
                session = bsc_ssn_core.GenerSession(
                    type=hook_type,
                    hook=hook_key,
                    configure=hook_configure
                )

            session.set_configure_yaml_file(yaml_file_path)
            if python_file_path is not None:
                session.set_python_script_file(python_file_path)
            if shell_file_path:
                session.set_shell_script_file(shell_file_path)

            return session, functools.partial(session.execute)
