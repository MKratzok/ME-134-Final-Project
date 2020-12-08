import robot
import sys
from time import sleep
import sensors


def run_auto(r):
    # Automatic mode TODO
    return


def menu():
    print('Command Options:\n'
          '\t[W]alk\n'
          '\t[T]urn 12 steps\n'
          '\t[M]anual turn\n'
          '\t[C]limb\n'
          '\t[R]eset\n'
          '\t[E]xtend\n'
          '\t[S]ense range\n'
          '\t[L]ight level\n'
          '\t[P]icture\n'
          '\t[Q]uit\n')
    c = input().lower()

    if c in ['w', 't', 'c', 'r', 'e', 's', 'l', 'p', 'q', 'm']:
        return c
    else:
        print('Command not found.')
        return menu()


def run_manual(r, s):
    """
    run_manual(r) - Gives user control of robot until they quit. Control with WASD keys
    :param r: a robot class
    :return: nothing
    """
    print("   ___________________________________")
    print("  /                                  /")
    print(" /           MANUAL MODE            /")
    print("/__________________________________/\n\n")

    c = ''

    while c != "q":
        c = menu()

        if c == 'w':
            steps = input('\t\tHow many steps?')
            r.walk(steps)
        elif c == 't':
            r.turning(12)
        elif c == 'm':
            steps = input('\t\tHow many steps?')
            r.turning(steps)
        elif c == 'r':
            r.reset()
        elif c == 'e':
            r.extend()
        elif c == 's':
            print(('Range {}mm'.format(s.range).ljust(20, '-')).rjust(30,'-'))
        elif c == 'l':
            print(('Light {} lux'.format(11).ljust(21, '-')).rjust(30,'-'))
        elif c == 'p':
            s.take_photo()
        elif c == 'q':
            return
        else:
            print('This should not happen. Please contact MAX and tell him that \"' + c + '\" messed up the cmd seq.')
            exit(-69)


if __name__ == "__main__":
    """ To select mode, run program with (default is manual): 
    >>> python3 main.py [-a or --auto] or [-m --manual]
    """
    if len(sys.argv) is 1:
        auto = False
    elif sys.argv[1] in ['--auto', '-a']:
        auto = True
    elif sys.argv[1] in ['--manual', '-m']:
        auto = False
    else:
        auto = False
        print('usage: main.py [-a or --auto] or [-m --manual]')
        quit()

    r = robot.Robot()
    s = sensors.Sensors()

    if auto:
        run_auto(r)
    else:
        run_manual(r, s)
