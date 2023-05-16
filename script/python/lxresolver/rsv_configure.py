# coding:utf-8
import os

import glob


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


class EntityCategories(object):
    Project = 'project'
    ResourceGroup = 'resource_group'
    Resource = 'resource'
    Step = 'step'
    Task = 'task'


class EntityTypes(object):
    Project = 'project'
    Role = 'role'
    Asset = 'asset'
    Sequence = 'sequence'
    Shot = 'shot'
    #
    Step = 'step'
    Task = 'task'
    #
    Version = 'version'
    #
    Projects = [
        Project
    ]
    #
    ResourceGroups = [
        Role,
        Sequence
    ]
    #
    Resources = [
        Asset,
        Shot
    ]
    #
    All = [
        Asset,
        Sequence,
        Shot
    ]


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
        Root,
        Project,
        Workspace, WorkspaceKey,
        Branch,
        Role, Sequence,
        Asset, Shot,
        Step, Task,
        Version,
        TaskExtra, VersionExtra,
        User, Artist,
    ]


class VariantKeysExtend(object):
    Keyword = 'keyword'
    Pattern = 'pattern'
    Result = 'result'
    #
    Category = 'category'
    Type = 'type'
    Path = 'path'
    #
    Update = 'update'
    #
    All = [
        Keyword, Pattern, Result,
        Category, Type, Path,
        Update
    ]


class VariantsKeys(object):
    Schemes = 'schemes'
    Roles = 'roles'
    Workspaces = 'workspaces'
    #
    ProjectSteps = 'project_steps'
    #
    AssetSteps = 'asset_steps'
    #
    SequenceSteps = 'sequence_steps'
    ShotSteps = 'shot_steps'
    #
    ProjectTasks = 'project_tasks'
    AssetTasks = 'asset_tasks'
    SequenceTasks = 'sequence_tasks'
    ShotTasks = 'shot_tasks'
    #
    All = [
        Schemes,
        Roles,
        Workspaces,
        ProjectSteps, AssetSteps, SequenceSteps, ShotSteps,
        ProjectTasks, AssetTasks, SequenceTasks, ShotTasks
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

