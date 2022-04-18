'''
根据 评估数据 将策略表现可视化
绘制各种图片并保存：最大损益区间图、策略净值标的净值对比图、最大回撤图
Class & Functions
- Pictures      [class]
    需要调用 Evaluate() , 获取 策略评估数据
    Functions:
        - draw_winLoseTopN         最大损益区间图
        - draw_value_ret           策略净值标的净值对比图
        - draw_rolling_drawdown    最大回撤图
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Trade import Trade
from Evaluate import Evaluate, get_return


class Pictures():
    def __init__(self, trade_data, holding_gain) -> None:
        self.time_frequency = 240

        self.trade_data = trade_data # EvaluateData.trade_data
        self.holding_gain = holding_gain # EvaluateData.get_holding_gain()

        self.savefig_path = r"C:\Users\shao\Desktop\CUHKSZ\programming\project\_"

    # holding gain
    def draw_winLoseTopN(self, n=3):
        # 获取 Top n 盈亏的 买入、卖出index
        data = self.trade_data.copy()
        pos_perform = self.holding_gain

        pos_perform.loc[:, 'gain_rank_ds'] = pos_perform['gain'].rank(method='first', ascending=False)  # 自大到小排列
        pos_perform.loc[:, 'gain_rank_as'] = pos_perform['gain'].rank(method='first', ascending=True)  # 自小到大排列
        print(pos_perform)
        win_topN_buy = list(pos_perform[pos_perform['gain_rank_ds'] <= n].index)
        win_topN_sell = list(pos_perform.shift(1)[pos_perform['gain_rank_ds'] <= n].index)
        lose_topN_buy = list(pos_perform[pos_perform['gain_rank_as'] <= n].index)
        lose_topN_sell = list(pos_perform.shift(1)[pos_perform['gain_rank_as'] <= n].index)
        win_topN = [win_topN_buy, win_topN_sell]
        lose_topN = [lose_topN_buy, lose_topN_sell]
        print(win_topN, lose_topN)

        # 画图
        # 将策略净值放缩到和 r_open初始值一样的水平上
        data.loc[:, 'stra_Val'] = data['value']  # * data['r_open'].iloc[0]/data['value'].iloc[0]

        # data.set_index(['date_time'], inplace=True)
        highest = data['value'].max()
        lowest = data['value'].min()
        buy_idx = list(data[data.position_chg > 0].index)

        plt.figure(figsize=(7, 5))

        plt.plot(data['value'], label="strategy value", color='r', linewidth=1)
        plt.plot(data['value'][buy_idx], 'g^', label="buy", markersize=5)

        # 高亮 TOP n的盈亏区间
        if len(win_topN[0]) < n:
            n = len(win_topN[0])
            print(f'trading signals are less than {n}!')
            # raise NameError('trading signals are less than N!')
        if len(win_topN[0]) > 0:
            for i in range(n):
                plt.fill_between(np.array(data.loc[win_topN[0][i]:win_topN[1][i]].index),
                                 lowest, highest, facecolor='red', alpha=0.3)
                plt.fill_between(np.array(data.loc[lose_topN[0][i]:lose_topN[1][i]].index),
                                 lowest, highest, facecolor='green', alpha=0.3)
            plt.legend(loc=0)
            plt.show()  # savefig(self.savefig_path + "trading_sig.png")
            plt.close()
        data.reset_index(inplace=True)

    def draw_value_ret(self):
        strate_data = self.trade_data.copy()
        strate_data.loc[:, 'bench_net_val'] = np.divide(strate_data['benchmark_value'],
                                                        strate_data['benchmark_value'].iloc[0])
        strate_data.loc[:, 'stra_net_val'] = strate_data.loc[:, 'value'] / strate_data['value'].iloc[0]
        strate_data.loc[:, 'abs_ret'] = np.divide(strate_data.loc[:, 'stra_net_val'],
                                                  strate_data.loc[:, 'bench_net_val'])
        # 分钟收益

        ### 画图：策略净值、标的净值、绝对收益
        # 总图
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 画图：策略净值、标的净值、绝对收益
        fig, ax = plt.subplots(figsize=(12, 6))
        line1 = ax.plot(strate_data['bench_net_val'], 'g', label="标的累计净值", linewidth=1)
        line2 = ax.plot(strate_data['stra_net_val'], 'r', label="策略净值", linewidth=1.5)
        ax2 = ax.twinx()
        line3 = ax2.plot(strate_data['abs_ret'], 'b--', label="绝对收益", linewidth=1)
        lns = line1 + line2 + line3
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=2)
        ax.set_xlabel("Date")
        # ax2.set_ylim(0, 0.5)
        plt.title("策略表现")
        # plt.show()
        plt.show()  # savefig(self.savefig_path + "all_strategy_netValue.png")
        plt.close()

    def draw_rolling_drawdown(self):
        '''
        Function
            求滚动回撤率序列，并求出总的最大回撤和最大回测时间
            绘图 策略回撤率
        Parameters
            price_data  [dataframe]  数据[['date_time','bench_netVal']]
            allocation  [int]        初始资金（和策略净值 bench_netVal 配套）
        Return
            rolling_d  [dataframe]  年度最大回撤数据[['year','dd_ratio','date_time']]
            drawdown_list [list]    回撤数据 [最大回撤, 最大回撤时间]
        '''
        # 取最大值序列，和当前的price减一下得到新序列，最大回测 = 新序列的最大值/最大值序列
        price_data = self.trade_data.copy()
        price_data.loc[:, 'cummax_price'] = price_data['value'].cummax()
        price_data.loc[:, 'dd'] = -np.subtract(price_data.loc[:, 'cummax_price'], price_data.loc[:, 'value'])
        price_data.loc[:, 'dd_ratio'] = np.divide(price_data.loc[:, 'dd'], price_data.loc[:, 'cummax_price'])

        plt.bar(price_data.index, height=price_data['dd_ratio'])
        plt.title("策略回撤率")
        plt.show()  # savefig(self.savefig_path+"_drawdown_ratio.png")
        plt.close()

    def paint(self):
        self.draw_winLoseTopN()
        self.draw_value_ret()
        self.draw_rolling_drawdown()


if __name__ == '__main__':
    trade = Trade([], [])

    analyse = Evaluate(trade)
    analyse.evaluate()

    picture = Pictures(analyse)
    picture.paint()


