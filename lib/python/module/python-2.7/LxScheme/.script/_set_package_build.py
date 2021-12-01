# coding:utf-8

if __name__ == '__main__':
    from LxScheme.shmObjects import _shmObjBuilder

    # wb = shmBuilder.WindowsResourceBuilder()
    #
    # for i in wb.packages():
    #     print i.name
    #     print i.system

    lb = _shmObjBuilder.LinuxResourceBuilder()

    for i in lb.packages():
        print i.name
        i.createServerConfigFile()
        i.createDevelopSourceDirectories()
        #
        op = i.operateAt(i.version.active)
        print op.develop_source_directory
