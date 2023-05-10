# coding:utf-8
if __name__ == '__main__':
    # print self._rsv_filter_opt.value
    # print rsv_entities[0]
    # print rsv_entities[0].get_rsv_tasks(**self._rsv_filter_opt.value)
    # OrderedDict([('branch', 'asset'), ('step', ['cpt', 'mod', 'srf', 'grm', 'rig', 'env', 'cam', 'lgt'])])
    # RsvStep(type="step", path="/nsa_dev/chr/td_test/srf")
    # [RsvTask(type="task", path="/nsa_dev/chr/td_test/srf/surface")]
    import collections

    from lxutil import utl_core

    import lxresolver.commands as rsv_commands

    utl_core.Log.TRACE_RESULT_ENABLE = False

    r = rsv_commands.get_resolver()

    s = r.get_rsv_step(
        project='nsa_dev', asset='td_test', step='srf'
    )

    print s

    print s.get_rsv_tasks(
        **collections.OrderedDict([('branch', 'asset'), ('step', ['cpt', 'mod', 'srf', 'grm', 'rig', 'env', 'cam', 'lgt'])])
    )

    print s.get_children()
