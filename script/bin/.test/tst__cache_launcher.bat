@echo off
pushd %~d0

set /a shell_start_s=%time:~6,2%
set /a shell_start_m=%time:~3,2%

REM
REM
REM ################################################################################
REM system setup
REM ################################################################################
set REZ_USED=l:\packages\pg\prod\rez\2.50.0\platform-windows\lib\site-packages\rez
set REZ_USED_VERSION=2.50.0
set REZ_USED_TIMESTAMP=1642489658
set REZ_USED_REQUESTED_TIMESTAMP=0
set REZ_USED_REQUEST=lxdcc
set REZ_USED_IMPLICIT_PACKAGES=C:\Users\platform==windows ~arch==AMD64 ~os==windows-10.0.18362
set REZ_USED_RESOLVE=lxdcc_fnc-99.99.99 lxdcc_rsc-99.99.99 lxdcc_gui-99.99.99 lxdcc_prd-0.0.119 lxdcc_lib-0.0.2 lxdcc-99.99.99
set REZ_USED_PACKAGES_PATH=%HOMEPATH%\packages;%HOMEPATH%\.rez\packages\int;%HOMEPATH%\.rez\packages\ext;L:\packages\pg\prod;L:\packages\pg\dept;L:\packages\pg\third_party\app;L:\packages\pg\third_party\plugin;L:\packages\pg\third_party\ocio
set REZ_VERSION=2.50.0
set REZ_PATH=l:\packages\pg\prod\rez\2.50.0\platform-windows\lib\site-packages\rez
set REZ_REQUEST=lxdcc ~platform==windows ~arch==AMD64 ~os==windows-10.0.18362
set REZ_RESOLVE=lxdcc_fnc-99.99.99 lxdcc_rsc-99.99.99 lxdcc_gui-99.99.99 lxdcc_prd-0.0.119 lxdcc_lib-0.0.2 lxdcc-99.99.99
set REZ_RAW_REQUEST=lxdcc ~platform==windows ~arch==AMD64 ~os==windows-10.0.18362
set REZ_RESOLVE_MODE=latest
REM
REM
REM ################################################################################
REM package variables
REM ################################################################################
REM
REM variables for package lxdcc_fnc-99.99.99[]
REM --------------------------------------------------------------------------------
set REZ_LXDCC_FNC_VERSION=99.99.99
set REZ_LXDCC_FNC_MAJOR_VERSION=99
set REZ_LXDCC_FNC_MINOR_VERSION=99
set REZ_LXDCC_FNC_PATCH_VERSION=99
set REZ_LXDCC_FNC_BASE=%HOMEPATH%\packages\lxdcc_fnc\99.99.99
set REZ_LXDCC_FNC_ROOT=%HOMEPATH%\packages\lxdcc_fnc\99.99.99
REM
REM variables for package lxdcc_rsc-99.99.99[]
REM --------------------------------------------------------------------------------
set REZ_LXDCC_RSC_VERSION=99.99.99
set REZ_LXDCC_RSC_MAJOR_VERSION=99
set REZ_LXDCC_RSC_MINOR_VERSION=99
set REZ_LXDCC_RSC_PATCH_VERSION=99
set REZ_LXDCC_RSC_BASE=%HOMEPATH%\packages\lxdcc_rsc\99.99.99
set REZ_LXDCC_RSC_ROOT=%HOMEPATH%\packages\lxdcc_rsc\99.99.99
REM
REM variables for package lxdcc_gui-99.99.99[]
REM --------------------------------------------------------------------------------
set REZ_LXDCC_GUI_VERSION=99.99.99
set REZ_LXDCC_GUI_MAJOR_VERSION=99
set REZ_LXDCC_GUI_MINOR_VERSION=99
set REZ_LXDCC_GUI_PATCH_VERSION=99
set REZ_LXDCC_GUI_BASE=%HOMEPATH%\packages\lxdcc_gui\99.99.99
set REZ_LXDCC_GUI_ROOT=%HOMEPATH%\packages\lxdcc_gui\99.99.99
REM
REM variables for package lxdcc_prd-0.0.119[]
REM --------------------------------------------------------------------------------
set REZ_LXDCC_PRD_VERSION=0.0.119
set REZ_LXDCC_PRD_MAJOR_VERSION=0
set REZ_LXDCC_PRD_MINOR_VERSION=0
set REZ_LXDCC_PRD_PATCH_VERSION=119
set REZ_LXDCC_PRD_BASE=l:\packages\pg\prod\lxdcc_prd\0.0.119
set REZ_LXDCC_PRD_ROOT=l:\packages\pg\prod\lxdcc_prd\0.0.119
REM
REM variables for package lxdcc_lib-0.0.2[]
REM --------------------------------------------------------------------------------
set REZ_LXDCC_LIB_VERSION=0.0.2
set REZ_LXDCC_LIB_MAJOR_VERSION=0
set REZ_LXDCC_LIB_MINOR_VERSION=0
set REZ_LXDCC_LIB_PATCH_VERSION=2
set REZ_LXDCC_LIB_BASE=l:\packages\pg\prod\lxdcc_lib\0.0.2
set REZ_LXDCC_LIB_ROOT=l:\packages\pg\prod\lxdcc_lib\0.0.2
REM
REM variables for package lxdcc-99.99.99[]
REM --------------------------------------------------------------------------------
set REZ_LXDCC_VERSION=99.99.99
set REZ_LXDCC_MAJOR_VERSION=99
set REZ_LXDCC_MINOR_VERSION=99
set REZ_LXDCC_PATCH_VERSION=99
set REZ_LXDCC_BASE=%HOMEPATH%\packages\lxdcc\99.99.99
set REZ_LXDCC_ROOT=%HOMEPATH%\packages\lxdcc\99.99.99
REM
REM
REM ################################################################################
REM commands
REM ################################################################################
REM
REM commands from package lxdcc_fnc-99.99.99[]
REM --------------------------------------------------------------------------------
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python
REM
REM commands from package lxdcc_rsc-99.99.99[]
REM --------------------------------------------------------------------------------
set PAPER_EXTEND_RESOURCES=%HOMEPATH%\packages\lxdcc_rsc\99.99.99/script/python/.resources
REM
REM commands from package lxdcc_gui-99.99.99[]
REM --------------------------------------------------------------------------------
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python
REM
REM commands from package lxdcc_prd-0.0.119[]
REM --------------------------------------------------------------------------------
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python
REM
REM commands from package lxdcc_lib-0.0.2[]
REM --------------------------------------------------------------------------------
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/python-2.7/site-packages
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-python-2.7/site-packages
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-x64-python-2.7/site-packages
REM
REM commands from package lxdcc-99.99.99[]
REM --------------------------------------------------------------------------------
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-x64-python-2.7/site-packages;%HOMEPATH%\packages\lxdcc\99.99.99/lib/python/module/python-2.7
set PATH=%HOMEPATH%\packages\lxdcc\99.99.99/script/bin
set PATH=%HOMEPATH%\packages\lxdcc\99.99.99/script/bin;%HOMEPATH%\packages\lxdcc\99.99.99/script/bin/windows
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-x64-python-2.7/site-packages;%HOMEPATH%\packages\lxdcc\99.99.99/lib/python/module/python-2.7;%HOMEPATH%\packages\lxdcc\99.99.99/script/python
set PYTHONPATH=%HOMEPATH%\packages\lxdcc_fnc\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_fnc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc_gui\99.99.99/lib/python/site-packages;%HOMEPATH%\packages\lxdcc_gui\99.99.99/script/python;l:\packages\pg\prod\lxdcc_prd\0.0.119/lib/python/site-packages;l:\packages\pg\prod\lxdcc_prd\0.0.119/script/python;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-python-2.7/site-packages;l:\packages\pg\prod\lxdcc_lib\0.0.2/lib/windows-x64-python-2.7/site-packages;%HOMEPATH%\packages\lxdcc\99.99.99/lib/python/module/python-2.7;%HOMEPATH%\packages\lxdcc\99.99.99/script/python;%HOMEPATH%\packages\lxdcc\99.99.99/script/python/.setup/maya/scripts
set HOUDINI_PATH=%HOMEPATH%\packages\lxdcc\99.99.99/script/python/.setup/houdini:^&
set KATANA_RESOURCES=%HOMEPATH%\packages\lxdcc\99.99.99/script/python/.setup/katana
REM
REM
REM ################################################################################
REM post system setup
REM ################################################################################
set PATH=%HOMEPATH%\packages\lxdcc\99.99.99/script/bin;%HOMEPATH%\packages\lxdcc\99.99.99/script/bin/windows;L:\packages\pg\prod\pg_python_lib\9.9.9\bin;L:\packages\pg\prod\pg_tools\9.9.9\bin;C:\Program Files\NVIDIA Corporation\NVIDIA NGX;L:\packages\pg\prod\rez\current\platform-windows\Scripts\rez;C:\Windows\System32\OpenSSH\;L:\packages\pg\prod\pg_production_lib\9.9.9\bin;C:\Windows;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\Wbem;C:\Windows\system32
set PATH=%HOMEPATH%\packages\lxdcc\99.99.99/script/bin;%HOMEPATH%\packages\lxdcc\99.99.99/script/bin/windows;L:\packages\pg\prod\pg_python_lib\9.9.9\bin;L:\packages\pg\prod\pg_tools\9.9.9\bin;C:\Program Files\NVIDIA Corporation\NVIDIA NGX;L:\packages\pg\prod\rez\current\platform-windows\Scripts\rez;C:\Windows\System32\OpenSSH\;L:\packages\pg\prod\pg_production_lib\9.9.9\bin;C:\Windows;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\Wbem;C:\Windows\system32;l:\packages\pg\prod\rez\current\platform-windows\scripts\rez

lxhook-python -o "hook_key=kit-panels/app-kit"

echo. & pause