class Bond(object):
    """
    strategies for bond   
    """
   
    def __init__(self):
        self.state = 0     
        self.buy_order = 0
        self.sell_order = 0   


    def marketMaking(self,order_id,book):
        trades[]
        trades.append({'type': 'add', 'order_id': order_id.getOrderID(), 
                       'symbol': 'BOND', 'dir': 'SELL',
                       'price': 1001, 'size': 1})
        
        self.sell_order = order_id.order_id  
        trades.append({'type': 'add', 'order_id': order_id.getOrderID(), 
                       'symbol': 'BOND', 'dir': 'BUY',
                       'price': 1000, 'size': 0})
        self.buy_order = order_id.order_id
        return trades

        
        
