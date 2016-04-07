from . import graft
from contextlib import suppress
from facts import mark
from uuid import getnode as get_mac
import locale
import netifaces
import os
import platform
import psutil
import socket
import sys
import uptime


@graft(namespace='cpu')
async def cpu_info():
    """Returns cpu data.
    """
    return {
        'count': psutil.cpu_count(logical=False),
        'logical': psutil.cpu_count()
    }


@graft
async def os_info():
    """Returns os data.
    """
    return {
        'uname': dict(platform.uname()._asdict()),
        'path': os.environ.get('PATH', '').split(':'),
        'shell': os.environ.get('SHELL', '/bin/sh'),
    }


@graft(namespace='python')
async def python_info():
    """Returns Python data.
    """
    return {
        'version': '%s.%s.%s-%s%s' % sys.version_info,
        'executable': sys.executable,
        'path': sys.path
    }


@graft
async def facts_info():
    """Returns facts library data.
    """
    from facts import __version__
    from . import __path__ as grafts_dirs
    return {
        'facts_version': __version__,
        'grafts_dirs': grafts_dirs
    }


@graft
async def network_info():
    """Returns hostname, ipv4 and ipv6.
    """

    def extract(host, family):
        return socket.getaddrinfo(host, None, family)[0][4][0]
    host = socket.gethostname()
    response = {
        'hostname': host,
        'ipv4': None,
        'ipv6': None
    }
    with suppress(IndexError, socket.gaierror):
        response['ipv4'] = extract(host, socket.AF_INET)
    with suppress(IndexError, socket.gaierror):
        response['ipv6'] = extract(host, socket.AF_INET6)
    return response


@graft
async def mac_addr_info():
    """Returns mac address.
    """
    mac = get_mac()
    if mac == get_mac():  # not random generated
        hexa = '%012x' % mac
        value = ':'.join(hexa[i:i+2] for i in range(0, 12, 2))
    else:
        value = None
    return {'mac': value}


@graft(namespace='locale')
async def locale_info():
    """Returns locale data.
    """
    code, encoding = locale.getdefaultlocale()
    return {
        'language': code,
        'encoding': encoding
    }


@graft(namespace='interfaces')
async def interfaces_info():
    """Returns interfaces data.
    """
    def replace(value):
        if value == netifaces.AF_LINK:
            return 'link'
        if value == netifaces.AF_INET:
            return 'ipv4'
        if value == netifaces.AF_INET6:
            return 'ipv6'
        return value

    results = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        results[iface] = {replace(k): v for k, v in addrs.items()}

    return results


@graft(namespace='gateways')
async def gateways_info():
    """Returns gateways data.
    """
    data = netifaces.gateways()
    results = {'default': {}}

    def expand(data):
        addr, interface, is_default = data
        return {
            'addr': addr,
            'interface': interface,
            'default': is_default
        }

    def expand2(data):
        addr, interface = data
        return {
            'addr': addr,
            'interface': interface
        }

    with suppress(KeyError):
        results['ipv4'] = [expand(elt) for elt in data[netifaces.AF_INET]]
        elt = expand2(data['default'][netifaces.AF_INET])
        results['default']['ipv4'] = elt
    with suppress(KeyError):
        results['ipv6'] = [expand(elt) for elt in data[netifaces.AF_INET6]]
        elt = expand2(data['default'][netifaces.AF_INET6])
        results['default']['ipv6'] = elt

    return results


@graft(namespace='uptime')
async def uptime_data():
    """Returns uptime data.
    """
    return {
        'uptime': mark(uptime.uptime(), 'duration'),
        'boottime': uptime.boottime()
    }


@graft(namespace='memory')
async def memory_data():
    """Returns memory data.
    """
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()

    return {
        'virtual': {
            'total': mark(vm.total, 'bytes'),
            'free': mark(vm.free, 'bytes'),
            'percent': mark(vm.percent, 'percentage')
        },
        'swap': {
            'total': mark(sw.total, 'bytes'),
            'free': mark(sw.free, 'bytes'),
            'percent': mark(sw.percent, 'percentage')
        },
    }


@graft(namespace='devices')
async def devices_data():
    """Returns devices data.
    """
    response = {}
    for part in psutil.disk_partitions():
        device = part.device
        response[device] = {
            'device': device,
            'mountpoint': part.mountpoint,
            'fstype': part.fstype,
            'opts': part.opts,
        }
        if part.mountpoint:
            usage = psutil.disk_usage(part.mountpoint)
            response[device]['usage'] = {
                'size': mark(usage.total, 'bytes'),
                'used': mark(usage.used, 'bytes'),
                'free': mark(usage.free, 'bytes'),
                'percent': mark(usage.percent, 'percentage')
            }
    return response
