from fyers.script import name_to_script
class quote:
    def __init__(self,fyers):
        self.fyers=fyers.fyers
    def quote(self,stock_name):
        stock_name=name_to_script(stock_name)
        data=data = {"symbols":stock_name}
        return self.fyers.quotes(data)['d'][0]['v']['cmd']['o']