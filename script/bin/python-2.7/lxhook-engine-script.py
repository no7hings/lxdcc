# coding:utf-8
import sys


def main(argv):
    import lxsession.commands as ssn_commands; ssn_commands.set_option_hook_execute(argv[1])


if __name__ == '__main__':
    main(sys.argv)



