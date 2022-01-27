@echo off
pushd %~d0
if exist %HOMEPATH%\packages\lxdcc (
    echo %HOMEPATH%\packages\lxdcc is exists
) else (
    mkdir %HOMEPATH%\packages\lxdcc
)
if exist %HOMEPATH%\packages\lxdcc\99.99.99 (
    echo %HOMEPATH%\packages\lxdcc\99.99.99 is exists
) else (
    mklink /D %HOMEPATH%\packages\lxdcc\99.99.99 L:\temp\td\dongchangbao\myworkspace\lxdcc
)
if exist %HOMEPATH%\packages\lxdcc_fnc (
    echo %HOMEPATH%\packages\lxdcc_fnc is exists
) else (
    mkdir %HOMEPATH%\packages\lxdcc_fnc
)
if exist %HOMEPATH%\packages\lxdcc_fnc\99.99.99 (
    echo %HOMEPATH%\packages\lxdcc_fnc\99.99.99 is exists
) else (
    mklink /D %HOMEPATH%\packages\lxdcc_fnc\99.99.99 L:\temp\td\dongchangbao\myworkspace\lxdcc_fnc
)
if exist %HOMEPATH%\packages\lxdcc_gui (
    echo %HOMEPATH%\packages\lxdcc_gui is exists
) else (
    mkdir %HOMEPATH%\packages\lxdcc_gui
)
if exist %HOMEPATH%\packages\lxdcc_gui\99.99.99 (
    echo %HOMEPATH%\packages\lxdcc_gui\99.99.99 is exists
) else (
    mklink /D %HOMEPATH%\packages\lxdcc_gui\99.99.99 L:\temp\td\dongchangbao\myworkspace\lxdcc_gui
)
if exist %HOMEPATH%\packages\lxdcc_rsc (
    echo %HOMEPATH%\packages\lxdcc_rsc is exists
) else (
    mkdir %HOMEPATH%\packages\lxdcc_rsc
)
if exist %HOMEPATH%\packages\lxdcc_rsc\99.99.99 (
    echo %HOMEPATH%\packages\lxdcc_rsc\99.99.99 is exists
) else (
    mklink /D %HOMEPATH%\packages\lxdcc_rsc\99.99.99 L:\temp\td\dongchangbao\myworkspace\lxdcc_rsc
)
popd
echo. & pause