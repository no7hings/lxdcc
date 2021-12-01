# coding:utf-8
from lxutil import utl_core
import urllib


@utl_core._print_time_
def test():
    for i in ['http://192.168.18.100:2526/resolver?file=asset-maya-ma&project=shl&workspace=publish&asset=nn_gongshifu&step=mod&task=modeling&version=latest&platform=windows']*1000:
        print urllib.urlopen(i).read()


if __name__ == '__main__':
    test()
