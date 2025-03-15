import os
import socket
import struct
import time

from IPy import IP


class Computer:
    def __init__(self, ip, mac, port=445):
        self.ip = ip
        self.mac = mac
        self.port = port
        self.broadcast = str(IP(f'{self.ip}/24', make_net=True)[-1]) # 局域网广播地址
        self.PASS = 'username%password'  # 用于远程关机的用户名和密码
    
    def check_status(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            res = s.connect_ex((self.ip, self.port))
        except Exception as e:
            print(e)
        finally:
            s.close()
        return True if res == 0 else False
    
    def wake_up(self):
        if len(self.mac) != 17:
            raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
        mac_address = self.mac.replace("-", '')
        data = ''.join(['FFFFFFFFFFFF', mac_address * 20])  # 构造原始数据格式
        send_data = b''
        # 把原始数据转换为16进制字节数组，
        for i in range(0, len(data), 2):
            send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])
        # print(send_data)
        # 通过socket广播出去，为避免失败，间隔广播两次
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(send_data, (self.broadcast, 7))
            time.sleep(0.1)
            s.sendto(send_data, (self.broadcast, 7))
            print("magic packet broadcast")
        except Exception as e:
            print(e)

    def shutdown(self):
        os.system(f'net rpc shutdown -I {self.ip} -U {self.PASS} -t 5')


if __name__ == '__main__':
    pc = Computer(ip='ip', mac='mac')
    print(pc.check_status())
