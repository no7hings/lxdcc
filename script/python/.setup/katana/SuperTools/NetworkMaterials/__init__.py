# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: SuperTools/NetworkMaterials/__init__.py
# Compiled at: 2021-06-28 21:25:16
"""
Copyright (c) 2019 The Foundry Visionmongers Ltd. All Rights Reserved.
"""
try:
    import v1 as NetworkMaterials
except ImportError:
    NetworkMaterialCreate = None
    NetworkMaterialEdit = None

try:
    from v1.NetworkMaterialCreateNode import NetworkMaterialCreateNode
except ImportError:
    NetworkMaterialCreateNode = None

try:
    from v1.NetworkMaterialEditNode import NetworkMaterialEditNode
except ImportError:
    NetworkMaterialEditNode = None

PluginRegistry = []
if NetworkMaterialCreateNode:
    PluginRegistry.append(('SuperTool',
     2,
     'NetworkMaterialCreate',
     (
      NetworkMaterialCreateNode,
      NetworkMaterials.GetNetworkMaterialCreateEditor)))
if NetworkMaterialEditNode:
    PluginRegistry.append(('SuperTool',
     2,
     'NetworkMaterialEdit',
     (
      NetworkMaterialEditNode,
      NetworkMaterials.GetNetworkMaterialEditEditor)))