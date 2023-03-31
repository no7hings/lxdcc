# coding:utf-8
import os

import glob


class Root(object):
    MAIN = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    DATA = '{}/.data'.format(MAIN)


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_PATH = '{}/.data'.format(ROOT)
    #
    GEOMETRY_USD_CONFIGURE_PATH = '{}/set-usd-configure.yml'.format(DATA_PATH)
    #
    ASSET_CONFIGURE_PATH = '{}/asset-configure.yml'.format(DATA_PATH)


class Platforms(object):
    Windows = 'windows'
    Linux = 'linux'
    All = [
        Windows,
        Linux
    ]


class Applications(object):
    Maya = 'maya'
    Houdini = 'houdini'
    Katana = 'katana'
    Clarisse = 'clarisse'
    Nuke = 'nuke'
    Python = 'python'
    Lynxi = 'lynxi'
    #
    DCCS = [
        Maya,
        Houdini,
        Katana,
        Clarisse,
        Nuke
    ]
    All = [
        Maya,
        Houdini,
        Katana,
        Clarisse,
        Nuke,
        Python,
        Lynxi
    ]
    #
    PATHSEP_DICT = {
        Maya: '|',
        Houdini: '/',
        Katana: '/',
        Clarisse: '/',
        Nuke: '/'
    }
    @classmethod
    def get_pathsep(cls, application):
        return cls.PATHSEP_DICT[application]


class VariantCategories(object):
    Project = 'project'
    Tag = 'tag'
    Resource = 'resource'
    Step = 'step'
    Task = 'task'


class VariantTypes(object):
    Root = 'root'
    #
    Project = 'project'
    Workspace = 'workspace'
    WorkspaceKey = 'workspace_key'
    #
    Branch = 'branch'
    #
    Role = 'role'
    Asset = 'asset'
    #
    Sequence = 'sequence'
    Shot = 'shot'
    #
    Step = 'step'
    Task = 'task'
    Version = 'version'
    #
    TaskExtra = 'task_extra'
    VersionExtra = 'version_extra'
    #
    User = 'user'
    Artist = 'artist'
    #
    Inners = [
        Branch
    ]
    #
    Trunks = [
        Project,
        Role, Sequence,
        Asset, Shot,
    ]
    #
    Branches = [
        Step, Task,
        Version,
    ]
    #
    Mains = Trunks + Branches
    #
    VariableTypes = [
        Workspace,
        WorkspaceKey
    ]
    #
    Extends = [
        User, Artist,
    ]
    #
    All = [
        Root, Project, Workspace, WorkspaceKey,
        Branch,
        Role, Sequence,
        Asset, Shot,
        Step, Task,
        Version,
        TaskExtra, VersionExtra,
        User, Artist,
    ]


class VariantsKeys(object):
    Schemes = 'schemes'
    Roles = 'roles'
    Workspaces = 'workspaces'
    #
    AssetSteps = 'asset_steps'
    SequenceSteps = 'sequence_steps'
    ShotSteps = 'shot_steps'
    #
    AssetTasks = 'asset_tasks'
    SequenceTasks = 'sequence_tasks'
    ShotTasks = 'shot_tasks'
    #
    All = [
        Schemes,
        Roles,
        Workspaces,
        AssetSteps, SequenceSteps, ShotSteps,
        AssetTasks, SequenceTasks, ShotTasks
    ]


class Branches(object):
    Asset = 'asset'
    Sequence = 'sequence'
    Shot = 'shot'
    #
    Mains = [
        Asset,
        Shot
    ]
    #
    All = [
        Asset,
        Sequence,
        Shot
    ]


class WorkspaceKeys(object):
    Source = 'source'
    User = 'user'
    Release = 'release'
    Temporary = 'temporary'
    Mains = [
        Source,
        Release
    ]
    All = [
        Source,
        User,
        Release,
        Temporary
    ]


class WorkspaceMatchKeys(object):
    Sources = ['source', 'work']
    Users = ['user']
    Releases = ['release', 'publish']
    Temporaries = ['temporary', 'output']


class Version(object):
    LATEST = 'latest'
    NEW = 'new'
    ALL = 'all'

