#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/14 14:30
# @Author  : luoxiaojian
# @Site    : 
# @File    : sysinfo.py.py
# @Software: PyCharm
import os
import sys
import json
import subprocess
import psutil
import socket
import platform
import requests



device_white = ['eth0','eth1', 'eth2', 'eth3', 'enp0s3', 'bond1']


def check_root():
    if os.geteuid() != 0:
        print("Permission denied, Please switch root user exec.")
        sys.exit(1)


def get_hostname():
    return socket.gethostname()

def get_device_info():
    ret = []
    for device, info in psutil.net_if_addrs().items():
        if device in device_white:
            device_info = {'device': device}
            for snic in info:
                if snic.family == 2:
                    device_info['ip'] = snic.address
                elif snic.family == 17:
                    device_info['mac'] = snic.address
            ret.append(device_info)
    return ret

def get_cpuinfo():
    ret = {"cpu": '', 'num': 0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            line_list = line.strip().split(':')
            key = line_list[0].rstrip()
            if key == "model name":
                ret['cpu'] = line_list[1].lstrip()
            if key == "processor":
                ret['num'] += 1
    return ret

def get_disk():
    cmd = """/sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'|head -1"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    partition_size = []
    for dev in disk_data.stdout.readlines():
        # print(dev)
        size = int(str(dev).strip().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
        partition_size.append(str(size))
    return partition_size  # 10.6 + 20.5 + 100
    # return " + ".join(partition_size)  # 10.6 + 20.5 + 100

def get_Manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines():
        line  = str(line)
        if "Manufacturer" in line:
            ret['manufacturers'] = line.split(': ')[1].strip()
        elif "Product Name" in line:
            ret['server_type'] = line.split(': ')[1].strip()
        elif "Serial Number" in line:
            ret['st'] = line.split(': ')[1].strip().replace(' ','')
        elif "UUID" in line:
            ret['uuid'] = line.split(': ')[1].strip()
    return ret
    #return manufacturer_data.stdout.readline().split(': ')[1].strip()

# 出厂日期
def get_rel_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    _dtime = p.stdout.readlines()[0].strip().decode("utf-8").split(': ')[1].strip()
    _dtime = _dtime.split("/")
    _dtime.reverse()
    dtime = '-'.join(_dtime)
    return dtime

def get_os_version():
    return " ".join(platform.linux_distribution())

def get_innerIp(ipinfo):
    inner_device = ["eth0", "enp0s3"]
    ret = {}
    for info in ipinfo:
        if info.get('ip') and info.get('device', None) in inner_device:
            ret['private_ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return  ret
    return {}

def run():
    check_root()

    data = {}
    data['hostname'] = get_hostname()
    data.update(get_innerIp(get_device_info()))
    cpuinfo = get_cpuinfo()
    data['server_type'] = "{cpu} {num}".format(**cpuinfo)
    data['disk'] = get_disk()
    data.update( get_Manufacturer())
    data['manufacture_date'] = get_rel_date()
    data['os'] = get_os_version()
    data['cpu'] = cpuinfo['num']
    if "VMware" in data['manufacturers']:
        data['vm_status'] = 0
    else:
        data['vm_status'] = 1

    print(json.dumps(data, indent=4))
    # for k,v in data.items():
    #     print(k, v)
    # send(data)

def send(data):
    url = "http://127.0.0.1:8000/api/v1/cmdb/collect"
    req = requests.post(url, data=data)
    print(req.ok)
    print(req.text)



if __name__ == "__main__":
    run()