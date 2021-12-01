# coding:utf-8
from __future__ import print_function

import sys

import getopt

argv = sys.argv


def usage():
    print (
        '***** lxhash *****\n'
        '\n'
        #
        '-h or --help: show help\n'
        #
        '-d or --data: data\n'
        '-o or --output: output\n'
        '***** lxhash *****\n'
    )


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:], 'hd:o:',
            ['help', 'data=', 'output=']
        )
        data, output = [None] * 2
        print("AAA")
        for key, value in opts:
            if key in ('-h', '--help'):
                usage()
                sys.exit()
            elif key in ('-d', '--data'):
                data = value
            elif key in ('-o', '--output'):
                output = value
        #
        set_hash_write(data, output)
    #
    except getopt.GetoptError:
        print('argv error')


def set_hash_write(data, output):
    pass


if __name__ == '__main__':
    main()
