# -*- coding: iso8859-15 -*-
import json
import os
import shutil
import subprocess
import signal
import gc
import re
from kivy.logger import Logger

_cur_dir = '/root/wsd'

def is_rpi():
    try:
        return 'arm' in os.uname()[4]
    except AttributeError:
        return False


def get_serial():
    """
    Get serial number of the device
    :return:
    """
    if is_rpi():
        cpuserial = "0000000000000000"
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26].lstrip('0')
        f.close()
        return cpuserial
    else:
        return '12345678'


_json_file = os.path.join(_cur_dir, 'config_{}.json'.format(get_serial()))
if not os.path.exists(_json_file):
    print('No JSON Config File Found! Recovering the default one...')
    shutil.copy(os.path.join(_cur_dir, 'config.json'), _json_file)


def update_config_file(data):
    json_data = json.loads(open(_json_file).read())
    json_data.update(data)
    with open(_json_file, 'w') as outfile:
        json.dump(json_data, outfile, indent=2)


def get_config():
    return json.loads(open(_json_file).read())


def kill_process_by_name(proc_name):
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.decode().splitlines():
        if proc_name in line:
            pid = int(line.split(None, 1)[0])
            print('Found PID({}) of `{}`, killing...'.format(pid, proc_name))
            os.kill(pid, signal.SIGKILL)


def number_to_ordinal(n):
    """
    Convert number to ordinal number string
    """
    return "%d%s" % (n, "tsnrhtdd"[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def get_free_gpu_size():
    gc.collect()
    if is_rpi():
        try:
            pipe = os.popen('vcdbg reloc stats | grep "free memory"')
            data = pipe.read().strip()
            pipe.close()
            return data
        except OSError:
            Logger.error('!!! Failed to get free GPU size! ')
            tot, used, free = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
            Logger.error('Total: {}, Used: {}, Free: {}'.format(tot, used, free))
    return 0


def disable_screen_saver():
    if is_rpi():
        os.system('sudo sh -c "TERM=linux setterm -blank 0 >/dev/tty0"')


def get_screen_resolution():
    """
    Get resolution of the screen
    :return:
    """
    if is_rpi():
        pipe = os.popen('fbset -s')
        data = pipe.read().strip()
        pipe.close()

        pattern = re.compile(r"^mode\s*\"(?P<width>\d+)x(?P<height>\d+)(-0)?\".*$", re.MULTILINE)
        matches = pattern.match(data)

        width = int(matches.group("width"))
        height = int(matches.group("height"))

        return width, height

        """
        for line in data.splitlines():
            if line.startswith('mode'):
                w, h = [int(p) for p in line.split('"')[1].split('x')]
                return w, h
        """
    else:
        return 1024, 600


def check_running_proc(proc_name):
    """
    Check if a process is running or not
    :param proc_name:
    :return:
    """
    try:
        if len(os.popen("ps -aef | grep -i '%s' "
                        "| grep -v 'grep' | awk '{ print $3 }'" % proc_name).read().strip().splitlines()) > 0:
            return True
    except Exception as e:
        print('Failed to get status of the process({}) - {}'.format(proc_name, e))
    return False

def set_system_time(datetime):
    """
    Set the system time using a datetime object and update the hardware clock if present
    """
    os.system('date -s "%s"' % datetime.strftime('%Y-%m-%d %H:%M'))
    os.system('hwclock -w')

