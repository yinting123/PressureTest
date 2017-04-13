#-*-coding:utf-8-*-

__author__='ting.yin'
import os,sys,time,json
sys.path.append("./PressureTest/")
sys.path.append("./PressureTest/interface/gen/")
sys.path.append("./PressureTest/interface/")

sys.path.append("../interface/gen/")
sys.path.append("../interface/")
from thrift import Thrift
from thrift.Thrift import TProcessor
from thrift.transport import TTransport,TSocket
from thrift.protocol import TBinaryProtocol, TProtocol,TCompactProtocol
from se.ttypes import *
from cm.ttypes import *
from thriftproxy.ThriftProxy import Client

from dsservice.ttypes import *
from dsservice.DSServiceProxy import Client as client1
from dss.ttypes import *

class build_message(object):

    def list_request(self,region,ci,co):
        req = InnerSearchRequest()
        req.inner_search_type = 1
        req.hotel_attr = HotelAttribute()

        req.hotel_attr.return_no_product_hotel = 1
        req.hotel_attr.price_sub_coupon = 1

        # req.hotel_attr.only_consider_salable = False

        req.product_attr = ProductAttribute()
        req.product_attr.return_has_resale_hotel = 1  # 二手房
        req.product_attr.use_day_promotion = 1
        req.product_attr.return_noinv_or_noprice_product = 1
        req.product_attr.stay_date = StayDate()
        req.product_attr.stay_date.check_in = int(time.time()) + 86400 * ci
        req.product_attr.stay_date.check_out = int(time.time()) + 86400 * co
        req.product_attr.product_type = []
        req.product_attr.sell_channel = []
        req.product_attr.promotion_channel_code = '1041'  # '0000'#web0000

        req.geo_attr = GeoAttribute()
        req.geo_attr.region_id = 101

        req.page_rank_attr = PageRankAttribute()
        req.page_rank_attr.page_index = 0
        req.page_rank_attr.page_size = 100

        req.caller_attr = CallerAttribute()
        req.caller_attr.ip = "192.168.1.1"
        req.caller_attr.SearchFrom = 1
        req.caller_attr.request_origin = 3  # 3为APP


        req.customer_attr = CustomerAttribute()
        req.customer_attr.request_origin = 3
        req.customer_attr.proxy_id = 'AP0011563'  # 'AP0011563'# 'AP0011893'# 'AP0048611' #'AP0011893'#'ZD'
        req.customer_attr.order_id = 50008  # 5999 60001  50008
        req.customer_attr.member_level = 1


        req.return_attr = ReturnAttribute()
        req.return_attr.return_static_info_level = 1
        req.return_attr.return_products = 1
        req.return_attr.return_rateplan_info = 1
        req.return_attr.return_hotel_static_info = 1
        req.return_attr.return_hotel_id_only = 0

        req.user_info = UserInfo()

        req.user_info.geo_info = GeoInfo()

        req.rec_attr = RecommendAttribute()

        req.caller_attr.SearchFrom = 1
        req.product_attr.has_zydj = 1
        req.product_attr.has_majia = True

        # 五折 参与相容互斥 ，不参与
        # req.product_attr.discount_method = 3
        req.product_attr.half_discount_promotion = 3
        # 转让房 吐出转让房 不参与®
        req.product_attr.return_has_resale_hotel = 1
        ##红包
        req.product_attr.is_new_hongbao = 1
        req.product_attr.hong_bao_records = []

        req.product_attr.return_hotel_ticket_product = True
        req.product_attr.return_new_botao_member_product = True  # False #True
        return req

    def nb_request(self,data):
        req = GetInvAndInstantConfirmRequest()
        req.mhotel_attr = []
        for one in data["mhotelAttr"]:
            rs = one.split("-")
            mhotel = MhotelAttr()
            mhotels = int(rs[0])
            mhotel.mhotel_id = mhotels
            if len(rs) >= 2:
                shotels = rs[1].split('|')
                mhotel.shotel_attr = []
                for sh in shotels:
                    shotel = ShotelAttr()
                    shotel.shotel_id = int(sh)
                    if len(rs) >= 3:
                        srooms = rs[2].split('|')
                        shotel.sroom_ids = [int(x) for x in srooms]
                    mhotel.shotel_attr.append(shotel)
            req.mhotel_attr.append(mhotel)

        req.start_date = data["start_date"]
        req.end_date = data["end_date"]
        req.need_instant_confirm = data["need"] == str(True)
        # req.order_from = 1
        req.search_from = 3
        return req


class transport(object):
    def __init__(self):
        pass

    def connect(self,host,port,req):
        socket = TSocket.TSocket(host,port)
        transport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Client(protocol)
        transport.open()
        try:
            return client.SearchInner(req)
        finally:
            transport.close()

    def connect_nbInv(self,host,port,req):
        socket = TSocket.TSocket(host, port)
        transport = TTransport.TFramedTransport(socket)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        client = client1(protocol)
        transport.open()
        try:
            return client.GetInvAndInstantConfirm(req)
        finally:
            transport.close()





