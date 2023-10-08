# coding:utf-8


def get_v_edge_indices(u_count, v_count):
    id_start = 0
    list_ = []
    for i_u in range(u_count):
        for i_v in range(v_count):
            i_is_corner = i_u == 0 and i_v == 0
            i_is_u_border = i_v == 0
            i_is_v_border = i_u == 0
            if i_is_corner is True:
                list_.extend([id_start, id_start+2])
                id_start += 4
            elif i_is_v_border is True:
                list_.extend([id_start, id_start + 2])
                id_start += 3
            elif i_is_u_border:
                list_.append(id_start+1)
                id_start += 3
            else:
                list_.append(id_start + 1)
                id_start += 2
    return list_


def get_u_edge_indices(u_count, v_count):
    id_start = 0
    list_ = []
    for i_u in range(u_count):
        for i_v in range(v_count):
            i_is_corner = i_u == 0 and i_v == 0
            i_is_u_border = i_v == 0
            i_is_v_border = i_u == 0
            if i_is_corner is True:
                list_.extend([id_start+1, id_start+3])
                id_start += 4
            elif i_is_v_border is True:
                list_.extend([id_start+1])
                id_start += 3
            elif i_is_u_border:

                list_.extend([id_start, id_start+2])
                id_start += 3
            else:
                list_.append(id_start)
                id_start += 2
    return list_


print get_v_edge_indices(5, 10)

print get_u_edge_indices(5, 10)
