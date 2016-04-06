import pytest
from facts.grafts import system_grafts
from collections.abc import Generator
from jsonspec.validators import load


@pytest.mark.asyncio
async def test_cpu():
    data = await system_grafts.cpu_info()
    assert data.namespace == 'cpu'
    assert load({
        'type': 'object',
        'properties': {
            'count': {'type': 'integer'},
            'logical': {'type': 'integer'}
        },
        'required': ['count', 'logical']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_os():
    data = await system_grafts.os_info()
    assert data.namespace is None
    assert load({
        'type': 'object',
        'properties': {
            'path': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'format': 'facts:path'
                }
            },
            'shell': {'type': 'string'},
            'uname': {
                'type': 'object',
                'properties': {
                    'machine': {'type': 'string'},
                    'node': {'type': 'string'},
                    'processor': {'type': 'string'},
                    'release': {'type': 'string'},
                    'system': {'type': 'string'},
                    'version': {'type': 'string'}
                },
                'required': ['machine', 'node', 'processor',
                             'release', 'system', 'version']
            }
        },
        'required': ['path', 'shell', 'uname']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_python():
    data = await system_grafts.python_info()
    assert data.namespace == 'python'
    assert load({
        'type': 'object',
        'properties': {
            'version': {'type': 'string'},
            'executable': {'type': 'string'},
            'path': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'format': 'facts:path'
                }
            }
        },
        'required': ['version', 'executable', 'path']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_facts():
    data = await system_grafts.facts_info()
    assert data.namespace is None
    assert load({
        'type': 'object',
        'properties': {
            'facts_version': {'type': 'string'},
            'grafts_dirs': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'format': 'facts:path'
                }
            }
        },
        'required': ['facts_version', 'grafts_dirs']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_network():
    data = await system_grafts.network_info()
    assert data.namespace is None
    assert load({
        'type': 'object',
        'properties': {
            'hostname': { 'type': 'string' },
            'ipv4': { 'type': ['string', 'null'] },
            'ipv6': { 'type': ['string', 'null'] },
        },
        'required': ['hostname', 'ipv4', 'ipv6']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_mac_addr():
    data = await system_grafts.mac_addr_info()
    assert data.namespace is None
    assert load({
        'type': 'object',
        'properties': {
            'mac': { 'type': 'string' }
        },
        'required': ['mac']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_locale():
    data = await system_grafts.locale_info()
    assert data.namespace == 'locale'
    assert 'language' in data.value
    assert 'encoding' in data.value
    assert load({
        'type': 'object',
        'properties': {
            'encoding': { 'type': ['string', 'null'] },
            'language': { 'type': ['string', 'null'] }
        },
        'required': ['encoding', 'language']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_interfaces():
    data = await system_grafts.interfaces_info()
    assert data.namespace == 'interfaces'
    assert load({
        'type': 'object',
        'patternProperties': {
            '^\w+$': {
                'type': 'object',
                'properties': {
                    'ipv6': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties':{
                                'addr': {'type': 'string', 'format': 'facts:ipv6' },
                                'netmask': {'type': 'string'},
                            }
                        }
                    }
                }
            }
        }
    }).validate(data.value)


@pytest.mark.asyncio
async def test_gateways():
    data = await system_grafts.gateways_info()
    assert data.namespace == 'gateways'
    assert load({
        'type': 'object',
        'properties': {
            'default': {
                'type': 'object',
                'properties': {
                    'ipv4': {
                        'type': 'array',
                        'items': [
                            {'type': 'string', 'format': 'ipv4'},
                            {'type': 'string'},
                        ]
                    },
                    'ipv6': {
                        'type': 'array',
                        'items': [
                            {'type': 'string', 'format': 'facts:ipv6'},
                            {'type': 'string'},
                        ]
                    }
                }
            },
            'ipv4': {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': [
                        {'type': 'string', 'format': 'ipv4'},
                        {'type': 'string'},
                        {'type': 'boolean'},
                    ]
                }
            },
            'ipv6': {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': [
                        {'type': 'string', 'format': 'facts:ipv6'},
                        {'type': 'string'},
                        {'type': 'boolean'},
                    ]
                }
            }
        },
        'required': ['default']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_uptime_data():
    data = await system_grafts.uptime_data()
    assert load({
        'type': 'object',
        'properties': {
            'uptime': {
                'type': 'number'
            },
            'boottime': {},
        },
        'required': ['boottime', 'uptime']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_memory():
    data = await system_grafts.memory_data()
    assert data.namespace == 'memory'
    assert load({
        'type': 'object',
        'properties': {
            'virtual': {
                'type': 'object',
                'properties': {
                    'free': {'type': 'integer'},
                    'percent': {'type': 'number'},
                    'total': {'type': 'integer'}
                },
                'required': ['free', 'percent', 'total']
            },
            'swap': {
                'type': 'object',
                'properties': {
                    'free': {'type': 'integer'},
                    'percent': {'type': 'number'},
                    'total': {'type': 'integer'}
                },
                'required': ['free', 'percent', 'total']
            },
        },
        'required': ['virtual', 'swap']
    }).validate(data.value)


@pytest.mark.asyncio
async def test_devices():
    data = await system_grafts.devices_data()
    assert data.namespace == 'devices'
    assert load({
        'type': 'object',
        'patternProperties': {
            '(/[^/]+)+$': {
                'type': 'object',
                'properties': {
                    'device': { 'type': 'string' },
                    'fstype': { 'type': 'string' },
                    'mountpoint': { 'type': 'string' },
                    'opts': { 'type': 'string' },
                    'usage': {
                        'properties': {
                            'free': {'type': 'integer'},
                            'percent': {'type': 'number'},
                            'size': {'type': 'integer'},
                            'used': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }).validate(data.value)
