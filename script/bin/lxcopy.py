# coding:utf-8
from __future__ import print_function

import sys

import getopt

import subprocess

import multiprocessing

import os

argv = sys.argv


def set_usage_print():
    print (
        u'***** lxdcc *****\n'
        u'\n'
        #
        u'-h or --help: show help-info\n'
        #
        u'-c or --configure: configure-file\n'
    )


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:], 'hc',
            ['help', 'configure=']
        )
        configure = [None] * 7
        for key, value in opts:
            if key in ('-h', '--help'):
                set_usage_print()
                sys.exit()
            elif key in ('-c', '--configure'):
                configure = value
    except:
        pass

