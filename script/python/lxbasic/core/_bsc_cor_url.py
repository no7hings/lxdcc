# coding:utf-8
import os

from lxbasic.core import _bsc_cor_utility, _bsc_cor_log


class UrlMtd(object):
    WINDOWS_BIN_PATHS = [
        "C:/google/Chrome/Application/chrome.exe",
        "D:/google/Chrome/Application/chrome.exe"
    ]
    LINUX_BIN_PATHS = [
        "/opt/google/chrome/google-chrome"
    ]
    @classmethod
    def open_in_chrome(cls, url):
        if _bsc_cor_utility.SystemMtd.get_is_linux():
            bin_paths = cls.LINUX_BIN_PATHS
        elif _bsc_cor_utility.SystemMtd.get_is_windows():
            bin_paths = cls.WINDOWS_BIN_PATHS
        else:
            raise RuntimeError()
        #
        exists_bin_paths = [i for i in bin_paths if os.path.isfile(i)]
        if exists_bin_paths:
            import webbrowser
            webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(exists_bin_paths[0]))
            webbrowser.get('Chrome').open(
                url, new=1
            )
        else:
            _bsc_cor_log.LogMtd.get_method_error(
                'url method', 'chrome is not found'
            )
