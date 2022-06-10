from multiprocessing import Process,Pipe

class Test:
    def __init__(self):
        pass
    def f(self, child_conn):
        msg = 1
        child_conn.send(msg)
        child_conn.close()