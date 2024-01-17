# coding:utf-8
import collections

import os

import copy

option = dict(
    root_src='/data/e/workspace',
    root_tgt='/job/PLE/workspace/dongchangbao/myworkspace'
)
#
package_rez_file_format_src = '{root_src}/lynxi/script/.package/rez/{package_name}/package.py'
package_bundle_file_format_src = '{root_src}/lynxi/script/.package/bundle/{package_name}/paper_configure_bundle.py'
package_rez_file_format_tgt = '{root_tgt}/{package_name}/package.py'
package_bundle_file_format_tgt = '{root_tgt}/{package_name}/paper_configure_bundle.py'
#
script_python_directory_format_src = '{root_src}/lynxi/script/python/{module_name}'
script_configure_directory_format_src = '{root_src}/lynxi/script/configure'
script_bin_directory_format_src = '{root_src}/lynxi/script/bin'
script_execute_directory_format_src = '{root_src}/lynxi/script/execute'
#
package_directory_format_tgt = '{root_tgt}/{package_name}'
package_script_directory_format_tgt = '{root_tgt}/{package_name}/script'
script_python_directory_format_tgt = '{root_tgt}/{package_name}/script/python'
script_python_module_directory_format_tgt = '{root_tgt}/{package_name}/script/python/{module_name}'
script_configure_directory_format_tgt = '{root_tgt}/{package_name}/script/configure'
script_bin_directory_format_tgt = '{root_tgt}/{package_name}/script/bin'
script_execute_directory_format_tgt = '{root_tgt}/{package_name}/script/execute'

lib_directory_format_src = '{root_src}/lynxi/lib/{name}/site-packages'
lib_directory_format_tgt = '{root_tgt}/lxdcc_lib/lib/{name}/site-packages'

lib_enable = False
package_enable = True
resource_enable = True

package_dict = collections.OrderedDict(
    {
        'lxdcc': {
            'script': [
                'lxresource', 'lxcontent', 'lxbasic',
                'lxsession', 'lxuniverse',
                #
                'lxwrap',
                #
                'lxutil',
                'lxusd',
                'lxarnold',
                'lxmaya',
                'lxkatana',
                'lxhoudini',
                'lxclarisse',
                #
                'lxresolver',
                'lxsession',
                'lxshotgun',
                #
                '.data',
                '.doc',
                '.image',
                '.icon',
                '.setup',
            ],
            #
            'package': True,
            'configure': True,
            'execute': True,
            'bin': True,
        },
        'lxdcc_gui': {
            'script': [
                'lxgui',
                'lxmaya_gui',
                'lxhoudini_gui',
                'lxkatana_gui',
                #
                'lxtool',
            ],
            'package': True,
        },
        'lxdcc_rsc': {
            'script': [
                '.setup',
                '.resources',
            ],
            'package': True,
        },
        'lxdcc_lib': {
            'package': True,
        },
    }
)

library_dict = collections.OrderedDict(
    {
        'lxdcc_lib': [
            'python-2.7',
            'linux-python-2.7',
            'linux-x64-python-2.7'
        ]
    }
)

resource_directory_format_src = '{root_src}/lynxi/resource/{resource_type}/{name}'

resource_directory_format_tgt = '{root_tgt}/lxdcc/resource/{resource_type}/{name}'

resource_dict = collections.OrderedDict(
    {
        'plug': [
            # 'maya/easy_tools',
            # 'maya/lynxinode'
        ]
    }
)

commit = '''common update'''


def run_push():
    sh_copy_commands = []
    sh_git_push_commands = []
    # library
    if lib_enable is True:
        for k, v in library_dict.items():
            i_option = copy.copy(option)
            for j in v:
                j_option = copy.copy(i_option)
                j_option['name'] = j
                j_source_path = lib_directory_format_src.format(**j_option)
                j_target_path = lib_directory_format_tgt.format(**j_option)
                sh_copy_commands.append(
                    'mkdir -p {}/'.format(j_target_path)
                )
                sh_copy_commands.append(
                    'rm -rf {}/*'.format(j_target_path)
                )
                sh_copy_commands.append(
                    'cp -rf {} {}/'.format(j_source_path, '/'.join(j_target_path.split('/')[:-1]))
                )
    # package
    if package_enable is True:
        for i_package_name, i_package_data in package_dict.items():
            i_package_option = copy.copy(option)
            i_package_option['package_name'] = i_package_name
            script_modules = i_package_data.get('script') or []
            #
            i_package_script_directory_tgt = package_script_directory_format_tgt.format(**i_package_option)
            #
            i_package_directory_src = package_directory_format_tgt.format(**i_package_option)
            i_script_python_directory_tgt = script_python_directory_format_tgt.format(**i_package_option)
            sh_copy_commands.append(
                '# push package "{}"'.format(i_package_name)
            )
            sh_copy_commands.append(
                'mkdir -p {}/'.format(i_script_python_directory_tgt)
            )
            sh_copy_commands.append(
                'rm -rf {}/*'.format(i_script_python_directory_tgt)
            )
            #
            sh_git_push_commands.append(
                'cd {}\ngit add --all\ngit commit -m "{}"'.format(i_package_directory_src, commit)
            )
            for j_module_name in script_modules:
                j_module_option = copy.copy(i_package_option)
                j_module_option['module_name'] = j_module_name
                j_script_python_directory_path_src = script_python_directory_format_src.format(**j_module_option)
                j_script_python_module_directory_path_tgt = script_python_module_directory_format_tgt.format(**j_module_option)
                sh_copy_commands.append(
                    '# push module or data "{}/{}"'.format(i_package_name, j_module_name)
                )
                sh_copy_commands.append(
                    'mkdir -p {}/'.format(j_script_python_module_directory_path_tgt)
                )
                sh_copy_commands.append(
                    'rm -rf {}/*'.format(j_script_python_module_directory_path_tgt)
                )
                sh_copy_commands.append(
                    'cp -rf {} {}/'.format(j_script_python_directory_path_src, i_script_python_directory_tgt)
                )
            #
            i_package = i_package_data.get('package') or False
            if i_package is True:
                i_package_rez_file_src = package_rez_file_format_src.format(**i_package_option)
                i_package_rez_file_tgt = package_rez_file_format_tgt.format(**i_package_option)
                sh_copy_commands.append(
                    'cp -f {} {}'.format(i_package_rez_file_src, i_package_rez_file_tgt)
                )
                i_package_bundle_file_src = package_bundle_file_format_src.format(**i_package_option)
                i_package_bundle_file_tgt = package_bundle_file_format_tgt.format(**i_package_option)
                sh_copy_commands.append(
                    'cp -f {} {}'.format(i_package_bundle_file_src, i_package_bundle_file_tgt)
                )
            #
            i_package_configure = i_package_data.get('configure') or False
            if i_package_configure is True:
                i_script_configure_directory_src = script_configure_directory_format_src.format(**i_package_option)
                i_script_configure_directory_tgt = script_configure_directory_format_tgt.format(**i_package_option)
                sh_copy_commands.append(
                    'rm -rf {}/*'.format(i_script_configure_directory_tgt)
                )
                if os.path.exists(i_script_configure_directory_src):
                    sh_copy_commands.append(
                        'cp -rf {} {}/'.format(i_script_configure_directory_src, i_package_script_directory_tgt)
                    )
            #
            i_package_bin = i_package_data.get('bin') or False
            if i_package_bin is True:
                i_directory_src = script_bin_directory_format_src.format(**i_package_option)
                i_directory_tgt = script_bin_directory_format_tgt.format(**i_package_option)
                sh_copy_commands.append(
                    'rm -rf {}/*'.format(i_directory_tgt)
                )
                if os.path.exists(i_directory_src):
                    sh_copy_commands.append(
                        'cp -rf {} {}/'.format(i_directory_src, i_package_script_directory_tgt)
                    )

            #
            i_package_execute = i_package_data.get('execute') or False
            if i_package_execute is True:
                i_directory_src = script_execute_directory_format_src.format(**i_package_option)
                i_directory_tgt = script_execute_directory_format_tgt.format(**i_package_option)
                sh_copy_commands.append(
                    'rm -rf {}/*'.format(i_directory_tgt)
                )
                if os.path.exists(i_directory_src):
                    sh_copy_commands.append(
                        'cp -rf {} {}/'.format(i_directory_src, i_package_script_directory_tgt)
                    )
    # resource
    if resource_enable is True:
        for i_resource_type, i_resource_data in resource_dict.items():
            i_option = copy.copy(option)
            i_option['resource_type'] = i_resource_type
            for j_resource_name in i_resource_data:
                j_option = copy.copy(i_option)
                j_option['name'] = j_resource_name
                j_source_path = resource_directory_format_src.format(**j_option)
                j_target_path = resource_directory_format_tgt.format(**j_option)
                sh_copy_commands.append(
                    'mkdir -p {}/'.format(j_target_path)
                )
                sh_copy_commands.append(
                    'rm -rf {}/*'.format(j_target_path)
                )
                sh_copy_commands.append(
                    'cp -rf {} {}/'.format(j_source_path, '/'.join(j_target_path.split('/')[:-1]))
                )
    # do copy
    for i in sh_copy_commands:
        print i
        os.system(i)
    # do git push
    # for i in sh_git_push_commands:
    #     print i
    #     os.system(i)


if __name__ == '__main__':
    run_push()
