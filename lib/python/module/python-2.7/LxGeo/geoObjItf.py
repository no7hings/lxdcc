# coding:utf-8


# data *************************************************************************************************************** #
class ItfGeoData(object):
    def _initItfGeoData(self, *args, **kwargs):
        self._raw = args[0]
    
    def raw(self):
        pass
    
    def toString(self):
        pass


class ItfGeoIntegerArray(object):
    pass


class ItfGeoFloat2(ItfGeoData):
    def _initItfGeoFloat2(self, *args, **kwargs):
        if args:
            self._raw = args[0]
        else:
            self._raw = (.0, .0)


class ItfGeoFloat2Array(ItfGeoData):
    pass


class ItfGeoFloat3(ItfGeoData):
    def _initItfGeoFloat3(self, *args, **kwargs):
        if args:
            self._raw = args[0]
        else:
            self._raw = (.0, .0, .0)


class ItfGeoFloat3Array(ItfGeoData):
    pass


class ItfGeoFaceVertices(ItfGeoData):
    CLS_geo__face_vertices__face_vertex_counts = None
    CLS_geo__face_vertices__vertex_indices = None

    def _initItfGeoFaceVertices(self, *args, **kwargs):
        vertexCountsArgs, vertexIndicesArgs = args
        self._setVertexCountsCreate(vertexCountsArgs, **kwargs)
        self._setVertexIndices(vertexIndicesArgs, **kwargs)

    @property
    def vertexCounts(self):
        """
        :return: instance(VertexCounts)
        """
        return self._vertexCountsIst

    def _setVertexCountsCreate(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, self.CLS_geo__face_vertices__face_vertex_counts):
            self._vertexCountsIst = _
        elif isinstance(_, (tuple, list)):
            self._vertexCountsIst = self.CLS_geo__face_vertices__face_vertex_counts(_)
        raise TypeError()

    @vertexCounts.setter
    def vertexCounts(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return: None
        """
        self._setVertexCountsCreate(*args, **kwargs)

    @property
    def vertexIndices(self):
        return self._vertexIndicesIst

    def _setVertexIndices(self, *args, **kwargs):
        _ = args[0]
        if isinstance(_, self.CLS_geo__face_vertices__vertex_indices):
            self._vertexIndicesIst = _
        elif isinstance(_, (tuple, list)):
            self._vertexIndicesIst = self.CLS_geo__face_vertices__vertex_indices(_)
        raise TypeError()
    
    @vertexIndices.setter
    def vertexIndices(self, *args, **kwargs):
        self._setVertexIndices(*args, **kwargs)


class ItfGeoFaceVertexCounts(ItfGeoData):
    def _initItfGeoFaceVertexCounts(self, *args, **kwargs):
        if args:
            self._raw = args[0]
        else:
            self._raw = []
            
            
class ItfGeoPoints(ItfGeoData):
    def _initItfGeoPoints(self, *args, **kwargs):
        pass


class ItfGeoFaceVertexIndices(ItfGeoData):
    pass


class ItfGeoMapUvs(ItfGeoData):
    pass


# prim *************************************************************************************************************** #
class ItfGeoPrim(object):
    pass


class ItfGeo(object):
    pass
