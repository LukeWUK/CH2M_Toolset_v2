
__author__ = 'WebbL'


import subprocess
import os



def decompressLAZ(input, output):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)


    command = '%s\laszip -i "%s" -o "%s"' % (dir_path, input, output)

    print command

    pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    std_out, std_err = pipes.communicate()
    if pipes.returncode != 0:
        err_msg = ""
        if std_out:
            err_msg = "Output: "+ std_out
        if std_err:
            err_msg = err_msg + std_err
        return err_msg
    else:
        if len(std_out)>1:
            return std_out
        else:
            return "OK"


if __name__ == "__main__":
    input = r'C:\Temp\las_tEST\in\ALAZ.laz'
    output = r'C:\Temp\las_tEST\in\ALAS.las'
    process = decompressLAZ(input, output)