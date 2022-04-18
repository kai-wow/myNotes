""" 2020.08.28  9:57
美林时钟
"""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']


def load_data(path='国内股债收盘价.xlsx'):
    # 数据导入
    data = pd.read_excel(path)
    data.set_index(data["日期"], inplace=True)
    dates = list(data.index)  # 记录交易日信息，方便以后进行查找
    data_dict = data.to_dict(orient='index')
    # csi300 = data['沪深300'].to_dict()
    # bond = data['国债'].to_dict()  # 国债ETF专属数据结构。仅保留收盘价格
    return dates, data_dict


def get_trading_signal(opinions=None, benchmark=False):
    if benchmark:
        return {'沪深300': 0.2, '国债': 0.8}

    # weight = {'csi300': 0, 'bond': 0}
    if opinions['增长'] == -1 and opinions['通胀'] == -1:  # 衰退
        weight = {'沪深300': 0.6, '国债': 0.4}
    elif opinions['增长'] == -1 and opinions['通胀'] == 1:  # 滞胀
        weight = {'沪深300': 0.7, '国债': 0.3}
    elif opinions['增长'] == 1 and opinions['通胀'] == -1:  # 复苏
        weight = {'沪深300': 0.9, '国债': 0.1}
    elif opinions['增长'] == 1 and opinions['通胀'] == 1:  # 过热
        weight = {'沪深300': 0.9, '国债': 0.1}
    else:
        weight = {'沪深300': 0.8, '国债': 0.2}
    # elif opinions['增长'] == 0 and opinions['通胀'] == 1:
    #     pass
    # elif opinions['增长'] == 0 and opinions['通胀'] == -1:
    #     pass
    # elif opinions['增长'] == 1 and opinions['通胀'] == 1:
    #     pass
    return weight

if __name__ == "__main__":
    trade_dt, trade_price = load_data(path='国内股债收盘价.xlsx')
    opinion_dt, opinions = load_data(path='增长-通胀观点.xlsx')
    print([d for d in opinion_dt if d in trade_dt])
    print(trade_price[trade_dt[0]], opinions[opinion_dt[0]])
