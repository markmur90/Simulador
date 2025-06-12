# /home/markmur88/api_bank_h2/utils/allow_internal_network.py

import ipaddress
from django.core.exceptions import DisallowedHost


class AllowInternalNetworkMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_networks = [
            ipaddress.ip_network("127.0.0.0/8"),
            ipaddress.ip_network("192.168.0.0/16"),
            ipaddress.ip_network("10.0.0.0/8"),
            ipaddress.ip_network("172.16.0.0/12"),
            ipaddress.ip_network("193.150."),
            ipaddress.ip_network("*.*"),
            ipaddress.ip_network("0.0.0.0"),
        ]

    def __call__(self, request):
        ip = ipaddress.ip_address(request.META.get('REMOTE_ADDR', ''))
        if not any(ip in net for net in self.allowed_networks):
            raise DisallowedHost(f"Blocked IP: {ip}")
        return self.get_response(request)
