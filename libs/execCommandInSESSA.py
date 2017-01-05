import os
import time
import subprocess
import threading
import signal
from subprocess import call
import shlex

def terminate(process):
    if process.poll() is None:
        # call('taskkill /F /T /PID ' + str(process.pid))
        # call('kill ' + str(process.pid))
        # subprocess.Popen('kill ' + str(process.pid), shell=True)
        # subprocess.Popen('kill ' + str(process.pid), shell=True)
        # subprocess.Popen('killall sessa.exe', shell=True)

        print('\n' + '='*15 + '\n->> Kill process PID = ' + str(process.pid) + '\n' + '='*15)
        # kill pycharm:
        # cmd_kill = 'kill -- -$(ps -o pgid={0} | grep -o [0-9]*)'.format(str(process.pid))
        # subprocess.Popen(cmd_kill, shell=True)

        # os.killpg(process.pid, signal.SIGINT)
        subprocess.Popen('killall wine', shell=True)
        subprocess.Popen('killall wineserver', shell=True)
        subprocess.Popen('killall winedevice.exe', shell=True)
        subprocess.Popen('killall sessa.exe', shell=True)
        subprocess.Popen('killall vpnclient.exe', shell=True)

def subprocess_execute(command, time_out=60):
    """executing the command with a watchdog"""

    # launching the command
    c = subprocess.Popen(shlex.split(command))

    # now waiting for the command to complete
    t = 0
    while t < time_out and c.poll() is None:
        time.sleep(1)  # (comment 1)
        t += 1

    # there are two possibilities for the while to have stopped:
    if c.poll() is None:
        # in the case the process did not complete, we kill it
        terminate(c)
        # and fill the return code with some error value
        returncode = -1  # (comment 2)

    else:
        # in the case the process completed normally
        returncode = c.poll()

    return returncode

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(shlex.split(self.cmd))
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            try:
                terminate(self.p)
                # self.p.kill()
                # process.terminate()
                # os.kill(self.p.pid, signal.SIGINT)
                # os.killpg(process.pid, signal.SIGINT)
                print("wine SESSA had been killed")
            except (OSError):
                print("wine SESSA had been terminated gracefully")
            # self.p.kill()      #use self.p.kill() if process needs a kill -9
            self.join()

def execProjectSession(workDir = r'/home/yugin/VirtualboxShare/Co-CoO/src/2016-11-21/tmp'):
    os.chdir(workDir)
    run_exe = 'wine cmd /C "' + workDir + '/exec.bat"'
    # p = subprocess.call(run_exe, shell=True)
    process = subprocess.Popen(run_exe, shell=True)
    while process.poll() is None:
        time.sleep(1)
        # print('waiting')

    try:
        process.kill()
        # process.terminate()
        # os.kill(process.pid, signal.SIGINT)
        # os.killpg(process.pid, signal.SIGINT)
        print("wine SESSA had been killed")
    except (OSError):
        print("wine SESSA had been terminated gracefully")

    # subprocess.call('pkill -f wine', shell=True)
    print("finished")

def execProjectSessionWithTimeoutControl(workDir = r'/home/yugin/VirtualboxShare/Co-CoO/src/2016-11-21/tmp', timeOut = 60):
    os.chdir(workDir)
    run_exe = 'wine cmd /C "' + workDir + '/exec.bat"'
    # RunCmd(run_exe, 7).Run()
    print('\n' + '='*15 + '\n--> Run process with timeout = {0}'.format(timeOut) + '\n' + '='*15)
    returncode = subprocess_execute(run_exe, time_out=timeOut)
    time.sleep(2)
    if returncode == -1: # if subprocess is error then increase a timeout by 2 times and repeat it again:
        time.sleep(10)
        print('\n' + '='*15 + '\n--> Repeat it again with timeout = {0}'.format(2*timeOut) + '\n' + '='*15)
        returncode = subprocess_execute(run_exe, time_out=2*timeOut)

    if returncode is -1:
        time.sleep(10)
        run_exe = 'touch error_timeout'
        subprocess_execute(run_exe, time_out=timeOut)

    return returncode

if __name__=='__main__':
    print('-> execCommandInSESSA run in main mode')
    execProjectSessionWithTimeoutControl(timeOut = 60)
    # execProjectSession()

    print('-> execCommandInSESSA had been finished')