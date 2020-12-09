import robot
import sys
from time import sleep
import sensors


def run_auto(r, s, light_0, obstacles=0):
    input('Am I in the right spot to start? Press enter to continue...')

    # Automatic mode

    if obstacles == 3:
        print('Heck yeah! I did it!!! Aren\'t you proud of me??? :)')
        return

    # Check if wall
    if s.range < 100 and s.read_lux() >= light_0 - 5:
        r.walk(5)
        r.climb()
    elif s.read_lux() < light_0 / 2:
        r.turning(12)
        r.walk(5)
    else:
        r.hulk()

    run_auto(r, s, light_0, obstacles+1)

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
          '\t[Sh]ort range\n'
          '\t[L]ight level\n'
          '\t[A]djust gain for light level\n'
          '\t[P]icture\n'
          '\t[Q]uit\n')
    c = input().lower()

    if c in ['w', 't', 'c', 'r', 'e', 's', 'l', 'p', 'q', 'm', 'a', 'sh']:
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
            steps = int(input('\t\tHow many steps?'))
            r.walk(steps)
        elif c == 't':
            r.turning(12)
        elif c == 'm':
            steps = int(input('\t\tHow many steps?'))
            r.turning(steps)
        elif c == 'c':
            print('not implemented... sorry.... YET!')
        elif c == 'r':
            r.reset()
        elif c == 'e':
            r.extend()
        elif c == 's':
            print(('Range {}mm'.format(s.range).ljust(20, '-')).rjust(30,'-'))
        elif c == 'l':
            print(('Light {} lux'.format(s.read_lux()).ljust(21, '-')).rjust(30,'-'))
        elif c == 'p':
            s.send_photo()
        elif c == 'ph':
            s.send_photo(sendto='Matthew.Woodward@tufts.edu')
        elif c == 'q':
            return
        elif c == 'a':
            gain = int(input('What gain level would you like? 1, 1.25, 1.67, 2.5, 5, 10, 20, 40?'))
            print(('Light {} lux'.format(s.read_lux(gain)).ljust(21, '-')).rjust(30, '-'))
        elif c == 'sh':
            print(('Range {}mm'.format(s.range_short).ljust(20, '-')).rjust(30, '-'))
        else:
            print('This should not happen. Please contact MAX and tell him that \"' + c + '\" messed up the cmd seq.')
            exit(-1)


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

    light_0 = s.read_lux()

    if auto:
        run_auto(r, s, light_0)
    else:
        run_manual(r, s)
