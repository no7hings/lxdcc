# coding:utf-8
from lxobj import obj_configure


class DccPathDagMtd(object):
    @classmethod
    def get_dag_args(cls, path, pathsep=obj_configure.Obj.PATHSEP):
        """
        :param path: str(<obj-path>)
        :param pathsep: 
        :return: list[str(<obj-name>), ...]
        """
        if pathsep is None:
            raise TypeError()
        # is <root-obj>, etc: "/"
        if path == pathsep:
            return [pathsep, ]
        # is <obj>, etc: "/obj"
        return path.split(pathsep)
    @classmethod
    def get_dag_name(cls, path, pathsep=obj_configure.Obj.PATHSEP):
        """
        :param path:
        :param pathsep: 
        :return:
        """
        # is <root-obj>, etc: "/"
        if path == pathsep:
            return pathsep
        # is <obj>, etc: "/obj"
        return cls.get_dag_args(path, pathsep)[-1]
    @classmethod
    def get_dag_parent(cls, path, pathsep=obj_configure.Obj.PATHSEP):
        """
        :param path:
        :param pathsep: 
        :return:
        """
        dag_args = cls.get_dag_args(path, pathsep)
        # windows file-path-root etc: "D:/directory"
        if ':' in dag_args[0]:
            if len(dag_args) == 1:
                return None
            else:
                return pathsep.join(dag_args[:-1])
        else:
            if len(dag_args) == 1:
                return None
            elif len(dag_args) == 2:
                return pathsep
            else:
                return pathsep.join(dag_args[:-1])
    @classmethod
    def get_dag_component_paths(cls, path, pathsep=obj_configure.Obj.PATHSEP):
        """
        :param path:
        :param pathsep: 
        :return: list[str(<obj-path>)]
        """
        def _rcs_fnc(lis_, path_):
            if path_ is not None:
                lis_.append(path_)
                _parent_path = cls.get_dag_parent(path_, pathsep)
                if _parent_path:
                    _rcs_fnc(lis_, _parent_path)

        lis = []
        _rcs_fnc(lis, path)
        return lis
    @classmethod
    def get_dag_name_with_namespace_clear(cls, name, namespacesep=obj_configure.Obj.NAMESPACESEP):
        return name.split(namespacesep)[-1]
    @classmethod
    def get_dag_path_with_namespace_clear(cls, path, pathsep=obj_configure.Obj.PATHSEP, namespacesep=obj_configure.Obj.NAMESPACESEP):
        dag_args = cls.get_dag_args(path, pathsep)
        lis = []
        for i in dag_args:
            lis.append(cls.get_dag_name_with_namespace_clear(i, namespacesep))
        return cls.get_dag_path(lis, pathsep)
    @classmethod
    def get_dag_path_lstrip(cls, path, lstrip=None):
        if lstrip is not None:
            if path.startswith(lstrip):
                return path[len(lstrip):]
            elif lstrip.startswith(path):
                return ''
            return path
        return path
    @classmethod
    def get_dag_path(cls, dag_args, pathsep=obj_configure.Obj.PATHSEP):
        return pathsep.join(dag_args)
    @classmethod
    def get_dag_pathsep_replace(cls, path, pathsep_src=obj_configure.Obj.PATHSEP, pathsep_tgt=obj_configure.Obj.PATHSEP):
        if path == pathsep_src:
            return pathsep_tgt
        return pathsep_tgt.join(cls.get_dag_args(path, pathsep=pathsep_src))


class AtrPathMtd(object):
    @classmethod
    def set_atr_path_split(cls, path, pathsep=obj_configure.Port.PATHSEP):
        _ = path.split(pathsep)
        return _[0], pathsep.join(_[1:])


class PortPathMethod(object):
    @classmethod
    def get_dag_args(cls, path, pathsep=obj_configure.Obj.PATHSEP):
        return path.split(pathsep)
    @classmethod
    def get_dag_name(cls, path, pathsep=obj_configure.Obj.PATHSEP):
        return cls.get_dag_args(path, pathsep)[-1]
    @classmethod
    def get_dag_parent(cls, path, pathsep):
        dag_args = cls.get_dag_args(path, pathsep)
        if len(dag_args) == 1:
            return None
        elif len(dag_args) == 2:
            return pathsep
        else:
            return pathsep.join(dag_args[:-1])
