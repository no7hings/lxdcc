# coding:utf-8
import os

from urllib import quote, unquote

import platform

import locale

import subprocess

import getpass


def main(file, movie_file='', description=''):
    user = getpass.getuser()

    env = dict(os.environ)
    env = {str(k): str(v) for k, v in env.items()}
    env['REZ_BETA'] = '1'

    description = quote(description.encode('utf-8'))
    description = description.replace('%', r'///')

    cmd = r'rez-env lxdcc -c "lxhook-command -o \"option_hook_key=rsv-task-batchers/asset/gen-model-export-extra&choice_scheme=asset-maya-publish&file={file}&movie_file={movie_file}&user={user}&description={description}&td_enable={td_enable}&rez_beta={rez_beta}&deadline_enable={deadline_enable}\""'.format(
        file=file,
        description=description,
        user=user,
        movie_file=movie_file,
        td_enable=False,
        rez_beta=True,
        deadline_enable=True,
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
        startupinfo=NO_WINDOW,
        env=env
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
        file='l:/prod/cgm/work/assets/chr/td_test/mod/modeling/maya/scenes/td_test.mod.modeling.v017.ma',
    )