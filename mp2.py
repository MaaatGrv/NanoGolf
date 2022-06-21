"""
@author: Mathis Gorvien/Ludwig Julie/Theotime Perrichet
github : https://github.com/MaaatGrv/NanoGolf.git
"""

from multiprocessing import Process,Queue,Pipe
from mp1 import Test

def print_msg():
    print("Hello from child process")

def print_msg2()
    print("Hello from child process2")

if __name__ == '__main__':
    V = Test()
    parent_conn,child_conn = Pipe()
    p = Process(target=V.f, args=(child_conn,))
    p.start()
    d = parent_conn.recv()
    if d==1:
        print_msg()