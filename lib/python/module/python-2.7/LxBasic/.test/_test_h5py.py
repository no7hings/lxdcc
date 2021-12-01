# coding:utf-8
from LxBasic import bscModifiers
import os

import json

import numpy

import h5py

f1 = '/data/f/h5_test/test.h5'
f2 = '/data/f/h5_test/test.json'
f3 = '/data/f/h5_test/test_1.h5'


@bscModifiers.getFncCostTime
def set_json_read(filepath):
    with open(filepath) as j:
        return json.load(j)


def set_h5_write(filepath, data, dataset=None):
    dirname = os.path.dirname(filepath)

    if os.path.isdir(dirname) is False:
        os.makedirs(dirname)

    with h5py.File(filepath, 'w') as h:
        if dataset is None:
            dataset = 'dataset_1'

        h.create_dataset(
            dataset, data=data,
            compression="gzip",
            compression_opts=9,
        )


@bscModifiers.getFncCostTime
def set_h5_read(filepath, dataset=None):
    with h5py.File(filepath, 'r') as h:
        if dataset is None:
            dataset = h.keys()[0]
        data = h[dataset]
        return list(numpy.array(data))


@bscModifiers.getFncCostTime
def set_numpy_write(filepath, data):
    a = numpy.array(data)
    a.tofile(filepath)

@bscModifiers.getFncCostTime
def set_numpy_read(filepath):
    return list(numpy.fromfile(filepath, dtype=numpy.float))


d2 = set_json_read(f2)
d3 = set_numpy_read(f3)

# set_numpy_write(f3, set_json_read(f2))
