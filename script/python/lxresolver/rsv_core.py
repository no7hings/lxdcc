# coding:utf-8
import re


class ResolverMtd(object):
    @classmethod
    def _str_to_number_embedded_args_(cls, string):
        pieces = re.compile(r'(\d+)').split(unicode(string))
        pieces[1::2] = map(int, pieces[1::2])
        return pieces
    @classmethod
    def set_rsv_obj_sort(cls, rsv_objs):
        lis = []
        paths = []
        obj_dic = {}
        for rsv_obj in rsv_objs:
            path = rsv_obj.path
            paths.append(path)
            obj_dic[path] = rsv_obj
        #
        paths.sort(key=lambda x: cls._str_to_number_embedded_args_(x))
        for path in paths:
            lis.append(
                obj_dic[path]
            )
        return lis
