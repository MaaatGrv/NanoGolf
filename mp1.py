"""
@author: Mathis Gorvien/Ludwig Julie/Theotime Perrichet
github : https://github.com/MaaatGrv/NanoGolf.git
"""

from multiprocessing import Process,Pipe

class Test:
    def __init__(self):
        pass
    def f(self, child_conn):
        msg = 1
        child_conn.send(msg)
        child_conn.close()