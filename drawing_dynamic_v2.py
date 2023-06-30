# coding=utf-8
import pandas as pd
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import json
import requests
from MyTT import *
import matplotlib
import sys

sys.setrecursionlimit(10000)  # 嵌套层数
matplotlib.use('tkagg')  # 独立窗口


class StockData(object):
    def get_eastmoney_trade_data(self, code='515030', period=30, fqt=0, day_num=500):
        """ 可以获取实时数据股票与场内基金
        :param code: 代码
        :param period:周期
        :param fqt: 是否加权
        :return:
        基金举例1.515030 0.159919
        """
        code = '1.' + code if code[0] in ['6', '5'] else '0.' + code
        if period == 'd':
            url = 'http://56.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404111304433712406_1607946908499&' \
                  'secid={0}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=0&end=20500101&' \
                  'lmt={1}&_=1607946908538' \
                .format(code, day_num)
        else:
            url = "http://51.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112401333280111780102_1638622653459&" \
                  "secid={0}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&" \
                  "klt={1}&fqt=0&beg=0&end=20500101&smplmt=460&lmt=1000&_=1638622653551" \
                .format(code, period)
        html = requests.get(url)
        info = html.text[42:-2]
        info = json.loads(info)
        code = info['data']['code']
        name = info['data']['name']
        history = info['data']['klines']
        stock_values = []
        # amp为振幅 pctChg为涨幅 increase涨跌额 turn换手率
        info_head = ['code', 'name', 'date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'amp', 'pctChg',
                     'increase', 'turn']

        for his in history:  # 股票的为逆序
            val = [code, name] + his.split(",")
            stock_values.append(val)
        df = pd.DataFrame(stock_values, columns=info_head)
        df = df.rename(columns={'date': 'datetime'})
        df.index = pd.DatetimeIndex(df['datetime'])
        df['open'] = df['open'].astype('float')
        df['close'] = df['close'].astype('float')
        df['high'] = df['high'].astype('float')
        df['low'] = df['low'].astype('float')
        df['volume'] = df['volume'].astype('float')
        return df


# 自定义风格和颜色
# 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
my_color = mpf.make_marketcolors(up='r',  # 上涨K线的柱子的内部填充色
                                 down='g',  # 下跌K线的柱子的内部填充色
                                 edge='inherit',  # 边框设置“inherit”代表使用主配色 不设置则为黑色
                                 wick='inherit',  # wick设置的就是上下影线的颜色
                                 volume='inherit')  # volume设置的是交易量柱子的颜色
# 设置图表的背景色
my_style = mpf.make_mpf_style(marketcolors=my_color,
                              figcolor='(0.82, 0.83, 0.85)',
                              gridcolor='(0.82, 0.83, 0.85)')

# 定义各种字体
title_font = {'fontname': 'pingfang HK',
              'size': '16',
              'color': 'black',
              'weight': 'bold',
              'va': 'bottom',
              'ha': 'center'}
large_red_font = {'fontname': 'Arial',
                  'size': '24',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom'}
large_green_font = {'fontname': 'Arial',
                    'size': '24',
                    'color': 'green',
                    'weight': 'bold',
                    'va': 'bottom'}
small_red_font = {'fontname': 'Arial',
                  'size': '12',
                  'color': 'red',
                  'weight': 'bold',
                  'va': 'bottom'}
small_green_font = {'fontname': 'Arial',
                    'size': '12',
                    'color': 'green',
                    'weight': 'bold',
                    'va': 'bottom'}
normal_label_font = {'fontname': 'pingfang HK',
                     'size': '12',
                     'color': 'black',
                     'weight': 'normal',
                     'va': 'bottom',
                     'ha': 'right'}
normal_font = {'fontname': 'Arial',
               'size': '12',
               'color': 'black',
               'weight': 'normal',
               'va': 'bottom',
               'ha': 'left'}


class InterCandle:
    def __init__(self, data, name, window_len=60):
        self.buy = 0
        self.sell = 0
        self.data = data
        self.name = name
        self.t1 = ""
        self.t2 = ""
        self.date = ""
        self.curt = time.strftime("%Y%m%d%H", time.localtime())
        self.file = open('op_log.txt', 'w+')
        self.profit = 0
        self.all_profit = 0
        self.close = 0
        self.log = ''
        self.start = 0  # 开始序号
        self.len = window_len  # 显示长度
        # 添加三个图表，四个数字分别代表图表左下角在figure中的坐标，以及图表的宽（0.88）、高（0.60）
        self.fig = mpf.figure(figsize=(12, 8), facecolor=(0.82, 0.83, 0.85))
        # 添加三个图表，四个数字分别代表图表左下角在figure中的坐标，以及图表的宽（0.88）、高（0.60）
        self.price_axe = self.fig.add_axes([0.06, 0.25, 0.88, 0.60])  # 添加价格图表 K线图
        # 添加第二、三张图表时，使用sharex关键字指明与ax1在x轴上对齐，且共用x轴
        self.volume_axe = self.fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=self.price_axe)  # 添加成交量
        self.macd_axe = self.fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=self.price_axe)  # 添加macd
        # 设置三张图表的Y轴标签
        self.price_axe.set_ylabel('price')
        self.volume_axe.set_ylabel('volume')
        # self.macd_axe.set_ylabel('macd')

        # 标题等文本
        # 初始化figure对象，在figure上预先放置文本并设置格式，文本内容根据需要显示的数据实时更新
        self.t1 = self.fig.text(0.50, 0.94, self.name, **title_font)
        self.t2 = self.fig.text(0.10, 0.90, '今收: ', **normal_label_font)
        self.t2_1 = self.fig.text(0.10, 0.90, f'', **small_red_font)
        self.t21 = self.fig.text(0.19, 0.90, '涨幅: ', **normal_label_font)
        self.t21_1 = self.fig.text(0.19, 0.90, f'', **small_red_font)
        self.t3 = self.fig.text(0.325, 0.90, '今开/昨收: ', **normal_label_font)
        self.t3_1 = self.fig.text(0.40, 0.90, f'', **normal_label_font)
        self.t4 = self.fig.text(0.45, 0.90, '振幅: ', **normal_label_font)
        self.t4_1 = self.fig.text(0.49, 0.90, f'', **normal_label_font)
        self.t5 = self.fig.text(0.45, 0.87, '量比: ', **normal_label_font)  # 55 58
        self.t5_1 = self.fig.text(0.49, 0.87, f'', **normal_label_font)
        self.t52 = self.fig.text(0.57, 0.87, '换手率: ', **normal_label_font)  # 71 75
        self.t52_1 = self.fig.text(0.62, 0.87, f'', **normal_label_font)
        self.t53 = self.fig.text(0.57, 0.90, 'RSI6: ', **normal_label_font)  # 85 89
        self.t53_1 = self.fig.text(0.62, 0.90, f'', **normal_label_font)
        self.t6 = self.fig.text(0.845, 0.87, '日期:', **normal_label_font)
        self.t6_1 = self.fig.text(0.925, 0.87, f' ', **normal_label_font)
        self.t7 = self.fig.text(0.10, 0.87, 'MA5: ', **normal_label_font)
        self.t7_1 = self.fig.text(0.10, 0.87, f'', **normal_font)
        self.t8 = self.fig.text(0.20, 0.87, 'MA10: ', **normal_label_font)
        self.t8_1 = self.fig.text(0.20, 0.87, f'', **normal_font)
        self.t9 = self.fig.text(0.30, 0.87, 'MA20: ', **normal_label_font)
        self.t9_1 = self.fig.text(0.30, 0.87, f'', **normal_font)
        self.t13 = self.fig.text(0.10, 0.81, '均线: ', **normal_label_font)
        self.t13_1 = self.fig.text(0.10, 0.81, f'', **normal_font)
        self.t14 = self.fig.text(0.10, 0.75, '收益: ', **normal_label_font)
        self.t14_1 = self.fig.text(0.10, 0.75, f'', **normal_font)
        self.t15 = self.fig.text(0.10, 0.70, '总收: ', **normal_label_font)
        self.t15_1 = self.fig.text(0.10, 0.70, f'', **normal_font)
        self.t16 = self.fig.text(0.10, 0.65, '日志: ', **normal_label_font)
        self.t16_1 = self.fig.text(0.10, 0.65, f'', **normal_font)

        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def plt_show(self):
        self.refresh_plot(self.data.iloc[self.start:self.start + self.len])

    def refresh_plot(self, plot_data):
        # 刷新图
        # 读取显示区间最后一个交易日的数据
        last_data = plot_data.iloc[-1]
        last_data2 = plot_data.iloc[-2]
        self.close = last_data["close"]
        # 将这些数据分别填入figure对象上的文本中
        self.t2_1.set_text(f'{np.round(last_data["close"], 3)}')
        self.t21_1.set_text(f'{np.round(last_data["pctChg"], 3)}%')
        self.t3_1.set_text(f'{np.round(last_data["open"], 3)}/{np.round(last_data2["close"], 3)}')
        self.t4_1.set_text(f'{np.round(last_data["amp"], 2)}%')
        self.t5_1.set_text(f'{np.round(last_data["vol_rate"], 2)}')
        self.t52_1.set_text(f'{np.round(last_data["turn"], 2)}%')
        self.t53_1.set_text(f'{np.round(last_data["rsi"], 2)}')

        self.date = last_data["date"]
        self.t6_1.set_text(f'{last_data["date"]}')
        self.t7_1.set_text(f'{np.round(last_data["MA5"], 2)}')
        self.t8_1.set_text(f'{np.round(last_data["MA10"], 2)}')
        self.t9_1.set_text(f'{np.round(last_data["MA20"], 2)}')
        self.t13_1.set_text(f'{last_data["cross"]}')
        self.t14_1.set_text(f'{np.round(self.profit, 2)}%')
        self.t15_1.set_text(f'{np.round(self.all_profit, 2)}%')
        self.t16_1.set_text(f'{self.log}')

        if last_data['pctChg'] > 0:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'red'
        elif last_data['pctChg'] < 0:  # 如果今日变动额小于0，即今天价格低于昨天，今天价格显示为绿色
            close_number_color = 'green'
        else:
            close_number_color = 'black'
        self.t21_1.set_color(close_number_color)
        self.t2_1.set_color(close_number_color)

        if last_data['MA5'] > last_data['MA10']:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'blue'
        else:
            close_number_color = 'black'
        self.t7_1.set_color(close_number_color)

        if 3 * (last_data['turn_avg'] * 5 - last_data['turn']) / 4 <= last_data[
            'turn']:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'blue'
        elif (last_data['turn_avg'] * 5 - last_data['turn']) / 4 >= 3 * last_data['turn']:
            close_number_color = 'yellow'
        else:
            close_number_color = 'black'
        self.t52_1.set_color(close_number_color)

        if 3 * (last_data['vol_avg'] * 5 - last_data['volume']) / 4 <= last_data['volume']:  # 大于4日前的平均3倍
            close_number_color = 'blue'
        elif (last_data['vol_avg'] * 5 - last_data['volume']) / 4 >= 3 * last_data['volume']:
            close_number_color = 'yellow'
        else:
            close_number_color = 'black'
        self.t5_1.set_color(close_number_color)

        if last_data['rsi'] >= 92:  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'red'
        elif last_data['rsi'] <= 25:
            close_number_color = 'blue'
        else:
            close_number_color = 'black'
        self.t53_1.set_color(close_number_color)

        if last_data['cross'] == 'B':  # 如果今日变动额大于0，即今天价格高于昨天，今天价格显示为红色
            close_number_color = 'red'
        elif last_data['cross'] == 'S':
            close_number_color = 'green'
        else:
            close_number_color = 'black'
        self.t13_1.set_color(close_number_color)

        # 生成一个空列表用于存储多个addplot
        ap = []
        # 添加均线
        ap.append(mpf.make_addplot(plot_data[['MA5', 'MA10', 'MA20']], ax=self.price_axe))
        # 添加 diff 和 dea
        # ap.append(mpf.make_addplot(plot_data[['diff']], color='black', ax=self.macd_axe))
        # ap.append(mpf.make_addplot(plot_data[['dea']], color='orange', ax=self.macd_axe))
        # 添加macd
        # ap.append(mpf.make_addplot(plot_data[['macd']], type='bar', color='green', ax=self.macd_axe))
        #  调用mpf.plot()函数，这里需要指定ax=price_axe，volume=ax2，将K线图显示在ax1中，交易量显示在ax2中
        mpf.plot(plot_data, ax=self.price_axe, addplot=ap, volume=self.volume_axe, type='candle', style=my_style,
                 xrotation=0)
        mpf.show()

    def on_key_press(self, event, name='贵州茅台'):
        key = event.key

        if key == 'b':
            self.sell = 0
            self.buy = self.close
            self.log = "buy"
            self.t1 = self.date
        elif key == 's':
            self.sell = self.close
            self.log = "sell"
            self.t2 = self.date
            # self.profit = round(100 * (self.sell - self.buy)/self.buy, 2)
            self.all_profit += round(100 * (self.sell - self.buy) / self.buy, 2)
            log = "{}测试{},{}买入[{}],{}卖出[{}],收益{}%,总收益{}%\n" \
                .format(self.curt, self.name, self.buy, self.t1, self.sell, self.t2, self.profit, self.all_profit)
            ans = [self.curt, self.name, self.buy, self.t1, self.sell, self.t2, self.profit, self.all_profit]
            ans = [str(i) for i in ans]
            ans = ",".join(ans)
            self.profit = 0
            print(log)
            self.buy = 0
            self.file.write(ans + "\n")
        else:
            self.log = ""
            if self.buy != 0:
                self.profit = round(100 * (self.close - self.buy) / self.buy, 2)

        if key == 'enter':
            # 保存图片
            img_path = name
            plt.savefig(img_path + '.jpg')
            return

        elif key == 'left' or key == 'down':
            if self.start > 1:
                self.start = self.start - 1
        elif key == 'right' or key == 'up':
            if self.start + self.len < self.data.shape[0]:
                self.start = self.start + 1

        self.price_axe.clear()
        self.macd_axe.clear()
        self.volume_axe.clear()
        self.refresh_plot(self.data.iloc[self.start:self.start + self.len])


def get_trader_data(code, period='d', data_len=100):
    sd = StockData()
    df = sd.get_eastmoney_trade_data(code=code, period=period, fqt=0, day_num=500)
    close = df.close.values
    volume = df.volume.values
    turn = df.turn.values
    df['MA5'] = MA(close, 5)
    df['MA10'] = MA(close, 10)
    df['MA20'] = MA(close, 20)
    df['MA60'] = MA(close, 60)
    df['MA16'] = MA(close, 16)
    df['vol_avg'] = MA(volume, 5)
    df['rsi'] = RSI(close, N=6)
    df['vol_rate'] = df.apply(lambda x: x['volume'] / x['vol_avg'], axis=1)
    df['turn'] = df['turn'].astype('float')
    df['turn_avg'] = MA(turn, 5)
    df['turn_rate'] = df.apply(lambda x: x['turn'] / x['turn_avg'], axis=1)
    df['increase'] = df['increase'].astype('float')
    df['pctChg'] = df['pctChg'].astype('float')
    df['amp'] = df['amp'].astype('float')

    MA5 = MA(close, 5)
    MA10 = MA(close, 10)
    df['金叉'] = CROSS(MA5, MA10)
    df['死叉'] = CROSS(MA10, MA5)

    def judge_cross(val1, val2):
        if val1 == True:
            return "B"
        if val2 == True:
            return "S"
        return ''

    df['cross'] = df.apply(lambda x: judge_cross(x['金叉'], x['死叉']), axis=1)

    df = df.iloc[-data_len:, :]
    df = df.rename(columns={'datetime': 'date'})
    return df


"""
使用指南：
1、建议先安装依赖库，例如MyTT
2、k线图模拟买卖交易   b买 s卖    左右键移动k线
注意保存路径的更改
"""
if __name__ == "__main__":
    stock_dict = {}
    for line in open('stock_name.txt', 'r'):
        tmp = line.strip().split("\t")
        stock_dict[tmp[0]] = tmp[1]
    name = "剑桥科技"
    code = stock_dict[name]  # 若是无stock_name.txt文件 手动输入股票代码 code=603083  name=剑桥科技
    daily_data = get_trader_data(code=code, period='d',
                                 data_len=100)  # period为K线周期 15为15分线， 30 60以此类推,  data_len为选用多少天的K线
    candle = InterCandle(daily_data, name=name,
                         window_len=60)  # window_len为画图时窗口大小  注意 data_len-window_len就训练天数，例如100-60=40表示移动箭头会训练最近40天数据
    candle.plt_show()
