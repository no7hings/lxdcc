# coding:utf-8
if __name__ == '__main__':
    import json

    from lxbasic import bsc_core

    _ = bsc_core.StgFileOpt('/l/prod/cjd/publish/assets/chr/td_test/srf/surfacing/td_test.srf.surfacing.v006/metadata/td_test.info.yml').set_read()

    print json.dumps(
            _,
            indent=4
        )

