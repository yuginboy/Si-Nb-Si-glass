'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-02-03
'''
import os
import time
import string
import sys
import subprocess
from libs.dir_and_file_operations import create_all_dirs_in_path_if_their_not_exist

# Collecting resources usage on the following processes
#
#   hdbnameserver
#   hdbcompileserver
#   hdbpreprocessor
#   hdbindexserver
#   hdbwebdispatcher

current_time = lambda: int(round(time.time() * 1000))


def get_process_info(process_name):
    d = [i for i in subprocess.getoutput("ps aux").split("\n")
         if i.split()[10] == str(process_name)]
    return (
    float(d[0].split()[2]), float(d[0].split()[3]), float(d[0].split()[4]), float(d[0].split()[5])) if d else None


if __name__ == '__main__':
    projPath = r'~/tmp/argos'
    projPath = create_all_dirs_in_path_if_their_not_exist(projPath)
    hdbnameserver_data = open(os.path.join(projPath, 'hdbnameserver.dat'), 'w+')
    hdbcompileserver_data = open(os.path.join(projPath, 'hdbcompileserver.dat'), 'w+')
    hdbpreprocessor_data = open(os.path.join(projPath, 'hdbpreprocessor.dat'), 'w+')
    hdbindexserver_data = open(os.path.join(projPath, 'hdbindexserver.dat'), 'w+')
    hdbwebdispatcher_data = open(os.path.join(projPath, 'hdbwebdispatcher.dat'), 'w+')

    try:
        while True:
            hdbnameserver_data.write("%.2f\t%.2f\t%.2f\t%.2f" % get_process_info("htop"))
            hdbnameserver_data.write("%.2f\t%.2f\t%.2f\t%.2f" % get_process_info("hdbnameserver"))
            hdbcompileserver_data.write("%.2f\t%.2f\t%.2f\t%.2f" % get_process_info("hdbcompileserver"))
            hdbpreprocessor_data.write("%.2f\t%.2f\t%.2f\t%.2f" % get_process_info("hdbpreprocessor"))
            hdbindexserver_data.write("%.2f\t%.2f\t%.2f\t%.2f" % get_process_info("hdbindexserver"))
            hdbwebdispatcher_data.write("%.2f\t%.2f\t%.2f\t%.2f" % get_process_info("hdbwebdispatcher"))

            time.sleep(2)
    except KeyboardInterrupt:
        print("all data in ~/tmp/argos/")
        exit(0)