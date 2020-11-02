import os
import subprocess
import shlex
import time

class CheckingEnv():
    """
        this class for helper checking enviroment requirement before running
    """
    def __init__(self):
        #nothings just init
        print('init')

    def executioner(self, command, component, do_exit=0):
        try:
            count = 0
            while True:
                res = subprocess.call(shlex.split(command))
                if res != 0:
                    count = count + 1
                    CheckingEnv.stdOut(component + ' failed, trying again, try number: ' + str(count), 0)
                    if count == 3:
                        CheckingEnv.stdOut(component + ' failed.', do_exit)
                        return False
                else:
                    CheckingEnv.stdOut(component + ' successful.', 0)
                    break
            return True
        except:
            return 0
    @staticmethod
    def stdOut(message, do_exit=0):
        print("\n\n")
        print(("[" + time.strftime(
            "%m.%d.%Y_%H-%M-%S") + "] #########################################################################\n"))
        print(("[" + time.strftime("%m.%d.%Y_%H-%M-%S") + "] " + message + "\n"))
        print(("[" + time.strftime(
            "%m.%d.%Y_%H-%M-%S") + "] #########################################################################\n"))

        if do_exit:
            os._exit(0)