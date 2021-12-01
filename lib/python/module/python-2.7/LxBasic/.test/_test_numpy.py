# coding:utf-8
import numpy

a = numpy.array([0.0, 1.0, 2.0])

print a

a.tofile('/data/f/h5_test/test_1.h5')

b = numpy.fromfile('/data/f/h5_test/test_1.h5', dtype=numpy.float)

print list(b)
