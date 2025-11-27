"""
[ INSEIN CORE - KERNEL INJECTOR ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

LOGIC:
Most Python "hackers" use the `socket` library. That is slow.
It creates a Python Object for every packet. DISGUSTING.

We use `ctypes` to load `libc.so.6` directly from the Linux Kernel.
We map C structures (sockaddr_in) into Python memory.
We call `sendto()` directly in C.

Is this necessary? No.
Is it insane? YES.
Does it scare other developers? ABSOLUTELY.
"""

import ctypes
import socket
import struct
import sys

# Load the C Standard Library (The Heart of Linux)
try:
    libc = ctypes.CDLL('libc.so.6')
except OSError:
    print("[!] CRITICAL: You are not on Linux. INSEIN cannot inject kernel structures.")
    sys.exit(1)

# --- C STRUCTURES MAPPING (The "Useless" Advanced Part) ---

class sockaddr_in(ctypes.Structure):
    """
    Mapping the C 'sockaddr_in' structure to Python.
    Memory layout must be EXACT or the kernel will reject it.
    """
    _fields_ = [
        ("sin_family", ctypes.c_short),
        ("sin_port",   ctypes.c_ushort),
        ("sin_addr",   ctypes.c_byte * 4),
        ("sin_zero",   ctypes.c_char * 8)
    ]

# --- DIRECT KERNEL CALLS ---

# Define C function signatures for speed
# ssize_t sendto(int sockfd, const void *buf, size_t len, int flags,
#                const struct sockaddr *dest_addr, socklen_t addrlen);
libc.sendto.argtypes = [
    ctypes.c_int,           # sockfd
    ctypes.c_void_p,        # buf
    ctypes.c_size_t,        # len
    ctypes.c_int,           # flags
    ctypes.POINTER(sockaddr_in), # dest_addr
    ctypes.c_int            # addrlen
]
libc.sendto.restype = ctypes.c_ssize_t

class KernelSocket:
    """
    A raw interface to the Linux Network Stack.
    Bypasses Python's socket object overhead for transmission.
    """
    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        # Create a raw socket using standard Python just to get the File Descriptor (FD)
        # We only need the FD (integer) to pass to C.
        try:
            self._py_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            self._py_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            self.sockfd = self._py_sock.fileno() # The golden integer
        except PermissionError:
            print("[!] CRITICAL: ROOT REQUIRED. The Ghost cannot fly without wings (sudo).")
            sys.exit(1)

    def fast_send(self, packet: bytes, target_ip: str, target_port: int):
        """
        Calls the C `sendto` function directly.
        Zero Python object overhead in the transmission path.
        """
        # Create C structure for destination
        addr = sockaddr_in()
        addr.sin_family = socket.AF_INET
        addr.sin_port = socket.htons(target_port)
        
        # Convert IP string to bytes manually (faster than inet_aton in loop if cached)
        packed_ip = socket.inet_aton(target_ip)
        # Memcopy into the C struct
        ctypes.memmove(addr.sin_addr, packed_ip, 4)

        # Cast the packet bytes to a C void pointer
        packet_buf = (ctypes.c_char * len(packet)).from_buffer_copy(packet)
        
        # THE INSANE CALL
        bytes_sent = libc.sendto(
            self.sockfd,
            packet_buf,
            len(packet),
            0,
            ctypes.byref(addr),
            ctypes.sizeof(addr)
        )
        
        if bytes_sent < 0:
            # If C returns -1, something broke in the kernel
            return False
        return True

    def close(self):
        self._py_sock.close()