set PATH=%PATH%;%LXDCC_LIB_BASE%\bin\windows-x64-python-2.7.18
set PATH=%PATH%;%LXDCC_LIB_BASE%\bin\windows-x64-python-2.7.18\Scripts
set PATH=%PATH%;%LXDCC_LIB_BASE%\bin\windows-x64-python-2.7.18-dlls
set PYTHONPATH=%PYTHONPATH%;%LXDCC_LIB_BASE%\bin\windows-x64-python-2.7.18-packages
set LYNXI_BIN_PYTHON=%LXDCC_LIB_BASE%\bin\windows-x64-python-2.7.18\python

%LYNXI_BIN_PYTHON% %LXDCC_BASE%\script\bin\python-2.7\lxapp.py %*