from pyshell import Shell
import time

if __name__ == "__main__":
    sh = Shell()
    print(sh.shell("python3 test/user_input.py"))
    print(sh.shell("aaabbbaa"))
    print(sh.shell("ls -a"))
    print(sh.shell(["sleep 3", "echo yes no | grep yes"]))