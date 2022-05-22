import subprocess
import threading, queue

import sys
import time
from pycmm.common.sys.env import system_info

# >>> p = subprocess.Popen(['grep','f'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
# >>> p.stdin.write(b'one\ntwo\nthree\nfour\nfive\nsix\n') #expects a bytes type object
# >>> p.communicate()[0]
# 'four\nfive\n'
# >>> p.stdin.close()




#     @classmethod
#     def shell_linux(cls, command):
#         encoding_format = 'utf-8'
#         cmd = ';'.join(command)
#         print("CMD : {}".format(cmd))
#         # On POSIX with shell=True, the shell defaults to /bin/sh.
#         process = subprocess.Popen('/bin/bash', stdin=sp.PIPE, stdout=sp.PIPE)
#         p.stdin.write(cmd.encode(encoding_format))
#         out, err = p.communicate()
#         p.stdin.close()
#         if out != None:
#             out = out.decode(encoding_format).strip()
#         if err != None:
#             err = err.decode(encoding_format).strip()
#         return out, err

# # For Windows
# # When typing 'chcp' command, Windows prompt print 'cp949'
# # On Windows with shell=True, the COMSPEC environment variable
# # specifies the default shell.
# # Windows에서 "shell=True"를 포함시켜주어야 에러 나지 않는 경우 있음.
# # stderr로 output이 나오는 경우, "stderr=sp.PIPE" 넣어주어야 함.
#     @classmethod
#     def shell_win32(cls, command):
#         #p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
#         #p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
#         p = sp.Popen(cmd, shell=True)
#         out, err = p.communicate()
#         if out:
#             #out = out.decode("cp949")
#             out = out.decode(sys.stdout.encoding, errors='ignore')
#             pass
#         if err:
#             #err = err.decode("cp949")
#             err = err.decode(sys.stdout.encoding, errors='ignore')
#             pass

class Shell:
    process = None
    output_thread = None
    def __init__(self):
        self.create()
    @classmethod
    def create(cls):
        system = system_info.system
        if system == "Linux":
            cls.process = subprocess.Popen(
                                '/bin/bash',
                                stdin =subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                bufsize=0
                                )
            cls.output_thread = threading.Thread(target=cls.get_out, daemon=True)

        if cls.process == None:
            print("wht not?")
        cls.output_thread.start()
    @classmethod
    def close(cls):
        cls.process.stdin.close()
    @classmethod
    def get_out(cls):
        while True:
            if cls.process.stdout != None:
                for line in cls.process.stdout:
                    print(line.strip())
            time.sleep(0.1)
            


    @classmethod
    def shell(cls, command):
        if cls.process == None:
            print("asdfasfdasfd")
        enc_fmt = 'utf-8'


        # cmd = ';'.join(command)
        # print("CMD : {}".format(cmd))
        # cls.process.stdin.write(cmd.encode(encoding_format))
        cls.process.stdin.write("{}\n".format(command))
        cls.process.stdin.flush()
        # out = repr(cls.process.stdout.readline())
        # cls.process.stdin.close()
        # cls.process.wait()
        # return out


def test1():
    process = subprocess.Popen(['ping', '-c 4', 'python.org'],
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break


if __name__ == "__main__":
    sh = Shell()
    sh.shell("echo Test")
    sh.shell("ls -l")
    time.sleep(2)
    sh.close()


        # if system == "WINDOWS":
        #     out, err = shell_win32(args)
        #     return out, err
        #     #return shell_win32(args)
        # elif system == "LINUX":
        #     out, err = shell_linux(args)
        #     return out, err
        #     #return shell_linux(args)
        # else:
        #     exit("> ERROR, not in WINDOWS or LINUX")
