#!/usr/bin/python
from __future__ import print_function, division



class Security(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.position = 0  # Total position
        self.cost = 0  # Total cost
        self.OrderHist = {'BUY': {}, 'SELL': {}}
        self.buySize, self.sellSize = 0, 0
        pass

    def buyOrder(self, order_id, price, size):
        self.buySize += size
        trade = self._Order('add', order_id, price, size, 'BUY')
        self.OrderHist['BUY'][order_id] = trade
        return trade

    def sellOrder(self, order_id, price, size):
        self.sellSize += size
        trade = self._Order('add', order_id, price, size, 'SELL')
        self.OrderHist['SELL'][order_id] = trade
        return trade
    
    def convertOrder(self, order_id, sellOrbuy, size):
        trade = self._Order('convert', order_id, None, size, sellOrbuy)
        return trade

    def fill(self, order):
        _orderid = order['order_id']
        _bors = order['dir']
        _size = order['size']

        if _size == self.OrderHist[_bors][_orderid]['size']:
            self.OrderHist[_bors].pop(_orderid)
        else:
            self.OrderHist[_bors][_orderid]['size'] -= _size

        if _bors == 'BUY':
            self.cost += _size * order['price']
            self.position += _size
            self.buySize -= _size

        elif _bors == 'SELL':
            self.cost -= _size * order['price']
            self.position -= _size
            self.sellSize -= _size
        pass

    def cancel(self, order_id):
        trade = self._Order('cancel', order_id, None, None, None)
        return trade

    def _Order(self, operation, order_id, price, size, sellOrbuy):

        trade = {'type': operation, 'order_id': order_id}
        if operation == 'cancel':
            return trade

        if operation == 'convert':
            ## TO-DO check covert
            if self.symbol in ['VALBZ', 'VALE', 'XLF']:
                trade.update(
                    {'symbol': self.symbol, 'dir': 'BUY', 'size': size})
                return trade
            else:
                print('Current symbol: {} can not be coverted'.format(self.symbol))
        if operation == 'add':
                trade.update({'symbol': self.symbol, 'dir': sellOrbuy, 'size': size, 'price': price})
        return trade

def convertADR(buy_sec, sell_sec, order_id, size):
    tradeOrder = buy_sec.convertOrder(order_id, 'BUY', size)
    buy_sec.position += size
    sell_sec.position -= size
    return tradeOrder

class monitor(object):
    '''
    symbols: symbols to monitor
    last_len: last trade length
    updateLastLen: method update last_len
    getTick: return (cur_max_buy - last_max_buy) (cur_min_sell - last_min_sell)
    updateOrder: update order information if symbols inte order in the symbols we are monitoring
    '''
    def __init__(self, symbols, last_len):
        self.symbols = symbols
        self.last_trade_len = last_len
        self.histTrade = {symbol: [] for symbol in self.symbols} # [price, size]
        self.histTradeMean = {symbol: -1 for symbol in self.symbols}
        self.lastPrice = {symbol: {'buy': -1, 'sell': -1} for symbol in self.symbols} # maybe ['buy', 'sell']
        self.book = {symbol: {'buy': [], 'sell': []}
                       for symbol in self.symbols}
        self.spread = {symbol: -1 for symbol in self.symbols}
    
    def getLastPrice(self, symbol):
        if symbol in self.symbols:
            return [self.lastPrice[symbol]['buy'], self.lastPrice[symbol]['sell']]
        else:
            return
            
    def getCurBook(self, symbol):
        if symbol in self.symbols:
            return self.book[symbol]

    def getLastTradePrice(self, symbol):
        if symbol in self.symbols:
            return self.histTradeMean[symbol]
        else:
            return
    
    def updateLastLen(self, last_len):
        self.last_trade_len = last_len

    def getTick(self, order_symbol, symbol):
        buy_tick = order_symbol['buy'][0][0] - self.lastPrice[symbol]['buy'][0]
        sell_tick = order_symbol['sell'][0][0] - self.lastPrice[symbol]['sell'][0]
        return buy_tick, sell_tick

    def updateOrder(self, order):
        if order['type'] is not 'book':
            return False
        if order['symbol'] not in self.symbols:
            return False
        
        if order['type'] == 'book':
            self._updateSymbol(order, order['symbol'])
        elif order['type'] == 'trade':
            self._updateTrade(order, order['symbol'])
        else:
            pass
        pass

    def _updateTrade(self, order_trade, symbol):
        if len(self.histTrade[symbol]) > self.last_trade_len:
            self.histTrade[symbol].pop()

        self.histTrade[symbol].append([order_trade['price'], order_trade['size']])
        
        priceTotal, sizeTotal = 0, 0
        for item in self.histTrade[symbol]:
            sizeTotal += item[1]
            priceTotal += item[0] * item[1]
        self.histTradeMean[symbol] = priceTotal / sizeTotal
            
    def _updateSymbol(self, order_symbol, symbol):
        buy, sell = order_symbol['buy'], order_symbol['sell']
        if buy:
            self.lastPrice[symbol]['buy'], self.book[symbol]['buy'] = buy[0], buy
        
        if sell:
            self.lastPrice[symbol]['sell'], self.book[symbol]['sell'] = sell[0], sell
        self._updateSpread(symbol)
        pass

    def _updateSpread(self, symbol):
        if self.lastPrice[symbol]['buy'] and self.lastPrice[symbol]['sell']:
            self.spread[symbol] = self.lastPrice[symbol]['sell'] - self.lastPrice[symbol]['buy']
        else:
            pass
