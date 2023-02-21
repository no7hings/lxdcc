# coding:utf-8
import six


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
    def run_branch_fnc_(batch_option_hook_key_, option_hook_key_, batch_hook_option_, hook_option_override_):
        _batch_hook_option_opt = bsc_core.ArgDictStringOpt(batch_hook_option_)
        _batch_choice_scheme = _batch_hook_option_opt.get('choice_scheme')
        _hook_option_opt = bsc_core.ArgDictStringOpt(
            dict(
                option_hook_key=option_hook_key_,
                #
                batch_file=_batch_hook_option_opt.get('batch_file'),
                # python option
                file=_batch_hook_option_opt.get('file'),
                #
                user=_batch_hook_option_opt.get('user'), time_tag=_batch_hook_option_opt.get('time_tag'),
                #
                choice_scheme=_batch_hook_option_opt.get('choice_scheme'),
                #
                rez_beta=_batch_hook_option_opt.get('rez_beta') or False,
                #
                td_enable=_batch_hook_option_opt.get('td_enable') or False,
                localhost_enable=_batch_hook_option_opt.get('localhost_enable') or False,
            )
        )
        #
        _hook_option_opt.set_update(
            hook_option_override_
        )
        # add main-key to dependencies
        _dependencies = _hook_option_opt.get('dependencies') or []
        _dependencies.append(batch_option_hook_key_)
        _hook_option_opt.set('dependencies', _dependencies)
        # _hook_option_opt.set('dependency_job_ids', )
        #
        _choice_scheme_includes = _hook_option_opt.get('choice_scheme_includes', as_array=True)
        if _choice_scheme_includes:
            if session._get_choice_scheme_matched_(
                    _batch_choice_scheme,
                    _choice_scheme_includes
            ) is False:
                bsc_core.LogMtd.trace_method_warning(
                    'scheme choice',
                    'option-hook="{}" is ignore'.format(option_hook_key_)
                )
                return
        #
        _inherit_keys = _hook_option_opt.get('inherit_keys', as_array=True)
        if _inherit_keys:
            _hook_option_opt.set('inherit_keys', _inherit_keys)
            for _i_key in _inherit_keys:
                _hook_option_opt.set(
                    _i_key, _batch_hook_option_opt.get(_i_key)
                )
        #
        _ssn_cmd_hook.set_option_hook_execute_by_deadline(
            option=_hook_option_opt.to_string()
        )
    #
    c = session.configure
    option_hook_keys = c.get('option_hooks')
    main_key = session.option_opt.get('option_hook_key')
    with bsc_core.LogProgress.create(
        maximum=len(option_hook_keys),
        label='option hooks execute by deadline',
        use_as_progress_bar=True,
    ) as g_p:
        for i in option_hook_keys:
            g_p.set_update()
            if isinstance(i, six.string_types):
                i_sub_key = i
                run_branch_fnc_(
                    main_key,
                    i_sub_key,
                    session.option,
                    {}
                )
            elif isinstance(i, dict):
                for i_k, i_v in i.items():
                    i_sub_key = i_k
                    i_script_option = i_v
                    run_branch_fnc_(
                        main_key,
                        i_sub_key,
                        session.option,
                        i_script_option
                    )
