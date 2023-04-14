# coding:utf-8
from lxutil.fnc import utl_fnc_obj_abs

import lxkatana.dcc.dcc_objects as ktn_dcc_objects


class TextureExporter(
    utl_fnc_obj_abs.AbsDccTextureExport,
    utl_fnc_obj_abs.AbsFncOptionMethod,
):
    FIX_NAME_BLANK = 'fix_name_blank'
    USE_TX = 'use_tx'
    WITH_REFERENCE = 'width_reference'
    OPTION = dict(
        directory_base='',
        directory='',
        location='',
        fix_name_blank=False,
        use_tx=False,
        width_reference=False,
        use_environ_map=False,
    )
    def __init__(self, option=None):
        super(TextureExporter, self).__init__(option)
        self._directory_path_dst = self.get('directory')
        self._directory_path_base = self.get('directory_base')
        self._location = self.get('location')

    def set_run(self):
        from lxkatana import ktn_core

        import lxkatana.scripts as ktn_scripts
        #
        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return

        s = ktn_scripts.ScpLookOutput(opt)

        location = s.get_geometry_root()
        #
        texture_references = ktn_dcc_objects.TextureReferences()
        dcc_shaders = s.get_all_dcc_geometry_shaders_by_location(location)
        dcc_objs = texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        self._set_copy_as_src_(
            directory_path_dst=self._directory_path_dst, 
            directory_path_base=self._directory_path_base,
            dcc_objs=dcc_objs,
            fix_name_blank=self.get('fix_name_blank'),
            use_tx=self.get('use_tx'),
            with_reference=self.get('width_reference'),
            #
            ignore_missing_texture=True,
            remove_expression=True,
            use_environ_map=self.get('use_environ_map'),
            #
            repath_fnc=texture_references.set_obj_repath_to,
        )
