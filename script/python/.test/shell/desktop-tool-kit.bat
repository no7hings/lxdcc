@echo off
pushd %~d0

paper lxdcc lxhook-command -o "hook_key=desktop-tools/desktop-tool-kit"

popd
echo. & pause