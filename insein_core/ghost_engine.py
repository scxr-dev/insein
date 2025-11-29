"""
[ INSEIN CORE - GHOST ENGINE ]
AUTHOR: R H A Ashan Imalka (scxr-dev)

LOGIC:
We construct raw binary packets using `struct`.
We implement the "Half-Open" (Stealth) scan manually.

UPDATES:
- Fixed: Added IPv4 Header construction (Required for IP_HDRINCL).
- Added: Decoy Storm logic (Sends fake packets from random IPs).
"""

import socket
import struct
import array
import os
import random
import asyncio
import time
from ._ctypes_injector import KernelSocket


TCP_FIN = 0x01
TCP_SYN = 0x02
TCP_RST = 0x04
TCP_PSH = 0x08
TCP_ACK = 0x10
TCP_URG = 0x20

def checksum(msg: bytes) -> int:
    s = 0
    if len(msg) % 2 == 1:
        msg += b'\0'
    for i in range(0, len(msg), 2):
        w = (msg[i] << 8) + msg[i+1]
        s = s + w
    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    return (~s) & 0xffff

class GhostPacket:
    
    def __init__(self, src_ip, dst_ip, dst_port, payload=None):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.src_port = random.randint(1024, 65535)
        self.seq = random.randint(0, 4294967295)
        self.ack_seq = 0
        self.window = 5840
        self.payload = payload or b""

    def build_ip(self, tcp_packet_len):
       
        ihl = 5
        version = 4
        tos = 0
        tot_len = 20 + tcp_packet_len
        id_ = random.randint(10000, 50000)
        frag_off = 0
        ttl = 64
        protocol = socket.IPPROTO_TCP
        check = 0 
        saddr = socket.inet_aton(self.src_ip)
        daddr = socket.inet_aton(self.dst_ip)

        ihl_version = (version << 4) + ihl

        ip_header = struct.pack('!BBHHHBBH4s4s', 
            ihl_version, tos, tot_len, id_, frag_off, ttl, protocol, check, saddr, daddr)
        
        return ip_header

    def build_tcp(self, flags=TCP_SYN):
        
        doff = 5
        
        tcp_header_pack = struct.pack(
            '!HHLLBBHHH',
            self.src_port, self.dst_port, self.seq, self.ack_seq, 
            (doff << 4), flags, self.window, 0, 0
        )

        source_address = socket.inet_aton(self.src_ip)
        dest_address = socket.inet_aton(self.dst_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header_pack) + len(self.payload)

        psh = struct.pack(
            '!4s4sBBH',
            source_address, dest_address, placeholder, protocol, tcp_length
        )

        full_packet_for_chk = psh + tcp_header_pack + self.payload
        tcp_checksum = checksum(full_packet_for_chk)

        tcp_header = struct.pack(
            '!HHLLBBHHH',
            self.src_port, self.dst_port, self.seq, self.ack_seq, 
            (doff << 4), flags, self.window, tcp_checksum, 0
        )
        
        return tcp_header + self.payload

    def get_full_packet(self):
        
        tcp_part = self.build_tcp()
        ip_part = self.build_ip(len(tcp_part))
        return ip_part + tcp_part

class GhostScanner:
    def __init__(self, target_ip, decoy_generator=None):
        self.target_ip = target_ip
        # Safe local IP detection
        self.local_ip = self._get_local_ip() 
        self.kernel = KernelSocket()
        self.open_ports = []
        self.decoys = []
        self.decoy_generator = decoy_generator

    def load_decoys(self, decoys):
        self.decoys = decoys

    def _get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
           
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except Exception:
            
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    async def scan_port(self, port: int):
        # 1. Real Packet
        real_pkt = GhostPacket(self.local_ip, self.target_ip, port).get_full_packet()
        self.kernel.fast_send(real_pkt, self.target_ip, port)

        # 2. Decoy Packets
        if self.decoys:
            for decoy_ip in random.sample(self.decoys, min(2, len(self.decoys))):
                fake_pkt = GhostPacket(decoy_ip, self.target_ip, port).get_full_packet()
                self.kernel.fast_send(fake_pkt, self.target_ip, port)
        return True

    def sniff_responses(self, timeout=2):
        try:
            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return

        sniffer.settimeout(timeout)

        try:
            while True:
                try:
                    raw_data, addr = sniffer.recvfrom(65535)
                    if addr[0] == self.target_ip:
                        ip_header_len = (raw_data[0] & 0xF) * 4
                        tcp_header_raw = raw_data[ip_header_len:ip_header_len+20]
                        tcph = struct.unpack('!HHLLBBHHH', tcp_header_raw)
                        src_port = tcph[0]
                        flags = tcph[5]
                        
                        if flags == 0x12: # SYN-ACK
                            if src_port not in self.open_ports:
                                self.open_ports.append(src_port)
                except socket.timeout:
                    pass
                except Exception:
                    pass
        except KeyboardInterrupt:
            pass
        finally:
            sniffer.close()

    async def run_scan(self, port_range: list):
        tasks = []
        for port in port_range:
            tasks.append(self.scan_port(port))
            if len(tasks) % 50 == 0:
                await asyncio.sleep(0.02)
        await asyncio.gather(*tasks)