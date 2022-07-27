# coding:utf-8
from urllib import quote, unquote

import platform

import locale

import subprocess

import getpass


def main(file, movie_file, description):
    user = getpass.getuser()
    cmd = r'rez-env lxdcc -c "lxhook-command -o \"option_hook_key=rsv-task-batchers/asset/gen-rig-export&choice_scheme=asset-maya-publish&file={file}&movie_file={movie_file}&user={user}&description={description}&td_enable={td_enable}\""'.format(
        file=file,
        description=quote(description.encode(locale.getdefaultlocale()[1])),
        user=user,
        movie_file=movie_file,
        td_enable=True
    )

    cmd = cmd.decode(locale.getdefaultlocale()[1])

    if platform.system() == 'Windows':
        cmd = cmd.replace("&", "^&")
    elif platform.system() == 'Linux':
        pass

    print repr(cmd)

    if platform.system() == 'Windows':
        # noinspection PyUnresolvedReferences
        NO_WINDOW = subprocess.STARTUPINFO()
        NO_WINDOW.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        NO_WINDOW = None

    s_p = subprocess.Popen(
        cmd,
        shell=True,
        # close_fds=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        startupinfo=NO_WINDOW
    )
    while True:
        next_line = s_p.stdout.readline()
        #
        return_line = next_line
        if return_line == '' and s_p.poll() is not None:
            break
        #
        return_line = return_line.decode('gbk', 'ignore')
        # noinspection PyBroadException
        try:
            print(return_line.encode('gbk').rstrip())
        except:
            pass
    #
    retcode = s_p.poll()
    if retcode:
        raise subprocess.CalledProcessError(retcode, cmd)
    #
    s_p.stdout.close()


if __name__ == '__main__':
    main(
        file='/l/prod/cgm/work/assets/chr/ext_woodpecker/rig/rigging/maya/scenes/ext_woodpecker.rig.rigging.v001.ma',
        description=u'测试',
        # description = 'td_test'
        movie_file='/l/prod/cgm/publish/assets/chr/bl_xiz_f/rig/rigging/bl_xiz_f.rig.rigging.v014/review/bl_xiz_f.rig.rigging.v014.mov',
    )
