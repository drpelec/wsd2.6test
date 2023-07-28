#!/usr/bin/python
import os
import subprocess


MOUNT_PATH = '/media/usb'


def get_connected_usb_device():
    pipe = os.popen('ls -l /dev/disk/by-path/*-usb-* | fgrep -v part')
    data = pipe.read().strip()
    pipe.close()
    for line in data.splitlines():
        dev_path = '/dev/' + line.split('/')[-1]
        pipe = os.popen('ls {}*'.format(dev_path))
        data = pipe.read().strip()      # '/dev/sda\n/dev/sda1'
        pipe.close()
        for _line in data.splitlines():
            if _line != dev_path:
                return _line


def save_file_to_usb_drive(usb_path, file_path):
    if not os.path.exists(MOUNT_PATH):
        os.makedirs(MOUNT_PATH)
    cmd_list = [
        'mount {} {}'.format(usb_path, MOUNT_PATH),
        'cp {} {}/'.format(file_path, MOUNT_PATH),
        'umount {}'.format(MOUNT_PATH),
    ]
    for cmd in cmd_list:
        _p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = _p.communicate()
        if err != '':
            print('Failed to save file to the USB drive - {}'.format(err))
            return False
        print(out)
        _p.wait()
    return True


def get_file_list_from_usb_drive(usb_path):
    if not os.path.exists(MOUNT_PATH):
        os.makedirs(MOUNT_PATH)
    cmd_list = [
        'mount {} {}'.format(usb_path, MOUNT_PATH),
        'find "{}" -maxdepth 1 -iname "*.xlsx"'.format(MOUNT_PATH),
        'umount {}'.format(MOUNT_PATH),
    ]

    # mount drive
    _p = subprocess.Popen(cmd_list[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = _p.communicate()
    if err != '':
        print('Failed to read the USB drive - {}'.format(err))
        return None
    _p.wait()

    files = []
    # list xlsx files in usb drive
    pipe = os.popen(cmd_list[1])
    data = pipe.read().strip()
    pipe.close()
    # try to parse as file list
    for line in data.splitlines():
        filename = line.split('/')[-1]
        files.append(filename)
    if len(files):
        files = sorted(files, reverse=True)

    # unmount drive
    _p = subprocess.Popen(cmd_list[2], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = _p.communicate()
    if err != '':
        print('Failed to read the USB drive - {}'.format(err))
        return None
    _p.wait()

    return files


def load_file_from_usb_drive(usb_path, file_path):
    if not os.path.exists(MOUNT_PATH):
        os.makedirs(MOUNT_PATH)

    dest = "/tmp/{}".format(file_path)
    cmd_list = [
        'mount {} {}'.format(usb_path, MOUNT_PATH),
        'cp {}/{} {}'.format(MOUNT_PATH, file_path, dest),
        'umount {}'.format(MOUNT_PATH),
    ]
    for cmd in cmd_list:
        _p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = _p.communicate()
        if err != '':
            print('Failed to save file to the USB drive - {}'.format(err))
            return None
        print(out)
        _p.wait()
    return dest


if __name__ == '__main__':
    print(get_connected_usb_device())
