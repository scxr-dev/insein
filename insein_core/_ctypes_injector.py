"""
[ INSEIN CORE - KERNEL INJECTOR ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

"""

import ctypes
import socket
import struct
import sys

try:
    libc = ctypes.CDLL('libc.so.6')
except OSError:
    print("[!] CRITICAL: You are not on Linux. INSEIN cannot inject kernel structures.")
    sys.exit(1)


class sockaddr_in(ctypes.Structure):

    _fields_ = [
        ("sin_family", ctypes.c_short),
        ("sin_port",   ctypes.c_ushort),
        ("sin_addr",   ctypes.c_byte * 4),
        ("sin_zero",   ctypes.c_char * 8)
    ]


libc.sendto.argtypes = [
    ctypes.c_int,           
    ctypes.c_void_p,        
    ctypes.c_size_t,        
    ctypes.c_int,           
    ctypes.POINTER(sockaddr_in), 
    ctypes.c_int            
]
libc.sendto.restype = ctypes.c_ssize_t

class KernelSocket:

    def __init__(self, interface: str = "eth0"):
        self.interface = interface

        try:
            self._py_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            self._py_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            self.sockfd = self._py_sock.fileno() # The golden integer
        except PermissionError:
            print("[!] CRITICAL: ROOT REQUIRED. The Ghost cannot fly without wings (sudo).")
            sys.exit(1)

    def fast_send(self, packet: bytes, target_ip: str, target_port: int):
 
        addr = sockaddr_in()
        addr.sin_family = socket.AF_INET
        addr.sin_port = socket.htons(target_port)
        
        packed_ip = socket.inet_aton(target_ip)
       
        ctypes.memmove(addr.sin_addr, packed_ip, 4)

        
        packet_buf = (ctypes.c_char * len(packet)).from_buffer_copy(packet)
        
        
        bytes_sent = libc.sendto(
            self.sockfd,
            packet_buf,
            len(packet),
            0,
            ctypes.byref(addr),
            ctypes.sizeof(addr)
        )
        
        if bytes_sent < 0:
           
            return False
        return True

    def close(self):
        self._py_sock.close()