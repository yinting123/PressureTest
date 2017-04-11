#-*-coding:utf-8-*-

import sys
sys.path.append('./PressureTest')

sys.path.append('../')
from base.build_message import *
from conf.config import *

HOST= '192.168.233.17'
PORT = 5100

class Transaction(object):
    def __init__(self):
        self.result = []

    def run(self):
        bm = build_message()
        request = bm.list_request(region,check_in,check_out)
        trans = transport()
        res = trans.connect(HOST,PORT,request)
        self.result.append(res.status.msg)

if __name__=="__main__":
    trans = Transaction()
    trans.run()
    for line in  trans.result:
        print line