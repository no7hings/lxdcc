# coding:utf-8


def set_session_option_hooks_execute_by_deadline(session):
    """
    execute contain option-hooks by deadline

    :param session: <instance of session>
    :return: None
    """
    from lxsession.commands import _ssn_cmd_hook
    #
    from lxbasic import bsc_core
    #
    def run_fnc_(main_key_, method_option_hook_key_, option_, script_option_):
        _batch_option_opt = bsc_core.KeywordArgumentsOpt(option_)
        _option_opt = bsc_core.KeywordArgumentsOpt(
            dict(
                option_hook_key=method_option_hook_key_,
                #
                batch_file=_batch_option_opt.get('batch_file'),
                # python option
                file=_batch_option_opt.get('file'),
                #
                user=_batch_option_opt.get('user'), time_tag=_batch_option_opt.get('time_tag'),
                #
                td_enable=_batch_option_opt.get('td_enable') or False,
                rez_beta=_batch_option_opt.get('rez_beta') or False,
            )
        )
        #
        _option_opt.set_update(
            script_option_
        )
        # add main-key to dependencies
        _dependencies = _option_opt.get('dependencies') or []
        _dependencies.append(main_key_)
        _option_opt.set('dependencies', _dependencies)
        #
        _inherit_keys = _option_opt.get('inherit_keys', as_array=True)
        if _inherit_keys:
            _option_opt.set('inherit_keys', _inherit_keys)
            for _i in _inherit_keys:
                _option_opt.set(
                    _i, _batch_option_opt.get(_i)
                )
        #
        _ssn_cmd_hook.set_option_hook_execute_by_deadline(
            option=_option_opt.to_string()
        )
    #
    c = session.configure
    option_hook_keys = c.get('option_hooks')
    main_key = session.option_opt.get('option_hook_key')
    for i in option_hook_keys:
        if isinstance(i, (str, unicode)):
            i_sub_key = i
            run_fnc_(
                main_key,
                i_sub_key,
                session.option,
                {}
            )
        elif isinstance(i, dict):
            for i_k, i_v in i.items():
                i_sub_key = i_k
                i_script_option = i_v
                run_fnc_(
                    main_key,
                    i_sub_key,
                    session.option,
                    i_script_option
                )
