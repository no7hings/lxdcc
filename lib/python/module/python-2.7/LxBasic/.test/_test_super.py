# coding:utf-8


class A(object):
    def __init__(self, *args):
        print args, "A"


class B(A):
    def __init__(self, *args):
        super(B, self).__init__(*args)
        print args, "B"


class C(B):
    def __init__(self, *args):
        super(C, self).__init__(*args)
        print args, "C"


C('TEST')
