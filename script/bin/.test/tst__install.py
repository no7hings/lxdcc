# coding:utf-8

lis = [
    (
        '@echo off\n'
        'pushd %~d0\n'
    )
]

for i in [
    'lxdcc',
    'lxdcc_fnc',
    'lxdcc_gui',
    # 'lxdcc_lib',
    'lxdcc_rsc',
    # 'test'
]:
    i_kwargs = dict(
        package=i
    )
    i_cmd = (
        'if exist %HOMEPATH%\\packages\\{package} (\n'
        '    echo %HOMEPATH%\\packages\\{package} is exists\n'
        ') else (\n'
        '    mkdir %HOMEPATH%\\packages\\{package}\n'
        ')\n'
        'if exist %HOMEPATH%\\packages\\{package}\\99.99.99 (\n'
        '    echo %HOMEPATH%\\packages\\{package}\\99.99.99 is exists\n'
        ') else (\n'
        '    mklink /D %HOMEPATH%\\packages\\{package}\\99.99.99 L:\\temp\\td\\dongchangbao\\myworkspace\\{package}\n'
        ')\n'
    ).format(
        **i_kwargs
    )
    lis.append(
        i_cmd
    )
lis.append(
    (
        'popd\n'
        'echo. & pause\n'
    )
)

print ''.join(
    lis
)
