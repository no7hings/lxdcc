# coding:utf-8
from ._bsc_cor_utility import *

from lxbasic.core import _bsc_cor_raw


class DccPathDagMtd(object):
    @classmethod
    def get_dag_args(cls, path, pathsep='/'):
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
    def get_dag_name(cls, path, pathsep='/'):
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
    def get_dag_parent(cls, path, pathsep='/'):
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
    def get_dag_component_paths(cls, path, pathsep='/'):
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
    def get_dag_name_with_namespace_clear(cls, name, namespacesep=':'):
        return name.split(namespacesep)[-1]
    @classmethod
    def get_dag_path_with_namespace_clear(cls, path, pathsep='/', namespacesep=':'):
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
    def get_dag_path(cls, dag_args, pathsep='/'):
        return pathsep.join(dag_args)
    @classmethod
    def get_dag_pathsep_replace(cls, path, pathsep_src='/', pathsep_tgt='/'):
        if path == pathsep_src:
            return pathsep_tgt
        return pathsep_tgt.join(cls.get_dag_args(path, pathsep=pathsep_src))
    @classmethod
    def get_dag_children(cls, path, paths, pathsep='/'):
        lis = []
        for i_path in paths:
            # r'/shl/chr/test_0/[^/]*'
            _ = re.match(
                r'{0}{1}[^{1}]*'.format(path, pathsep), i_path
            )
            if _ is not None:
                if _.group() == i_path:
                    lis.append(i_path)
        return lis
    @classmethod
    def set_dag_path_cleanup(cls, path, pathsep='/'):
        return re.sub(
            ur'[^\u4e00-\u9fa5a-zA-Z0-9{}]'.format(pathsep), '_', path
        )


class DccPathDagOpt(object):
    def __init__(self, path):
        self._pathsep = path[0]
        self._path = path

    def get_name(self):
        return DccPathDagMtd.get_dag_name(
            path=self._path, pathsep=self._pathsep
        )
    name = property(get_name)

    def set_name(self, name):
        self._path = self._pathsep.join(
            [self.get_parent_path(), name]
        )

    def get_pathsep(self):
        return self._pathsep
    pathsep = property(get_pathsep)

    def get_path(self):
        return self._path
    path = property(get_path)

    def get_value(self):
        return self._path
    value = property(get_value)

    def get_root(self):
        return self.__class__(self.pathsep)

    def get_is_root(self):
        return self.path == self.pathsep

    def get_parent_path(self):
        return DccPathDagMtd.get_dag_parent(
            path=self._path, pathsep=self._pathsep
        )

    def set_parent_path(self, path):
        # noinspection PyAugmentAssignment
        self._path = path + self._path

    def get_ancestor_paths(self):
        return self.get_component_paths()[1:]

    def get_ancestors(self):
        return [self.__class__(i) for i in self.get_ancestor_paths()]

    def get_parent(self):
        _ = self.get_parent_path()
        if _:
            return self.__class__(
                self.get_parent_path()
            )

    def get_component_paths(self):
        return DccPathDagMtd.get_dag_component_paths(
            path=self._path, pathsep=self._pathsep
        )

    def get_components(self):
        return [self.__class__(i) for i in self.get_component_paths()]

    def set_translate_to(self, pathsep='/'):
        return self.__class__(
            DccPathDagMtd.get_dag_pathsep_replace(
                self.path,
                pathsep_src=self.pathsep,
                pathsep_tgt=pathsep
            )
        )

    def set_namespace_clear_to(self):
        return self.__class__(
            DccPathDagMtd.get_dag_path_with_namespace_clear(
                self.path,
                pathsep=self.pathsep,
                # namespacesep=':',
            )
        )

    def get_name_namespace(self, namespacesep=':'):
        name = self.get_name()
        _ = name.split(namespacesep)
        # print _
        return namespacesep.join(_[:-1])

    def get_color_from_name(self, count=1000, maximum=255, offset=0, seed=0):
        return _bsc_cor_raw.RawColorMtd.get_color_from_string(
            self.get_name(), count=count, maximum=maximum, offset=offset, seed=seed
        )

    def get_rgb_from_index(self, index, count, maximum=255, seed=0):
        pass

    def get_path_prettify(self, maximum=18):
        p = self.path
        n = self.name
        #
        d = p[:-len(n)-1]
        c = len(d)
        if c > maximum:
            return u'{}...{}/{}'.format(d[:(int(maximum/2)-3)], d[-(int(maximum/2)):], n)
        return p

    def __str__(self):
        return self._path

    def __repr__(self):
        return self.__str__()

    def to_string(self):
        return self._path


class DccAttrPathMtd(object):
    @classmethod
    def get_atr_path(cls, obj_path, port_path, port_pathsep='.'):
        return port_pathsep.join([obj_path, port_path])


class DccAttrPathOpt(object):
    def __init__(self, atr_path, port_pathsep='.'):
        self._path = atr_path
        self._port_pathsep = port_pathsep
        _ = self._path.split(self._port_pathsep)
        self._obj_path = _[0]
        self._port_path = self._port_pathsep.join(_[1:])
    @property
    def path(self):
        return self._path
    @property
    def obj_path(self):
        return self._obj_path
    @property
    def port_path(self):
        return self._port_path

    def to_args(self):
        return self._obj_path, self._port_path
