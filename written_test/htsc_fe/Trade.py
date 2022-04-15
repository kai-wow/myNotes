'''
根据因子信号进行交易
Class
- Stock  进行单只股票的 买、卖、更新当日市值 等操作
- Trade  根据策略信号 进行 买buy()、卖sell()、更新持仓净值hold() 等操作
    - 需调用 Stock 类
Return
- trade_data [dict]  {date_time: {
                            'date_time','all_position_value', 'cash',
                            'value', 'signal', 'cost',
                            '','r_price','position', 'position_value'}
                     }
'''
# 买卖都用开盘价
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
import pickle


class Asset():
    def __init__(self, type):
        # 传入当日 价格数据
        self.type = type

        # 交易数据
        # self.price = price_dict[type]

        # 以前的 trade数据
        self.trade_gain = None
        self.position = None
        self.position_value = None

    def __str__(self) -> str:
        param_list = ['type', 'r_price', 'position', 'position_value']
        value = [(name, getattr(self, name)) for name in param_list]
        f_string = ''
        for i, (item, count) in enumerate(value):
            f_string += (f'#{i + 1}: '
                         f'{item.title():<15s} = '
                         f'{count}\n')
        return f_string

    def buy(self, price_data, amount):
        self.get_current_price(price_data)
        self.position = amount // self.price
        self.position_value = self.position * self.price
        return self.position_value

    def sell(self, price_data):
        self.get_current_price(price_data)
        self.position = 0
        self.position_value = self.position * self.price
        # return self.position_value

    def get_current_price(self, price_data):
        self.price = price_data[self.type]
        return self.price

    def get_position_value(self, price_data):
        self.get_current_price(price_data)
        self.position_value = self.position * self.price
        return self.position_value


class Trade():
    def __init__(self, price_data, current_date=datetime.datetime(2011, 7, 1)):
        self.date_time = current_date  # signalData.date_time
        self.time_frequency = 240  # 日度
        self.price_data = price_data
        self.stock = Asset(type='沪深300')
        self.bond = Asset(type='国债')
        self.current_price = self.price_data[current_date]
        self.weight = None

        self.trade_data_path = r'C:\Users\shao\Desktop\CUHKSZ\programming\project\trade_data.csv'

        # 参数
        self.allocation = 10000000
        self.commission = 0.0003

        self.holding_stock = []  # 存储 stock 实例
        self.holding_stock_code = []
        self.cash = self.allocation  # 初始化现金为上期现金值
        self.cost = None
        self.trade_gain = None
        self.all_position_value = None
        self.value = None

    def __str__(self) -> str:
        param_list = ['date_time', 'price_data',
                      'allocation', 'commission',
                      'all_position_value', 'cash', 'value', 'cost',
                      ]
        value = [(name, getattr(self, name)) for name in param_list]
        f_string = ''
        for i, (item, count) in enumerate(value):
            f_string += (f'#{i + 1}: '
                         f'{item.title():<15s} = '
                         f'{count}\n')
        return f_string

    def update(self, date):
        self.date_time = date  # signalData.date_time
        # self.weight = weight
        self.current_price = self.price_data[date]

    # 买入合约，并获取 头寸净值、策略净值
    def buy(self, weight):
        # 对每个股票进行买卖
        self.weight = weight
        self.stock.buy(self.current_price, weight['沪深300'] * self.allocation)
        self.bond.buy(self.current_price, weight['国债'] * self.allocation)

        self.all_position_value = self.stock.position_value + self.bond.position_value

        self.cash = self.cash - self.all_position_value
        self.value = self.cash + self.all_position_value

    def sell(self):
        # 非多即空 和 无空仓 的交易一致
        sold_position_value = 0

        self.stock.get_position_value(self.current_price)
        sold_position_value += self.stock.position_value
        self.stock.sell(self.current_price)

        self.bond.get_position_value(self.current_price)
        sold_position_value += self.bond.position_value
        self.bond.sell(self.current_price)

        self.all_position_value = 0
        self.cash = self.cash + sold_position_value

        self.value = self.cash + self.all_position_value

    def hold(self):
        # update current position value
        self.stock.get_position_value(self.current_price)
        self.bond.get_position_value(self.current_price)
        self.all_position_value = self.stock.position_value + self.bond.position_value

        # 头寸计算用 开盘价
        self.cost = 0
        # cash 不变
        self.value = self.cash + self.all_position_value

    def trade(self, weight=None):
        if self.signal == 1:  # 买入
            self.buy(weight)

        elif self.signal == -1:  # 卖出持仓股，不持股
            self.sell()
            self.buy(weight)
            # sell_cost = self.cost

        elif self.signal == 0:  # 无交易
            if len(self.holding_stock) != 0:  # 如果有持股，则更新价格数据
                self.hold()
            else:  # 如果无持股，则持仓价值为 0
                self.all_position_value = 0
                self.cost = 0

        self.value = self.all_position_value + self.cash

    # 获取 并 存储
    def get_trade_data(self):
        '''
        Return
            trade_data [dict]  {date_time: {
                                    'date_time','all_position_value', 'cash',
                                    'value', 'signal', 'cost',
                                    'stock_code','r_price','position', 'position_value'}
        '''
        param_list = ['all_position_value',
                      'cash', 'value', 'weight']
        value = {name: getattr(self, name) for name in param_list}

        # 每支个股的数据
        stock_param = ['type', 'price', 'position', 'position_value']
        for i in [self.stock, self.bond]:
            for name in stock_param:
                value[getattr(i, 'type') + '_' + name] = getattr(i, name)

        self.trade_data = {self.date_time: value}
        return value

    def show_trading_info(self, stock_list):
        if self.signal > 0:
            print(f'{self.date_time}买入{stock_list}，持仓价值{self.all_position_value:.2f}，剩余{self.cash:.2f}现金')
        elif self.signal < 0:
            print(f'{self.date_time}卖出{stock_list}股票，剩余{self.cash:.2f}现金')
        else:
            print(f'{self.date_time} 无操作，当前持仓价值{self.all_position_value:.2f}，总资产{self.value:.2f}')
        print()

    def save_trade_data(self):
        trade_data = pd.DataFrame.from_dict(self.trade_data, orient='index')

        if os.path.exists(os.path.split(self.trade_data_path)[0]):
            if os.path.exists(self.trade_data_path):
                trade_data_before = pd.read_csv(self.trade_data_path, index_col=0)
                trade_data = pd.concat([trade_data_before, trade_data])
                # 存入文件再读出来后，就发生: date_time 格式变为 str
                trade_data['date_time'] = pd.to_datetime(trade_data['date_time'])
                trade_data.sort_values(by='date_time', ascending=True, inplace=True)
                trade_data.drop_duplicates(subset='date_time', keep='last', inplace=True)
            else:  # 若无 旧数据
                pass
        else:
            os.makedirs(os.path.split(self.trade_data_path)[0])

        trade_data.to_csv(self.trade_data_path, index_label='time_index')  # , index=False

    def get_all_trade_data(self, path=None):
        '''
        Return
            trade_data [dict]  {date_time: {
                                    'date_time','all_position_value', 'cash',
                                    'value', 'signal', 'cost',
                                    'stock_code','r_price','position', 'position_value'}
        '''
        if path == None:
            path = self.trade_data_path
        all_trade_data = pd.read_csv(path, index_col='time_index')
        print(all_trade_data)
        all_trade_data = all_trade_data.to_dict(orient='index')
        return all_trade_data

    def run(self, save=True):
        self.trade()
        self.get_trade_data()
        if save:
            self.save_trade_data()
        self.show_trading_info()


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    from strategy import *
    trade_dt, trade_price = load_data(path='国内股债收盘价.xlsx')
    opinion_dt, opinions = load_data(path='增长-通胀观点.xlsx')
    print(trade_price[trade_dt[0]], opinions[opinion_dt[0]])

    trade_dt = [d for d in trade_dt if d>=opinion_dt[0]]
    # buy_stock = load_obj(r'data\lossstop(4).pkl')
    # all_trade_date = [key for key, value in buy_stock.items()]

    # get price data and change into dict
    # stock_data = pd.read_csv('data\open.csv', header=0, index_col=0)
    # stock_data.index = [(datetime.datetime.strptime(x, '%Y-%m-%d')) for x in stock_data.index]
    # stock_prices = stock_data.to_dict(orient='index')
    # benchmark = pd.read_csv('data\HS300_open.csv', header=0, index_col=0)
    # benchmark.index = [(datetime.datetime.strptime(x, '%Y-%m-%d')) for x in
    #                    benchmark.index]  # pd.to_datetime(benchmark.index)
    # benchmark_price = benchmark['OPEN'].to_dict()

    # create instance
    trade = Trade(trade_price, current_date=trade_dt[0])  # 传入数据
    trade.buy(weight={'沪深300': 0.8, '国债': 0.2})

    # begin_of_month = [trade_dt[i+1] for i in range(len(trade_dt)) if trade_dt[i] in opinion_dt]
    trade_info = {}
    begin_of_month = False
    for date in trade_dt:
        # update the backtest data
        trade.update(date)  # 更新价格
        if begin_of_month:  # 买入 date in
            trade.sell()
            trade.buy(weight)
        else:
            trade.hold()
        trade_info[date] = trade.get_trade_data()
        print(date, trade.value)

        # trade.get_trade_data()
        # # print(trade.trade_data)
        # trade.show_trading_info(buy_stock[date]['stocks'])
        # trade.save_trade_data()

        if date in opinion_dt:
            begin_of_month = True  # 第二天是 月初
            weight = get_trading_signal(opinions[date])
            print(date,'月末', weight)
        else:
            begin_of_month = True

    # trade.get_all_trade_data()
    print(trade_info[date])
    trade_data = pd.DataFrame.from_dict(trade_info, 'index')
    print(trade_data)
    print(trade_data.columns)

    plt.plot(trade_data['value']/trade_data['value'].iloc[0], label='策略')
    plt.plot(trade_data['沪深300_price']/trade_data['沪深300_price'].iloc[0], label='沪深300')
    plt.plot(trade_data['国债_price']/trade_data['国债_price'].iloc[0], label='国债')
    plt.legend()
    plt.show()