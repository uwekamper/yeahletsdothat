#!/usr/bin/python
# -*- coding: utf-8 -*-

# import jsonrpclib
from campaigns.payment_method import BasePaymentMethod
from django.conf import settings

def get_rpc_address(conf=None):
    if conf == None:
        conf = settings
    return 'http://{}:{}@{}:{}/'.format(conf.BTC_USER, conf.BTC_PASS, conf.BTC_HOST, conf.BTC_PORT)

def create_bitcoin_address(address=None):
    if not address:
        address = get_rpc_address()
    server = None
    # server = jsonrpclib.Server(address)
    new_addr = server.getnewaddress()
    return new_addr

class BitCoin(BasePaymentMethod):

    def __init__(self, options):
        super(BitCoin, self).__init__(options)

    def pay(self, campaign, transaction):
        # TODO implement this
        pass

    def refund(self, campaign, transaction):
        pass