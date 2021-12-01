# coding:utf-8
from __future__ import print_function

import sys

import getopt

import os

import collections

argv = sys.argv


def usage():
    print (
        '***** lxmethod *****\n'
        '\n'
        #
        '-h or --help: show help\n'
        #
        '-m or --method: <method-name>\n'
        '-o or --option: <option>\n'
    )


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hp:m:o:',
            ['help', 'method=', 'option=']
        )
        method, option = [None] * 2
        for key, value in opts:
            if key in ('-h', '--help'):
                usage()
                sys.exit()
            elif key in ('-m', '--method'):
                method = value
            elif key in ('-o', '--option'):
                option = value
        #
        set_run(method, option)
    #
    except getopt.GetoptError:
        print('arguments error')


def set_run(method, option):
    if method == 'texture-tx-create':
        set_texture_tx_create(option)


def set_texture_tx_create(option):
    pass


if __name__ == '__main__':
    main()
