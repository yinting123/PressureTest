#-*-coding:utf-8-*-

import sys,ConfigParser
sys.path.append('./PressureTest')

sys.path.append('../')
from base.build_message import *


HOST= '192.168.233.17'
PORT = 5100

class Transaction(object):
    def __init__(self):
        self.result = []

    def run(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read('./PressureTest/conf/data.conf')
        bm = build_message()
        request = bm.list_request(cfg.get('SA','region'),cfg.get('SA','check_in'),
                                  cfg.get('SA', 'check_out'))
        trans = transport()
        res = trans.connect(cfg.get('SA','HOST'),cfg.getint('SA','PORT'),request)
        self.result.append(res.status.msg)

if __name__=="__main__":
    trans = Transaction()
    trans.run()
    for line in  trans.result:
        print line