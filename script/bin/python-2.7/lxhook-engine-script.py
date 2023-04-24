# coding:utf-8
import sys


def main(argv):
    # run error in katana --script, no "__file__" argument
    # sys.stdout.write('execute lxhook-engine-script from: "{}"\n'.format(__file__))
    import lxsession.commands as ssn_commands; ssn_commands.set_option_hook_execute(argv[1])


if __name__ == '__main__':
    main(sys.argv)



