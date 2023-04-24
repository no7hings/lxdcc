# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import lxmaya.fnc.exporters as mya_fnc_exporters


def set_look_materialx_export(file_path, root=None, look='default', path_lstrip=0, path_rstrip=0):
    """
    :param file_path: str(<file-path>)
    :param root: str(<dcc-path>)
    :param look: str(<look>)
    :param path_lstrip: int(<index>)
    :param path_rstrip: int(<index>)
    :return: list[str(<result>)]
    """
    exporter = mya_fnc_exporters.LookMtlxExporter(
        file_path=file_path, root=root, look=look
    )
    exporter.set_run()
    return exporter.get_outputs()
