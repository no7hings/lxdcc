# coding:utf-8
import os


def _set_symlink_create_(src_path, tgt_path):
    tgt_dir_path = os.path.dirname(tgt_path)
    src_rel_path = os.path.relpath(src_path, tgt_dir_path)
    if os.path.exists(tgt_path) is False:
        print src_rel_path, tgt_path
        os.symlink(src_rel_path, tgt_path)


_set_symlink_create_(
    '/data/f/paper_workspace/pglauncher/src/cjd_config', '/data/f/paper_workspace/pglauncher/src/lib_config'
)
