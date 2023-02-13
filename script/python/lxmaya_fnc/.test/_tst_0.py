# coding:utf-8
import lxmaya.dcc.dcc_objects as mya_dcc_objects

root = mya_dcc_objects.Group('|master|hi')
mesh_paths = root.get_all_shape_paths(include_obj_type='mesh')
mesh_objs = [mya_dcc_objects.Mesh(i) for i in mesh_paths]
for mesh_obj in mesh_objs:
    print mesh_obj.get_edge_non_manifold_comp_names()
    print mesh_obj.get_vertex_non_manifold_comp_names()
    #
    print mesh_obj.get_face_n_side_comp_names()
    print mesh_obj.get_face_non_triangulable_comp_names()
    print mesh_obj.get_face_lamina_comp_names()
    print mesh_obj.get_edge_open_comp_names()
