# coding:utf-8
# noinspection PyUnresolvedReferences
from maya import cmds

import fnmatch

from lxbasic import bsc_core

from lxutil import utl_core

from lxmaya import ma_configure


class Utils(object):
    @classmethod
    def get_all_group_paths(cls):
        return [
            i
            for i in cmds.ls(exactType='transform', long=1) or []
            if i and cmds.listRelatives(i, children=1, shapes=1, noIntermediate=0) is None
        ]
    @classmethod
    def get_all_shape_paths(cls):
        return [
            i
            for i in cmds.ls(shapes=1, long=1, noIntermediate=1) or []
            if i and cmds.listRelatives(i, children=1, shapes=1, noIntermediate=0) is None
        ]
    @classmethod
    def get_all_namespace_paths(cls):
        lis = []
        except_list = ['UI', 'shared']
        _ = cmds.namespaceInfo(recurse=1, listOnlyNamespaces=1, fullName=1)
        if _:
            _.reverse()
            for namespace in _:
                if namespace not in except_list:
                    lis.append(namespace)
        return lis
    @classmethod
    def get_all_naming_overlapped_paths(cls, reference=True):
        _ = [x for x in cmds.ls() if '|' in x]
        if reference is True:
            return _
        return [i for i in _ if not cmds.referenceQuery(i, isNodeReferenced=1)]
    @classmethod
    def get_name_with_namespace_clear(cls, name):
        return bsc_core.DccPathDagMtd.get_dag_name_with_namespace_clear(
            name, ma_configure.Util.NAMESPACE_PATHSEP
        )
    @classmethod
    def get_path_with_namespace_clear(cls, path):
        return bsc_core.DccPathDagMtd.get_dag_path_with_namespace_clear(
            path, ma_configure.Util.OBJ_PATHSEP, ma_configure.Util.NAMESPACE_PATHSEP
        )


class UtlNode(object):
    @classmethod
    def get_all_history_paths(cls, path):
        except_types = ['shadingEngine', 'groupId', 'set']
        lis = []
        for j in cmds.listHistory(path, pruneDagObjects=1) or []:
            if cmds.nodeType(j) not in except_types:
                lis.append(j)
        return lis


class UtlNodeReference(object):
    @classmethod
    def get(cls, node_type):
        dic = {}
        PORT_PATHSEP = ma_configure.Util.PORT_PATHSEP
        directory_paths = cmds.filePathEditor(query=True, listDirectories="") or []
        for directory_path in directory_paths:
            raw = cmds.filePathEditor(query=True, listFiles=directory_path, withAttribute=True, byType=node_type) or []
            for i in range(len(raw)/2):
                file_name = raw[i*2]
                attribute_path = raw[i*2+1]
                _ = attribute_path.split(PORT_PATHSEP)
                file_path = '{}/{}'.format(directory_path, file_name)
                node_path = cmds.ls(_[0], long=1)[0]
                port_path = PORT_PATHSEP.join(_[1:])
                dic.setdefault(node_path, []).append((port_path, file_path))
        return dic


class UtlScriptJob(object):
    # dbTraceChanged
    # resourceLimitStateChange
    # linearUnitChanged
    # timeUnitChanged
    # angularUnitChanged
    # Undo
    # undoSupressed
    # Redo
    # customEvaluatorChanged
    # serialExecutorFallback
    # timeChanged
    # currentContainerChange
    # quitApplication
    # idleHigh
    # idle
    # idleVeryLow
    # RecentCommandChanged
    # ToolChanged
    # PostToolChanged
    # ToolDirtyChanged
    # ToolSettingsChanged
    # DisplayRGBColorChanged
    # animLayerRebuild
    # animLayerRefresh
    # animLayerAnimationChanged
    # animLayerLockChanged
    # animLayerBaseLockChanged
    # animLayerGhostChanged
    # cteEventKeyingTargetForClipChanged
    # cteEventKeyingTargetForLayerChanged
    # cteEventKeyingTargetForInvalidChanged
    # teClipAdded
    # teClipModified
    # teClipRemoved
    # teCompositionAdded
    # teCompositionRemoved
    # teCompositionActiveChanged
    # teCompositionNameChanged
    # teMuteChanged
    # cameraChange
    # cameraDisplayAttributesChange
    # SelectionChanged
    # PreSelectionChangedTriggered
    # LiveListChanged
    # ActiveViewChanged
    # SelectModeChanged
    # SelectTypeChanged
    # SelectPreferenceChanged
    # DisplayPreferenceChanged
    # DagObjectCreated
    # transformLockChange
    # renderLayerManagerChange
    # renderLayerChange
    # displayLayerManagerChange
    # displayLayerAdded
    # displayLayerDeleted
    # displayLayerVisibilityChanged
    # displayLayerChange
    # renderPassChange
    # renderPassSetChange
    # renderPassSetMembershipChange
    # passContributionMapChange
    # DisplayColorChanged
    # lightLinkingChanged
    # lightLinkingChangedNonSG
    # UvTileProxyDirtyChangeTrigger
    # preferredRendererChanged
    # polyTopoSymmetryValidChanged
    # SceneSegmentChanged
    # PostSceneSegmentChanged
    # SequencerActiveShotChanged
    # ColorIndexChanged
    # deleteAll
    # NameChanged
    # symmetricModellingOptionsChanged
    # softSelectOptionsChanged
    # SetModified
    # xformConstraintOptionsChanged
    # metadataVisualStatusChanged
    # undoXformCmd
    # redoXformCmd
    # freezeOptionsChanged
    # linearToleranceChanged
    # angularToleranceChanged
    # nurbsToPolygonsPrefsChanged
    # nurbsCurveRebuildPrefsChanged
    # constructionHistoryChanged
    # threadCountChanged
    # SceneSaved
    # NewSceneOpened
    # SceneOpened
    # SceneImported
    # PreFileNewOrOpened
    # PreFileNew
    # PreFileOpened
    # PostSceneRead
    # renderSetupAutoSave
    # workspaceChanged
    # PolyUVSetChanged
    # PolyUVSetDeleted
    # selectionConstraintsChanged
    # nurbsToSubdivPrefsChanged
    # startColorPerVertexTool
    # stopColorPerVertexTool
    # start3dPaintTool
    # stop3dPaintTool
    # DragRelease
    # ModelPanelSetFocus
    # modelEditorChanged
    # MenuModeChanged
    # gridDisplayChanged
    # interactionStyleChanged
    # axisAtOriginChanged
    # CurveRGBColorChanged
    # SelectPriorityChanged
    # snapModeChanged
    # texWindowEditorImageBaseColorChanged
    # texWindowEditorCheckerDensityChanged
    # texWindowEditorCheckerDisplayChanged
    # texWindowEditorDisplaySolidMapChanged
    # texWindowEditorShowup
    # texWindowEditorClose
    # profilerSelectionChanged
    # activeHandleChanged
    # ChannelBoxLabelSelected
    # colorMgtOCIORulesEnabledChanged
    # colorMgtUserPrefsChanged
    # RenderSetupSelectionChanged
    # colorMgtEnabledChanged
    # colorMgtConfigFileEnableChanged
    # colorMgtConfigFilePathChanged
    # colorMgtConfigChanged
    # colorMgtWorkingSpaceChanged
    # colorMgtPrefsViewTransformChanged
    # colorMgtPrefsReloaded
    # colorMgtOutputChanged
    # colorMgtPlayblastOutputChanged
    # colorMgtRefreshed
    # selectionPipelineChanged
    # currentSoundNodeChanged
    # graphEditorChanged
    # graphEditorParamCurveSelected
    # graphEditorOutlinerHighlightChanged
    # graphEditorOutlinerListChanged
    # glFrameTrigger
    # EditModeChanged
    # playbackRangeAboutToChange
    # playbackSpeedChanged
    # playbackModeChanged
    # playbackRangeSliderChanged
    # playbackByChanged
    # playbackRangeChanged
    # RenderViewCameraChanged
    # texScaleContextOptionsChanged
    # texRotateContextOptionsChanged
    # texMoveContextOptionsChanged
    # polyCutUVSteadyStrokeChanged
    # polyCutUVEventTexEditorCheckerDisplayChanged
    # polyCutUVShowTextureBordersChanged
    # polyCutUVShowUVShellColoringChanged
    # shapeEditorTreeviewSelectionChanged
    # poseEditorTreeviewSelectionChanged
    # sculptMeshCacheBlendShapeListChanged
    # sculptMeshCacheCloneSourceChanged
    # RebuildUIValues
    # cacheDestroyed
    # cachingPreferencesChanged
    # cachingSafeModeChanged
    # cachingEvaluationModeChanged
    # teTrackAdded
    # teTrackRemoved
    # teTrackNameChanged
    # teTrackModified
    # cteEventClipEditModeChanged
    # teEditorPrefsChanged
    @classmethod
    def get_all(cls):
        return cmds.scriptJob(listJobs=1) or []
    @classmethod
    def set_delete(cls, pattern):
        _ = fnmatch.filter(cls.get_all(), pattern)
        if _:
            for i in _:
                index = i.split(': ')[0]
                cmds.scriptJob(kill=int(index), force=1)
                bsc_core.LogMtd.trace_method_result(
                    'job-script kill',
                    'job-script="{}"'.format(i.lstrip().rstrip())
                )


class Modifier(object):
    @staticmethod
    def undo_run(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                from lxbasic import bsc_core
                bsc_core.ExceptionMtd.set_print()
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)

        return sub_fnc_
    @staticmethod
    def undo_debug_run(fnc):
        def sub_fnc_(*args, **kwargs):
            cmds.undoInfo(openChunk=1, undoName=fnc.__name__)
            # noinspection PyBroadException
            try:
                _method = fnc(*args, **kwargs)
                return _method
            except Exception:
                from lxutil import utl_core
                is_ui_mode = not cmds.about(batch=1)
                utl_core.ExceptionCatcher.set_create(use_window=is_ui_mode)
                raise
            #
            finally:
                cmds.undoInfo(closeChunk=1, undoName=fnc.__name__)

        return sub_fnc_


class CallbackOpt(object):
    def __init__(self, function, callback_type):
        self._function = function
        self._callback_type = callback_type

    def register(self):
        _index = cmds.scriptJob(
            parent='modelPanel4', event=[self._callback_type, self._function]
        )
        bsc_core.LogMtd.trace_method_result(
            'callback',
            'add as "{}" at "{}"'.format(self._callback_type, _index)
        )

    def deregister(self):
        pass

