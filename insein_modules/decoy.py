"""
[ INSEIN MODULE - DECOY SYSTEM ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

DESCRIPTION:
Generates valid random IP addresses to be used as decoys during scanning.
Filters out private, reserved, and loopback ranges to ensure decoys appear legitimate
to the target firewall.
"""

import random
import struct
import socket

class DecoyGenerator:
    def __init__(self):
        # Ranges to exclude (Private, Loopback, Multicast, Reserved)
        self.reserved_ranges = [
            (self._ip_to_int('10.0.0.0'), self._ip_to_int('10.255.255.255')),
            (self._ip_to_int('172.16.0.0'), self._ip_to_int('172.31.255.255')),
            (self._ip_to_int('192.168.0.0'), self._ip_to_int('192.168.255.255')),
            (self._ip_to_int('127.0.0.0'), self._ip_to_int('127.255.255.255')),
            (self._ip_to_int('0.0.0.0'), self._ip_to_int('0.255.255.255')),
            (self._ip_to_int('224.0.0.0'), self._ip_to_int('255.255.255.255'))
        ]

    def _ip_to_int(self, ip_str: str) -> int:
        """Converts IP string to integer for comparison."""
        packed = socket.inet_aton(ip_str)
        return struct.unpack("!L", packed)[0]

    def _int_to_ip(self, ip_int: int) -> str:
        """Converts integer back to IP string."""
        packed = struct.pack("!L", ip_int)
        return socket.inet_ntoa(packed)

    def _is_reserved(self, ip_int: int) -> bool:
        """Checks if the generated IP falls into reserved ranges."""
        for start, end in self.reserved_ranges:
            if start <= ip_int <= end:
                return True
        return False

    def generate_batch(self, count: int = 5) -> list:
        """
        Generates a batch of valid, non-reserved random IP addresses.
        
        Args:
            count (int): Number of decoy IPs to generate.
            
        Returns:
            list: List of IP address strings.
        """
        decoys = []
        while len(decoys) < count:
            ip_int = random.randint(0, 4294967295)
            if not self._is_reserved(ip_int):
                decoys.append(self._int_to_ip(ip_int))
        return decoys