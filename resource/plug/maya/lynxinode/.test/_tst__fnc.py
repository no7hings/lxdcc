# coding:utf-8
import copy

ps = [
    (1.0, 0.0, 0.0),
    (0.0, 0.0, -1.0),
    (-1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
    (1.0, 0.0, 0.0),
    (0.0, 0.0, -1.0)
]

ks = [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]


def _get_curve_knots_(count, degree, form):
    if form == 1:
        if count == 2:
            return [0.0] * degree + [1.0]
        span = max(count - 3, 1)
        M = span
        N = degree
        lis = []
        knot_minimum, knot_maximum = 0.0, float(M)
        #
        [lis.append(knot_minimum) for _ in range(degree)]
        #
        add_count = count - N - 1
        for seq in range(add_count):
            lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
        #
        [lis.append(knot_maximum) for _ in range(degree)]
        return lis
    elif form == 3:
        span = max(count - 3, 1)
        M = span
        N = degree
        lis = []
        knot_minimum, knot_maximum = 0.0, float(M) + 1
        #
        [lis.append(knot_minimum + i - degree + 1) for i in range(degree)]
        #
        add_count = count - N - 1
        for seq in range(add_count):
            lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
        #
        [lis.append(knot_maximum + i) for i in range(degree)]
        return lis


def _get_surface_knots_(count, degree, form):
    lis = []
    span = max(count - 3, 1)
    M = span
    N = degree
    knot_minimum, knot_maximum = 0.0, float(M)
    #
    add_count = count-N-1
    [lis.append(knot_minimum) for _ in range(degree)]
    #
    for seq in range(add_count):
        lis.append(float(seq + 1) * knot_maximum / (add_count + 1))
    #
    [lis.append(knot_maximum) for _ in range(degree)]
    return lis

# [0.0, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.0]


c = len(ps)
print _get_curve_knots_(6, 2, 3)
# print _get_surface_knots_(6, 2, 1)


# ps = [
#     (-1.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, -1.0), (-1.0, 0.0, -1.0), (-1.0, 0.0, 1.0), (1.0, 0.0, 1.0),
#     (-1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0), (1.0, 1.0, 1.0),
#     (-1.0, 2.0, 1.0), (1.0, 2.0, 1.0), (1.0, 2.0, -1.0), (-1.0, 2.0, -1.0), (-1.0, 2.0, 1.0), (1.0, 2.0, 1.0),
#     (-1.0, 3.0, 1.0), (1.0, 3.0, 1.0), (1.0, 3.0, -1.0), (-1.0, 3.0, -1.0), (-1.0, 3.0, 1.0), (1.0, 3.0, 1.0)
# ]
# ps__ = [
#     (-1.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, -1.0), (-1.0, 0.0, -1.0), (1.0, 0.0, 1.0), (-1.0, 0.0, 1.0),
#     (-1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, -1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0),
#     (-1.0, 2.0, 1.0), (1.0, 2.0, 1.0), (1.0, 2.0, -1.0), (-1.0, 2.0, -1.0), (1.0, 2.0, 1.0), (-1.0, 2.0, 1.0),
#     (-1.0, 3.0, 1.0), (1.0, 3.0, 1.0), (1.0, 3.0, -1.0), (-1.0, 3.0, -1.0), (1.0, 3.0, 1.0), (-1.0, 3.0, 1.0)
# ]
#
# ps_ = [
#     (-1.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, -1.0), (-1.0, 0.0, -1.0), (-1.0, 0.0, 1.0),
#     (-1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, -1.0), (-1.0, 1.0, -1.0), (-1.0, 1.0, 1.0),
#     (-1.0, 2.0, 1.0), (1.0, 2.0, 1.0), (1.0, 2.0, -1.0), (-1.0, 2.0, -1.0), (-1.0, 2.0, 1.0),
#     (-1.0, 3.0, 1.0), (1.0, 3.0, 1.0), (1.0, 3.0, -1.0), (-1.0, 3.0, -1.0), (-1.0, 3.0, 1.0)
# ]
#
# u = 4
# v = 5
#
#
# def _to_close_(points, u_count, v_count):
#     p = copy.copy(points)
#     for i_u in range(u_count):
#         i_start_index = i_u*v_count
#         i_end_index = (i_u+1)*v_count-1
#         print i_start_index, i_end_index
#         print i_end_index+i_u, i_start_index+i_u+2, 'A'
#         p.insert(i_end_index+i_u+1, p[i_start_index+i_u+1])
#
#     print p
#
#
# _to_close_(ps_, 4, 5)

# [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
# [-1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
