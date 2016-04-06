import ipaddress


def validate_path(obj):
    return obj


def validate_ipv6_gw(obj):
    """Special ipv6 validation with gateways

    format: <IPv6 address[%interface]>
    """
    addr, _, interface = str(obj).partition('%')
    ipaddress.IPv6Address(addr)
    return obj
