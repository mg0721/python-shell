import sys
import platform
import time
import subprocess
from threading import Thread
from queue import Queue
from typing import List, Dict
from enum import Enum

class OS(Enum):
    LINUX = 1
    WINDOWS = 2
    ETC = 3

class Shell():
    __os_name = None
    __shell = None
    __command_queue = None
    __output_queue = None

    def __init__(self):
        self.__shell = self.__create_subprocess(os=self.__check_system())
        self.__out_queue = Queue()
        self.process = [
            Thread(
                target=self.__monitor_out,
                args=(self.__shell, self.__out_queue, )
            )
        ]
        self.__start(process=self.process)

    def __check_system(self):
        return OS.LINUX if platform.system() == "Linux" else \
                OS.WINDOWS if platform.system() == "Windows" else OS.ETC

    def __create_subprocess(self, os):
        if os == OS.LINUX:
            return subprocess.Popen(
                # ['/bin/bash', '-c', 'sudo apt install baobab'],
                '/bin/bash',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True, # Text stream
                restore_signals=True,
                bufsize=1 # For realtime output
            )
        else:
            return None

    def __monitor_out(self, shell, out_queue):
        while shell.poll() == None:
            out = shell.stdout.readline()
            sys.stdout.write(out)
            out_queue.put(out)

    def write_input(self, command):
        self.write(command)
        # TODO: Not smart
        time.sleep(1)

    def write(self, command):
        self.__shell.stdin.write("{};\n".format(command))
        self.__shell.stdin.flush()
        print("@@@@@@@@@@@@@@@@@@@@@@ command = {}".format(command))

    @staticmethod
    def __start(process: List):
        for p in process:
            p.start()

    def join(self):
        while self.__shell.returncode == None:
            sh.write("exit")
            time.sleep(1)
        self.__shell.terminate()

if __name__ == "__main__":
    sh = Shell()
    sh.write("cat ./test/file")
    sh.write("sudo apt install baobab")
    sh.write_input("Y")
    sh.join()