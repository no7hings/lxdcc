@echo off
pushd %~d0

set /a shell_start_m=%time:~3,2%
set /a shell_start_s=%time:~6,2%

rez-env lxdcc -- lxhook-python -o "hook_key=kit-panels/app-kit"

echo. & pause