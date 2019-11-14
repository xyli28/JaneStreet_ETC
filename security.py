import statistics
SECURITIES = ['BOND', 'GS', 'MS', 'WFC', 'XLF', 'VALBZ', 'VALE']

class Security(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.position = 0 # Total position
        self.cost = 0 # Total cost
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
        
        if operation == 'covert':
            ## TO-DO check covert
            if self.symbol == 'XLF':
                trade.update({'symbol': self.symbol, 'dir': 'BUY', 'size': size})
                return trade
            else:
                print('Current symbol: {} can not be coverted'.format(self.symbol))
        if operation == 'add':
                trade.update({'symbol': self.symbol, 'dir': sellOrbuy, 'size': size, 'price': price})
        return trade

