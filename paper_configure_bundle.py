# coding:utf-8
import os

import platform

from cosmos.env.core import EnvOperationSetter, EnvOperationList

from cosmos.util.log import get_logger

logger = get_logger(__name__)
logger.debug('loading module {0} at {1}'.format(__name__, __file__))

bundle_dir = os.path.dirname(os.path.abspath(__file__))
platform_name = platform.system().lower()

environ_data = [
    ('LXDCC_BASE', '{root}', 'set'),
    ('LYNXI_SCHEME', 'new', 'set'),
    ('LYNXI_LOG_ROOT', '/job/PLE/resource/logs', 'set'),
    ('LYNXI_CONFIGURES', '{root}/script/configure', 'append_to_path'),
    #
    ('PATH', '{root}/script/bin', 'append_to_path'),
    #
    ('PYTHONPATH', '{root}/script/python', 'append_to_path'),
    # maya
    ('PYTHONPATH', '{root}/script/python/.setup/maya/scripts', 'append_to_path'),
    # houdini
    ('HOUDINI_PATH', '{root}/script/python/.setup/houdini:&', 'append_to_path'),
    # katana
    ('KATANA_RESOURCES', '{root}/script/python/.setup/katana', 'append_to_path'),
]

environ_data_linux = [
    ('PATH', '{root}/script/bin/linux', 'append_to_path')
]

environ_data_windows = [
    ('PATH', '{root}/script/bin/windows', 'append_to_path')
]

environ_variants = dict(
    root=bundle_dir
)

ops = EnvOperationList()

for i_key, i_value, i_opt_type in environ_data:
    ops.append_env_op(i_opt_type, i_key, i_value.format(**environ_variants))

if platform_name == 'linux':
    for i_key, i_value, i_opt_type in environ_data_linux:
        ops.append_env_op(i_opt_type, i_key, i_value.format(**environ_variants))
elif platform == 'windows':
    for i_key, i_value, i_opt_type in environ_data_windows:
        ops.append_env_op(i_opt_type, i_key, i_value.format(**environ_variants))

ops.export_for_config_base()
