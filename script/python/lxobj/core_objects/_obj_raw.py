# coding:utf-8
from .. import obj_abstract


class Constant(obj_abstract.AbsValue):
    def __init__(self, type_, raw):
        super(Constant, self).__init__(type_, raw)


class Color(obj_abstract.AbsValue):
    def __init__(self, type_, raw):
        super(Color, self).__init__(type_, raw)


class Vector(obj_abstract.AbsValue):
    def __init__(self, type_, raw):
        super(Vector, self).__init__(type_, raw)


class Matrix(obj_abstract.AbsValue):
    def __init__(self, type_, raw):
        super(Matrix, self).__init__(type_, raw)


class Array(obj_abstract.AbsValue):
    def __init__(self, type_, raw):
        super(Array, self).__init__(type_, raw)
