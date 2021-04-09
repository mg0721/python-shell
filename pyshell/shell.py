import subprocess
import platform

class Shell:
    @staticmethod
    def _shell_linux(command):
        encoding_format = 'utf-8'
        cmd = ';'.join(command)
        p = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdin.write(cmd.encode(encoding_format))
        out, err = p.communicate()
        if out != None:
            out = out.decode(encoding_format)
        if err != None:
            err = err.decode(encoding_format)
        return out, err
    @staticmethod
    def shell(command):
        if not type(command) == type(list()):
            if type(command) == type(str()):
                command = [command]
        system = platform.system()
        if system == "Linux":
            return Shell._shell_linux(command)
        else:
            exit("Error. Not supported OS.")

