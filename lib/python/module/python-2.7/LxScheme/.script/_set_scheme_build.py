# coding:utf-8

if __name__ == '__main__':
    from LxScheme.shmObjects import _shmObjBuilder

    # p = _shmObjBuilder.WindowsResourceBuilder()
    # for i in p.schemes():
    #     if i.name in ['maya_default']:
    #         i.createWorkspaceSourceDirectory()
    #         i.createServerConfigFile()
    #         op = i.operateAt('0.0.0')
    #
    #         op.createDevelopSetupJsonFile()
    #         op.createDevelopSetupJsonFile()
    #         op.createWorkspaceSetupJsonFile()
    #         op.pushWorkspaceSourceToDevelop()

    p = _shmObjBuilder.LinuxResourceBuilder()
    for i in p.schemes():
        if i.name in ['maya_default']:
            i.createWorkspaceSourceDirectory()
            i.createServerConfigFile()

            op = i.operateAt('0.0.0')

            op.createDevelopSetupJsonFile()
            op.createWorkspaceSetupJsonFile()
            op.pushWorkspaceSourceToDevelop()
