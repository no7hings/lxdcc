# coding:utf-8
from lxresolver import rsv_configure

import lxutil.objects as utl_objects

import lxresolver.commands as rsv_commands


class AbsEntities(object):
    CONFIGURE_FILE_PATH = rsv_configure.Data.ENTITIES_CONFIGURE_PATH
    def __init__(self, project_properties):
        self._project_properties = project_properties
        self._file_configure = utl_objects.Configure(value=self.CONFIGURE_FILE_PATH)
        self._resolver = rsv_commands.get_resolver()

    def _get_result_(self, key, sub_key, **kwargs):
        project_properties = self._project_properties
        resolver = self._resolver
        #
        v = self._file_configure.get('{}.{}'.format(key, sub_key))
        workspace = v['workspace']
        branch = v['branch']
        #
        platform = project_properties.get('platform')
        project = project_properties.get('project')
        #
        if branch == 'asset':
            _kwargs = dict(
                platform=platform,
                project=project,
                workspace=workspace,
                branch=branch,
                role='*'
            )
        elif branch == 'shot':
            _kwargs = dict(
                platform=platform,
                project=project,
                workspace=workspace,
                branch=branch,
                sequence='*'
            )
        else:
            raise TypeError()
        #
        for k, v in kwargs.items():
            if k in _kwargs:
                _kwargs[k] = v
        #
        rsv_entities = resolver.get_rsv_entities(
            **_kwargs
        )
        return rsv_entities


class RsvAssetsOpt(AbsEntities):
    KEY = 'entities.asset'
    def __init__(self, project_properties):
        super(RsvAssetsOpt, self).__init__(project_properties)

    def get_entities(self, **kwargs):
        sub_key = 'names'
        return self._get_result_(self.KEY, sub_key, **kwargs)

    def get_names(self, **kwargs):
        return [i.name for i in self.get_entities(**kwargs)]
