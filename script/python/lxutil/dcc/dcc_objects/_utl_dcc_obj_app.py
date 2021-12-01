# coding:utf-8
import os

import subprocess

from ... import utl_core


class MayaPython(object):
    def __init__(self):
        self._bin_path = '/usr/autodesk/maya2019/bin/mayapy'
        self._bin_name = 'mayapy'
        #
        environ_path_value = os.environ.get('PATH')
        if environ_path_value:
            if self._bin_path not in environ_path_value:
                os.environ['PATH'] += (os.pathsep + self._bin_path)
        else:
            os.environ['PATH'] = self._bin_path

    def set_run(self, python_command):
        command = '''"{}" -c "{}"'''.format(self._bin_name, python_command.replace('"', r'\"'))
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p

    def set_run_standalone(self, python_command):
        command = '''import maya.standalone; maya.standalone.initialize(name='python'); {}'''.format(
            python_command
        )
        p = self.set_run(command)
        results = p.stdout.readlines()
        return results


class MayaFile(object):
    def __init__(self, file_path):
        if os.path.exists(file_path):
            self._file_path = file_path
        else:
            raise TypeError(
                'file path: {} is Non-exists'.format(self._file_path)
            )
    @property
    def path(self):
        return self._file_path

    def get_reference_exists_file_paths(self):
        file_path = self.path
        if os.path.exists(file_path):
            python_commands = (
                '''from lxmaya.dcc import maya_objects;'''
                '''s=maya_objects.SceneFile();'''
                '''s.set_open("{}");'''
                '''frs = maya_objects.FileReferences();'''
                '''print frs.get_exists_file_paths()'''
            ).format(file_path)
            #
            rs = MayaPython().set_run_standalone(
                python_commands
            )
            for i in rs[:-1]:
                print i
            return eval(rs[-1])
        else:
            utl_core.Log.set_error_trace(
                'file="{}" is Non-exists'.format(file_path)
            )
