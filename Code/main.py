import robot
import sys
from time import sleep


def run_auto(r):
    # Automatic mode TODO
    return


def run_manual(r):
    """
    run_manual(r) - Gives user control of robot until they quit. Control with WASD keys
    :param r: a robot class
    :return: nothing
    """
    print("   ___________________________________")
    print("  /                                  /")
    print(" /           MANUAL MODE            /")
    print("/__________________________________/")

    sleep(1)

    c = ""

    while c.lower() != "q":
        c = input().lower()
        # TODO


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
        print('usage: main.py [-a or --auto] or [-m --manual]')
        quit()

    r = robot.Robot()

    if auto:
        run_auto(r)
    else:
        run_manual(r)
