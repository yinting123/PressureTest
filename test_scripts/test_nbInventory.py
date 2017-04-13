#-*-coding:utf-8-*-

import sys,ConfigParser,json
sys.path.append('./PressureTest')
sys.path.append('./PressureTest/conf/')

sys.path.append('../')
from base.build_message import *


HOST = '192.168.233.17'
HOST = '192.168.35.17'
PORT = 5400

class Transaction(object):
    def __init__(self):
        self.result = []

    def run(self):
        cfg = ConfigParser.ConfigParser()
        # cfg.read('./PressureTest/conf/data.conf')
        cfg.read('../conf/data.conf')
        bm = build_message()
        req = bm.nb_request(json.loads(cfg.get('NB','data').decode('utf-8')))
        con = transport()
        res = con.connect_nbInv(cfg.get('NB','HOST'),
                                cfg.getint('NB','PORT'),req)
        res = con.connect_nbInv(HOST,PORT,req)
        self.result.append(res)


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    for line in trans.result:
        print line




