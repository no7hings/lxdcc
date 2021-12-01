# coding:utf-8
from lxbasic import bsc_core
#
from lxutil import utl_core


class AbsCfg(object):
    def __init__(self, configure):
        self._configure = configure
        self._set_build_()

    def _set_build_(self):
        raise NotImplementedError()

    def __str__(self):
        return self._configure.__str__()


class TextureTxCfg(AbsCfg):
    def __init__(self, configure):
        super(TextureTxCfg, self).__init__(configure)

    def _set_build_(self):
        self._color_space_dict = {}
        self._purpose_dict = {}
        purposes = self._configure.get_branch_keys('tx')
        for purpose in purposes:
            name_patterns = self._configure.get('tx.{}.name-patterns'.format(purpose))
            color_space = self._configure.get('tx.{}.color-space'.format(purpose))
            for i_name_pattern in name_patterns:
                self._color_space_dict[i_name_pattern] = color_space
                self._purpose_dict[i_name_pattern] = purpose

    def get_name_patterns(self):
        return self._color_space_dict.keys()
    @classmethod
    def get_color_space(cls, file_path):
        from lxarnold import and_core
        #
        return and_core.AndTextureOpt_(file_path).get_color_space()

    def get_used_color_space(self, file_path):
        from lxarnold import and_core
        #
        file_opt = bsc_core.StorageFileOpt(file_path)
        _ = 'auto'
        for i_name_pattern in self.get_name_patterns():
            if file_opt.get_is_match_name_pattern(i_name_pattern) is True:
                _ = self._color_space_dict[i_name_pattern]
                break
        #
        if _ == 'auto':
            return and_core.AndTextureOpt_(file_path).get_color_space()
        return _

    def get_purpose(self, file_path):
        file_opt = bsc_core.StorageFileOpt(file_path)
        for i_name_pattern in self.get_name_patterns():
            if file_opt.get_is_match_name_pattern(i_name_pattern) is True:
                return self._purpose_dict[i_name_pattern]
        return 'unknown'


class ColorSpaceCfg(AbsCfg):
    def __init__(self, configure):
        super(ColorSpaceCfg, self).__init__(configure)
    @classmethod
    def get_is_use_aces(cls):
        return utl_core.Environ.get('OCIO') is not None

    def _set_build_(self):
        self._convert_dict = self._configure.get('aces.convert')

    def get_aces_color_spaces(self):
        return self._configure.get('aces.color-spaces')

    def get_aces_render_color_space(self):
        return self._configure.get('aces.default-color-space')

    def get_aces_file(self):
        _ = utl_core.Environ.get('OCIO')
        if _ is not None:
            return _
        return self._configure.get('aces.file')

    def get_aces_color_space(self, color_space):
        if self.get_is_use_aces() is True:
            return self._convert_dict[color_space]
        return color_space
