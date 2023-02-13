# coding:utf-8
from lxhoudini_fnc import hou_fnc_abstract

import lxhoudini.dcc.dcc_objects as hou_dcc_objects


class Method(hou_fnc_abstract.AbsHouIspOp):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    #
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        #
        error_obj_files = []
        textures = obj.get_textures()
        for texture in textures:
            if texture.get_is_exists() is False:
                error_obj_files.append(texture)
        #
        self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs
    # Rename Texture-file-name & Repath Node
    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()

        materialxs = hou_dcc_objects.Materialxs().get_objs()
        self._set_objs_check_(materialxs)
