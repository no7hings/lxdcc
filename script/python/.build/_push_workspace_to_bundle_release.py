# coding:utf-8
import os

import glob

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

src_root = '/l/temp/td/dongchangbao/myworkspace'

beta_root = '/job/PLE/bundle/thirdparty'

prod_root = '/job/PLE/bundle/thirdparty'

packages = [
    'lxdcc',
    'lxdcc_gui',
    'lxdcc_rsc',
    # 'lxdcc_lib',
]

version_override = 'master-1'
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
    return 'master-0'


def get_new_version(version):
    _ = version.split('-')
    _.reverse()
    for seq, i in enumerate(_):
        if str(i).isdigit():
            _[seq] = str(int(i) + 1)
            break

    _.reverse()
    return '-'.join(_)


def run_push():
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

        if version_override_enable is True:
            i_new_version = version_override

        i_kwargs = dict(
            src_root=src_root,
            beta_root=beta_root,
            prod_root=prod_root,
            package=i_package,
            version=i_new_version
        )

        i_package_path_src = '{src_root}/{package}'.format(
            **i_kwargs
        )

        i_package_path_beta_tgt = '{beta_root}/{package}/{version}'.format(
            **i_kwargs
        )
        if bsc_storage.StgPathMtd.get_is_exists(i_package_path_beta_tgt) is False:
            bsc_storage.StgDirectoryMtd.set_copy_to(
                i_package_path_src, i_package_path_beta_tgt, excludes=['/.git/*']
            )

            os.system(
                'chmod -R 775 {}'.format(i_package_path_beta_tgt)
            )


if __name__ == '__main__':
    run_push()
