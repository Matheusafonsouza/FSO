import os
import subprocess


signal_mapper = {
    'SIGTERM': 15,
    'SIGINT': 2,
    'SIGUSR1': 10,
    'SIGUSR2': 12
}


def send_signal(pid, signal):
    if signal in signal_mapper.keys():
        signal = signal_mapper[signal]
    reqstr = 'kill -s {} {}'.format(signal, pid)
    return subprocess.getstatusoutput(reqstr)[1]


def get_pid(process_name):
    return subprocess.getstatusoutput(
        "ps x | grep {} | head -n 1 | cut -d' ' -f3"
        .format(process_name))[1]


fl = input()

# Compile
os.system('gcc -O2 -static ' + fl)

# Run
proc = subprocess.Popen(['./a.out'])

# Get pid
pid = get_pid('./a.out')

while True:
    try:
        inp = input()
    except EOFError:
        break

    print(send_signal(pid, inp))

# Kill the process
send_signal(pid, 'SIGHUP')
