# coding:utf-8
import glob

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

src_root = '/l/temp/td/dongchangbao/myworkspace'

beta_root = '/l/packages/pg/beta'

prod_root = '/l/packages/pg/prod'

packages = [
    'lxdcc',
    'lxdcc_fnc',
    'lxdcc_gui',
    'lxdcc_rsc'
]

version_override = '0.0.192'
version_override_enable = False


def get_latest_version(**kwargs):
    kwargs['version'] = '*'
    fnmatch_pattern = '{root}/{package}/{version}'.format(
        **kwargs
    )
    _ = glob.glob(fnmatch_pattern)
    if _:
        _ = bsc_core.RawTextsMtd.sort_by_number(_)
        latest_path = _[-1]
        latest_path = latest_path.replace('\\', '/')
        return latest_path.split('/')[-1]


def get_new_version(version):
    _ = version.split('.')
    _.reverse()
    for seq, i in enumerate(_):
        if str(i).isdigit():
            _[seq] = str(int(i) + 1)
            break

    _.reverse()
    return '.'.join(_)


def set_push():
    for i_package in packages:
        i_beta_latest_version = get_latest_version(
            **dict(
                root=beta_root,
                package=i_package,
            )
        )
        if i_beta_latest_version is not None:
            i_new_version = get_new_version(i_beta_latest_version)
        else:
            i_prod_latest_version = get_latest_version(
                **dict(
                    root=prod_root,
                    package=i_package,
                )
            )
            i_new_version = get_new_version(i_prod_latest_version)
        #
        if version_override_enable is True:
            i_new_version = version_override

        i_kwargs = dict(
            src_root=src_root,
            beta_root=beta_root,
            prod_root=prod_root,
            package=i_package,
            version=i_new_version
        )

        i_src_package_path = '{src_root}/{package}'.format(
            **i_kwargs
        )
        #
        i_tgt_package_beta_path = '{beta_root}/{package}/{version}'.format(
            **i_kwargs
        )

        if bsc_storage.StgPathMtd.get_is_exists(i_tgt_package_beta_path) is False:
            bsc_storage.StgDirectoryMtd.set_copy_to(
                i_src_package_path, i_tgt_package_beta_path
            )


if __name__ == '__main__':
    set_push()
