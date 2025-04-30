#!/usr/bin/env python3
import socket
import struct
import time

def get_ntp_time(host='pool.ntp.org', port=123):
    # build 48-byte NTP request
    req = bytearray(48)
    req[0] = 0x1B  # LI=0, VN=3, Mode=3 (client)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(req, (host, port))
        data, _ = s.recvfrom(48)
    mv = memoryview(data)
    secs = struct.unpack_from('!I', mv, 40)[0]
    frac = struct.unpack_from('!I', mv, 44)[0]
    return secs - 2208988800 + frac / 2**32

if __name__ == '__main__':
    t = get_ntp_time()
    print("NTP time:", time.ctime(t))

