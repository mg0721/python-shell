import subprocess
from multiprocessing import Process, Queue
import threading, queue

import platform
import fcntl
import sys
import time
import os
import io



# https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
# https://stackoverflow.com/questions/33886406/how-to-avoid-the-deadlock-in-a-subprocess-without-using-communicate
# https://stackoverflow.com/questions/7206519/executing-bash-with-subprocess-popen
# https://stackoverflow.com/questions/8495794/python-popen-stdout-readline-hangs




class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)




class Shell:
    # _enc_fmt = 'utf-8'
    _process = None
    _thread_run = None
    _thread_out = None
    _queue_cmd = None
    _queue_out = None
    _empty = True
    _time_gap = 0.1
    stdout_buf = io.BytesIO()
    stderr_buf = io.BytesIO()
    def __init__(self):
        self._create()
    @classmethod
    def shell(cls, command):
        cls._queue_cmd.put(command)
    @classmethod
    def out(cls):
        cls.shell("exit")
        while (cls._process.poll() is None):
            time.sleep(cls._time_gap)
            pass
        # # result_list = []
        # while (cls._process.poll() is None) or (not cls._queue_out.empty()):
        #     # if cls._queue_out.empty():
        #         # print("empty")
        #         #
        #         # pass
        #     # else:
        #         # line = cls._queue_out.get()
        #         print("out:{}".format(line), end="")
        #         # result_list.append(line)
        #         # stdout_buf.write(line.encode())

        # print("cls._process.poll() : {}".format(cls._process.poll()))
        # print("return code : {}".format(cls._process.returncode))

        print("end of wait")
        def decode(file, lines):
            # from itertools import islice
            list_result = []
            for line in file.readlines():
                list_result.append(line.decode())
            return list_result

        cls.stdout_buf.seek(0)
        cls.stderr_buf.seek(0)

        return decode(cls.stdout_buf, 0), decode(cls.stderr_buf, 0)
    @classmethod
    def _run(cls, stdin, queue):
        while True:
            time.sleep(cls._time_gap)
            if queue.empty():
                continue
            else:
                command = queue.get()
                if cls._process == None:
                    exit("Error. No process exist.")
                try:
                    stdin.write("{};\n".format(command))
                    # stdin.write("/bin/bash -c '{}';\n".format(command))
                    stdin.flush()
                except Exception as e:
                    print("Shell {}".format(e))
    @classmethod
    def _output(cls, stdout, queue):
        fd = stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        # MK: stdout.readline() can't get the last line of the output.
        while (cls._process.poll() is None):
            try:
                q_len = queue.qsize()
                if q_len != 0:
                    print("queue.qsize()={}".format(q_len))
                # stdout.flush()
                # line = stdout.readline()
                # stdout.flush()
                line = stdout.read()
                print("len(stdout.readline())={}".format(len(line)))
                # if line != "":
                # print("in:{}".format(line), end="")
                cls.stdout_buf.write(line.encode())
                    # cls.stderr_buf.seek(0)

                    # queue.put(line)
                # print("returncode={}".format(cls._process.returncode))
            except TypeError as te:
                continue
            except Exception as e:
                print("except : {}".format(e))
    @classmethod
    def _create(cls):
        system = platform.system()
        if system == "Linux":
            cls._process = subprocess.Popen(
                                '/bin/bash',
                                # '/bin/sh',
                                stdin =subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True,
                                restore_signals=True,
                                bufsize=0
                                )
        elif system == "Windows":
            exit("Error. Not supported OS.")
        else:
            exit("Error. Not supported OS.")
        cls._queue_out = queue.Queue()
        cls._queue_cmd = queue.Queue()
        import io
        # cls._process.stdout = io.TextIOWrapper(open(cls._process.stdout.fileno(), 'wb', 0), write_through=True)
        cls._process.stdout.reconfigure(line_buffering=False)

        # cls._process.stdout = Unbuffered(cls._process.stdout)


        cls._thread_out = threading.Thread(
                                target=cls._output,
                                daemon=True,
                                args=(cls._process.stdout, cls._queue_out)
                                )
        cls._thread_run = threading.Thread(
                                target=cls._run,
                                daemon=True,
                                args=(cls._process.stdin, cls._queue_cmd)
                                )


        cls._thread_out.start()
        cls._thread_run.start()
        if cls._process == None:
            print("wht not?")



