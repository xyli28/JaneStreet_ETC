#!/usr/bin/python
from __future__ import print_function, division
from utils import monitor, Security
import json


def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

# ADR position can not over 10

class tradeADR:
    '''
    VALBZ more liquid, VALE less liquid
    '''
    CONFEE = 10
    def __init__(self):
        self.symbol = ['VALBZ', 'VALE']
        self.valbz_book = Security('VALBZ')
        self.vale_book = Security('VALE')
        self.monitor = monitor(self.symbol, 1)
        self.order_id = 0
    
    def _getOrder(self):
        self.order_id += 1
        return self.order_id

    def _convertADR(self, order_id, OrderDir, size):
        if OrderDir == 'bz2e':
            self.valbz_book.convertOrder(order_id, 'SELL', size)
            self.valbz_book.position -= size
            self.vale_book.position += size
        elif OrderDir == 'e2bz':
            self.valbz_book.convertOrder(order_id, 'BUY', size)
            self.valbz_book.position += size
            self.vale_book.position -= size

    def arbitrage(self, message, exchange):
        '''
        vale volumn is important
        buy in vale, liquide in valbz vale['sell'] must smaller than valbz['buy'] than 2
        sell in vale, liquide in valbz vale['buy'] must smaller than valz['sell']
        '''
        if not self.monitor.updateOrder(message):
            return
        
        vale = self.monitor.getCurBook('VALE')
        valbz = self.monitor.getCurBook('VALBZ')
        print(vale, valbz)
        if vale['sell'][0] < valbz['buy'][0]:
            '''
            buy in vale, liquide in valbz
            '''
            diff = valbz['buy'][0] - vale['sell'][0] - 2
            buyPrice = vale['sell'][0] + 1
            salePrice = valbz['buy'][0] - 1
            buySize = min([vale['sell'][1], valbz['buy']
                           [1], 10 - self.vale_book.position])
            if buySize * diff > tradeADR.CONFEE:
                print('buy vale sell valbz')
                write_to_exchange(exchange, self.vale_book.buyOrder(self._getOrder(), buySize, buyPrice))
                write_to_exchange(exchange, self.valbz_book.sellOrder(
                    self._getOrder(), buySize, salePrice))
                write_to_exchange(exchange, self._convertADR(self._getOrder(), 'e2bz', buySize))
        else:
            '''
            sell in vale, buy in valbz
            '''
            diff = valbz['sell'][0] - vale['buy'][0] - 2
            salePrice = vale['buy'][0] - 1
            buyPrice = valbz['sell'][0] + 1
            buySize = min([vale['buy'][1], valbz['sell'][1], - self.vale_book.position])
            if buySize * diff > tradeADR.CONFEE:
                print('sell vale buy valbz')
                write_to_exchange(exchange, self.vale_book.sellOrder(
                    self._getOrder(), buySize, salePrice))
                write_to_exchange(exchange, self.valbz_book.buyOrder(
                    self._getOrder(), buySize, buyPrice))
                write_to_exchange(exchange, self._convertADR(
                    self._getOrder(), 'e2bz', buySize))





