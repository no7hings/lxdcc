# coding:utf-8
import json

import re

from lxutil import utl_core

from lxutil.dcc import utl_dcc_obj_abs


class OsDirectory_(utl_dcc_obj_abs.AbsOsDirectory):
    def __init__(self, path):
        super(OsDirectory_, self).__init__(path)


class OsFile(utl_dcc_obj_abs.AbsOsFile):
    OS_DIRECTORY_CLS = OsDirectory_
    def __init__(self, path):
        super(OsFile, self).__init__(path)

    def set_read(self):
        pass

    def set_write(self, raw):
        self.directory.set_create()
        with open(self.path, u'w') as f:
            f.write(raw)
            utl_core.Log.set_module_result_trace(
                'file-write',
                u'file="{}"'.format(self.path)
            )

    def set_backup(self):
        backup_file_path = '{}/.backup/{}.{}{}'.format(
            self.directory.path,
            self.name_base,
            self.get_time_tag(),
            self.ext
        )
        self.set_copy_to_file(backup_file_path)


OsDirectory_.OS_FILE_CLS = OsFile


class OsPythonFile(utl_dcc_obj_abs.AbsOsFile):
    OS_DIRECTORY_CLS = OsDirectory_
    def __init__(self, path):
        super(OsPythonFile, self).__init__(path)

    def set_read(self):
        if self.get_is_exists() is True:
            with open(self.path) as p:
                raw = p.read()
                p.close()
                return raw


class OsMultiplyFile(utl_dcc_obj_abs.AbsOsFile):
    OS_DIRECTORY_CLS = OsDirectory_
    RE_MULTIPLY_PATTERNS = [r'.*?(\$F.*?)[\.]']
    def __init__(self, path):
        super(OsMultiplyFile, self).__init__(path)

    def get_has_elements(self):
        for pattern in self.RE_MULTIPLY_PATTERNS:
            re_pattern = re.compile(pattern, re.IGNORECASE)
            results = re.findall(re_pattern, self.name) or []
            if results:
                return True
        return False

    def set_file_path_convert_to_hou_seq(self):
        file_name = self.name
        pattern = r'[\.].*?(\d+.*?)[\.]'
        results = re.finditer(pattern, file_name, re.IGNORECASE) or []
        if results:
            start, end = list(results)[0].span()
            new_file_name = '{}.$F.{}'.format(file_name[:start], file_name[end:])
            new_file_path = '{}/{}'.format(self.directory.path, new_file_name)
            return new_file_path


class OsJsonFile(utl_dcc_obj_abs.AbsOsFile):
    OS_DIRECTORY_CLS = OsDirectory_
    def __init__(self, path):
        super(OsJsonFile, self).__init__(path)

    def set_read(self, encoding=None):
        if self.get_is_exists() is True:
            with open(self.path) as j:
                raw = json.load(j, encoding=encoding)
                j.close()
                return raw

    def set_write(self, raw):
        self.directory.set_create()
        utl_core.File.set_write(self.path, raw)


class OsYamlFile(utl_dcc_obj_abs.AbsOsFile):
    OS_DIRECTORY_CLS = OsDirectory_
    def __init__(self, path):
        super(OsYamlFile, self).__init__(path)

    def set_read(self):
        return utl_core.File.set_read(self.path)

    def set_write(self, raw):
        utl_core.File.set_write(self.path, raw)


class OsTexture(utl_dcc_obj_abs.AbsOsTexture):
    OS_DIRECTORY_CLS = OsDirectory_
    RE_SEQUENCE_PATTERN = r'.*?(####).*?'
    def __init__(self, path):
        super(OsTexture, self).__init__(path)


if __name__ == '__main__':
    OsDirectory_(
        '/l/prod/shl/publish/assets/chr/shuitao/srf/surfacing/shuitao.srf.surfacing.v070/texture'
    ).set_copy_to_directory(
       '/l/prod/lib/publish/assets/chr/shl__shuitao/srf/surfacing/shl__shuitao.srf.surfacing.v001/texture'
    )
