from pyshell import Shell
import time

# https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
# https://stackoverflow.com/questions/33886406/how-to-avoid-the-deadlock-in-a-subprocess-without-using-communicate
# https://stackoverflow.com/questions/7206519/executing-bash-with-subprocess-popen
# https://stackoverflow.com/questions/8495794/python-popen-stdout-readline-hangs

if __name__ == "__main__":
    sh = Shell()
    sh.shell("python3.7 test/test_input.py")
    # sh.shell("python test/test_input.py") <==== python2. error.
    sh.shell("aaabbbaa")
    # print(    )
    # time.sleep(0.5)
    # sh.shell("ls -a")
    # sh.shell("sleep 1; echo yes no | grep yes;")
    sh.shell("sleep 1")
    # sh.shell("ls -l")
    sh.shell("cat ./test/file")
    # sh.join()
    # while True:
    #     time.sleep(0.1)
    out, err = sh.out()
    for o in out:
        print(o)
    # [print(o, end='') for o in out]
        

# import subprocess
# from threading import Thread
# import time

# linebuffer=[]

# x=subprocess.Popen(['/bin/bash','-c',"while true; do sleep 5; echo yes; done"],stdout=subprocess.PIPE)
# def reader(f,buffer):
#     while True:
#         line=f.readline()
#         if line:
#             buffer.append(line)
#         else:
#             break

# t=Thread(target=reader,args=(x.stdout,linebuffer))
# t.daemon=True
# t.start()
# while True:
#     if linebuffer:
#         print(linebuffer.pop(0))
#     else:
#         print("nothing here")
#         time.sleep(1)

