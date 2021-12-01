# coding:utf-8

if __name__ == '__main__':
    import os
    from LxScheme.shmObjects import _shmObjBuilder

    os.environ[u'LYNXI_ENABLE_USEDEF'] = 'TRUE'

    p = _shmObjBuilder.WindowsResourceBuilder()

    for i in p.modules():
        if i.name in ['LxMaBasic']:
            op = i.operateAt('0.0.0')
            i.createServerConfigFile()
            i.createDevelopSourceDirectories()
