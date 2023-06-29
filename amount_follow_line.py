# -*- encoding=utf-8 -*-
import time
import warnings
warnings.filterwarnings('ignore')
import json
import requests
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
#plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def dt2ts(dt, format):
    return int(time.mktime(time.strptime(dt, format)))
def ts2dt(ts, format):
    return time.strftime(format, time.localtime(ts))
def get_time_dif():
    curt = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    dt = curt[:-5] + "09:30"
    hour = curt[-5:]
    end_dt = dt2ts(curt, "%Y-%m-%d %H:%M")
    if hour < "09:30" or hour > "15:00":
        begin_dt = dt2ts(dt, "%Y-%m-%d %H:%M")
        dif = 1
    elif hour <= "11:30":
        begin_dt = dt2ts(dt, "%Y-%m-%d %H:%M")
        dif = (end_dt - begin_dt) / 3600 / 4
    elif hour <= "13:00":
        begin_dt = dt2ts(dt, "%Y-%m-%d %H:%M")
        end_dt = dt2ts(curt[:-5] + "11:30", "%Y-%m-%d %H:%M")
        dif = (end_dt - begin_dt) / 3600 / 4
    elif hour < "15:00":
        dt = curt[:-5] + "13:00"
        begin_dt = dt2ts(dt, "%Y-%m-%d %H:%M")
        dif = (2 + (end_dt - begin_dt) / 3600) / 4
    return dif
class DingAlarm(object):
    # 颜色参考 https://blog.csdn.net/weixin_30340353/article/details/97490020
    def dingmessage(self, msgtype="text", content="包含关键词stock",
                    title="Top热词", isAtAll=False,
                    webhook="default"
                    ):
        if webhook == "default":
            #webhook = 'https://oapi.dingtalk.com/robot/send?access_token=2229f969f517444afdc973ec72008199ed72b29509ed29b6d08ba51ba08b4580'
            webhook = 'https://oapi.dingtalk.com/robot/send?access_token=e2b8a1b28f68f555614b4e0d228062c4d6b85176619320f0b8d5e22d79fc1eae'
        # 请求的URL，WebHook地址
        if "access_token" not in webhook:
            webhook = "https://oapi.dingtalk.com/robot/send?access_token=" + webhook
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        # default为文本
        message = {
            "msgtype": msgtype,
            "text": {"content": content},
            "at": {"isAtAll": False}  #
        }
        if msgtype == 'markdown':
            message = {
                "msgtype": msgtype, # markdown,
                "markdown": {
                    "title": title,  # title不能为空首屏展示内容
                    "text": content
                },
                "at": {
                    "isAtAll": isAtAll
                }
            }
        message_json = json.dumps(message)  # 对请求的数据进行json封装
        info = requests.post(url=webhook, data=message_json, headers=header)  # 发送请求
        # 打印返回的结果 返回日志
        #print(info.text)

    def send_dingd(self, content):
        token = "b9cc62e57820fbe20e327cbff210ad61a13945c7caf691e7165755d329d44c0b"
        self.dingmessage(content=content, webhook=token, title="成交量TOP股", msgtype="markdown")

    def coloring(self, text="", color="black"):
        color_dict = {
            'black': '#000000', '中木色': '#A68064',
            'red': '#FF0000', '橙红色': '#FF2400', '牡丹红': '#FF00FF',
            'green': '#32CD32', '黄绿色': '#99CC32', '森林绿': '#238E23',
            'blue': '#0000FF', '中蓝色': '#3232CD', '霓虹篮': '#4D4DFF', '藏青色': '#00009C', '海军蓝': '#23238E', '石板蓝': '#7F00FF',
            'yellow': '#FFFF00', '橙色': '#FF7F00', '金色': '#CD7F32', '暗金黄': '#CFB53B',
            '棕褐色': '#DB9370', '浅灰色': '#A8A8A8', '暗木色': '#855E42', '巧克力': '#5C3317',
            '土灰色': '#545454',
            '紫色': '#9932CD', '紫罗兰色': '#4F2F4F',
        }
        text = "<font color=\"{}\">{}</font>".format(color_dict[color], text)
        return text

class Plot(object):
    def __init__(self):
        pass
    def plot_top(self, names, open_price, close_price, max_price, min_price, vol_list,
                 ma5_list=[], title='TOP成交', blue_line=30, yellow_line=10,
                 save_file="", need_show=False, pct60_list=[], sort_ways='成交额'):
        """
            绘制蜡烛图
        """
        # https://blog.csdn.net/weixin_45875105/article/details/107221233
        # 方法-日期转换函数
        dates = names
        ans = []
        for i in range(len(dates)):  # X轴每个标签中插入换行符，让标签文字能竖排
            res = []
            for row in dates[i]:
                if row != " ":
                    res.append(row)
            ans.append("\n".join(res))
        dates = ans
        close_price = np.array(close_price)
        max_price = np.array(max_price)
        min_price = np.array(min_price)
        open_price = np.array(open_price)

        dates = [str(v) for v in dates]
        dates = list(dates)
        fig = plt.figure(figsize=(25, 20), dpi=80)
        # https://matplotlib.org/stable/api/axes_api.html#axis-limits
        left, width = 0.05, 0.9
        ax1 = fig.add_axes([left, 0.36, width, 0.60])  # left, bottom, width, height
        if sort_ways == "成交额":
            ax2 = fig.add_axes([left, 0.25, width, 0.11], sharex=ax1)  # 共享ax1轴
            ax3 = fig.add_axes([left, 0.15, width, 0.10], sharex=ax1)  # 共享ax1轴
        else:
            ax3 = fig.add_axes([left, 0.25, width, 0.11], sharex=ax1)  # 共享ax1轴
            ax2 = fig.add_axes([left, 0.15, width, 0.10], sharex=ax1)  # 共享ax1轴
        plt.setp(ax2.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
        plt.setp(ax1.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
        ax1.set_title(title, fontsize=20)
        ax1.set_ylabel('K\n图', fontweight='bold', fontsize=14, rotation=0)
        ax2.set_ylabel('成\n交\n额', fontweight='bold', fontsize=10, rotation=0)
        ax3.set_ylabel('60\n日\n涨\n幅', fontweight='bold', fontsize=10, rotation=0)
        ax1.tick_params(labelsize=14)
        ax2.tick_params(labelsize=10)
        ax3.tick_params(labelsize=10)
        ax1.grid(linestyle=":")  # 增加虚线
        ax2.grid(linestyle=":", b="True", axis="x")
        ax3.grid(linestyle=":", b="True", axis="x")

        # 4.判断收盘价与开盘价 确定蜡烛颜色
        colors_bool = close_price >= open_price
        colors = np.zeros(colors_bool.size, dtype="U5")
        colors[:] = "white"
        colors[colors_bool] = "white"
        for i in range(len(close_price)):
            if abs(list(close_price)[i] - 10) <= 0.3:
                colors[i] = 'r'
            elif abs(list(close_price)[i] - 20) <= 1:
                colors[i] = 'r'

        # 5.确定蜡烛边框颜色
        edge_colors = np.zeros(colors_bool.size, dtype="U1")
        edge_colors[:] = "g"
        edge_colors[colors_bool] = "r"
        line_colors = ['g'] * len(close_price)
        for i in range(len(close_price)):
            if len(ma5_list) > 0 and list(ma5_list)[i] == False:
                line_colors[i] = 'g'  # https://blog.csdn.net/u011808596/article/details/121335672
            elif colors_bool[i] == True:
                line_colors[i] = 'r'

        ax1.vlines(dates, min_price, max_price, color=line_colors)
        ax1.bar(dates, (close_price - open_price), bottom=open_price, color=colors,
                edgecolor=edge_colors, zorder=3)

        # 7.绘制蜡烛直线(最高价与最低价)
        # plt.legend()
        # plt.gcf().autofmt_xdate() ../data/east_money/top_amount/
        ax1.axhline(8, color='purple', linestyle='--')  # #FF00FF
        ax1.axhline(5, color='b', linestyle='--')
        ax1.axhline(2, color='y', linestyle='--')
        ax1.axhline(-2, color='gray', linestyle='--')

        # https://www.cnblogs.com/Gelthin2017/p/14177100.html 颜色设置参考
        colors_vol = ['#7f7f7f'] * len(close_price)
        for i in range(len(close_price)):
            if abs(list(close_price)[i] - 10) <= 0.3:
                colors_vol[i] = '#e377c2'
            elif abs(list(close_price)[i] - 20) <= 1:
                colors_vol[i] = '#e377c2'
            elif len(ma5_list) > 0 and list(ma5_list)[i] == False:
                colors_vol[i] = '#2ca02c'
            elif abs(list(close_price)[i] - list(max_price)[i]) <= 1.2:  # 上影线
                colors_vol[i] = '#1f77b4'

        colors_pct = ['r'] * len(pct60_list)
        for i in range(len(pct60_list)):
            if list(pct60_list)[i] < 0:
                colors_pct[i] = 'g'
            elif list(pct60_list)[i] < 30:
                colors_pct[i] = '#95d0fc'  # https://blog.csdn.net/u010705932/article/details/123929884
            elif list(pct60_list)[i] < 60:
                colors_pct[i] = '#1f77b4'  # blue
            elif list(pct60_list)[i] < 90:  # 上影线
                colors_pct[i] = '#ff796c'

        ax2.bar(dates, vol_list, color=colors_vol)
        ax2.axhline(blue_line, color='b', linestyle='--')
        ax2.axhline(yellow_line, color='y', linestyle='--')
        ax3.bar(dates, pct60_list, color=colors_pct)
        ax3.axhline(120, color='brown', linestyle='--')
        ax3.axhline(60, color='gray', linestyle='--')
        ax3.axhline(-10, color='gray', linestyle='--')
        curt = time.strftime("%Y-%m%d", time.localtime())
        # price_axe = plt.figure().add_axes()  # 添加价格图表 K线图
        plt.xticks(fontsize=14)
        # plt.yticks(fontsize=10)
        if len(save_file) > 0:
            loc = save_file + "{}.png".format(curt)
            plt.savefig(loc)  # 保存图片
        if need_show == True:
            plt.show()

class DealHistory(object):
    def __init__(self):
        pass

    def get_eastmoney_trade_data(self, code='515030', period=30, fqt=0, day_num=500):
        code = '1.' + code if code[0] in ['6', '5'] else '0.' + code
        # klt=103月线 klt=102周线线 klt=101日线
        if period in ['d', 'w', 'm']:
            klts = {'d': '101', 'w': '102', 'm': '103'}
            klt = klts[period]
            url = 'http://56.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112404111304433712406_1607946908499&' \
                  'secid={0}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt={1}&fqt=0&end=20500101&' \
                  'lmt={2}&_=1607946908538' \
                .format(code, klt, day_num)
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
        # print("该股票为:{},运行周期为{}".format(name, period))
        history = info['data']['klines']
        stock_values = []
        # amp为振幅 pctChg为涨幅 increase涨跌额 turn换手率
        info_head = ['code', 'name', 'date', 'open', 'close', 'high', 'low',
                     'volume', 'amount', 'amp', 'pctChg', 'increase', 'turn']

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
        df['pctChg'] = df['pctChg'].astype('float')
        df['amount'] = df['amount'].astype('float')
        df['turn'] = df['turn'].astype('float')
        # df.to_csv(name+code+".csv", index=False, encoding="gbk")
        return df

class plot_show(object):
    def __init__(self, ddf, mdf, odf, xt_bottom, xt_top, date_len=5):
        self.name_list = ddf['name'].values.tolist()
        self.pct_list = ddf['pctChg'].values.tolist()
        self.high_list = ddf['high'].values.tolist()
        self.open_list = ddf['open'].values.tolist()
        self.low_list = ddf['low'].values.tolist()
        self.close_list = ddf['close'].values.tolist()
        self.amount_list = ddf['amount'].values.tolist()
        self.date_list = [str(d)[-date_len:] for d in ddf['datetime'].values.tolist()]
        self.ma5_list = ddf['MA5'].values.tolist()
        self.ma10_list = ddf['MA10'].values.tolist()
        self.ma20_list = ddf['MA20'].values.tolist()
        self.amo_avg_list = ddf['amo_avg'].values.tolist()
        self.last_close = ddf['last_close'].values.tolist()

        self.pct_list2 = mdf['pctChg'].values.tolist()
        self.high_list2 = mdf['high'].values.tolist()
        self.open_list2 = mdf['open'].values.tolist()
        self.low_list2 = mdf['low'].values.tolist()
        self.close_list2 = mdf['close'].values.tolist()
        self.amount_list2 = mdf['amount'].values.tolist()
        self.date_list2 = [str(d)[-8:] for d in mdf['datetime'].values.tolist()]
        self.ma20_list2 = mdf['MA20'].values.tolist()
        self.ma10_list2 = mdf['MA10'].values.tolist()
        self.ma5_list2 = mdf['MA5'].values.tolist()
        self.amo_avg_list2 = mdf['amo_avg'].values.tolist()
        self.last_close2 = mdf['last_close'].values.tolist()

        self.pct_list3 = odf['pctChg'].values.tolist()
        self.high_list3 = odf['high'].values.tolist()
        self.open_list3 = odf['open'].values.tolist()
        self.low_list3 = odf['low'].values.tolist()
        self.close_list3 = odf['close'].values.tolist()
        self.amount_list3 = odf['amount'].values.tolist()
        self.date_list3 = [str(d)[-8:] for d in odf['datetime'].values.tolist()]
        self.ma20_list3 = odf['MA20'].values.tolist()

        self.close_price = np.array(self.close_list)
        self.max_price = np.array(self.high_list)
        self.min_price = np.array(self.low_list)
        self.open_price = np.array(self.open_list)

        self.close_price2 = np.array(self.close_list2)
        self.max_price2 = np.array(self.high_list2)
        self.min_price2 = np.array(self.low_list2)
        self.open_price2 = np.array(self.open_list2)

        self.close_price3 = np.array(self.close_list3)
        self.max_price3 = np.array(self.high_list3)
        self.min_price3 = np.array(self.low_list3)
        self.open_price3 = np.array(self.open_list3)

        self.dates = self.date_list
        self.dates2 = self.date_list2
        self.dates3 = self.date_list3

        self.xt_bottom = xt_bottom
        self.xt_top = xt_top


    def set_colors(self, colors_bool, close, high, pct, low, open, last_close, thr=0.1):
        colors = np.zeros(colors_bool.size, dtype="U5")
        colors[:] = "white"
        colors[colors_bool] = "white"
        for i in range(len(close)):
            max_pct = 100*(high[i]-last_close[i])/last_close[i]
            min_pct = 100*(low[i] - last_close[i]) / last_close[i]
            if max_pct - pct[i] < thr * 2 and pct[i] > 0 and pct[i] - min_pct >= 2*thr:
                colors[i] = 'r'
            elif pct[i] - min_pct <= 1.5 * thr and max_pct - pct[i] > 2*thr and close[i] < open[i]:
                colors[i] = 'g'
            elif pct[i] < -5:
                colors[i] = 'g'

        return colors

    def set_ege_colors(self, colors_bool, close, ma5):
        edge_colors = np.zeros(colors_bool.size, dtype="U1")
        edge_colors[:] = "g"
        edge_colors[colors_bool] = "r"
        line_colors = ['g'] * len(close)
        for i in range(len(close)):
            if len(ma5) > 0 and ma5[i] > close[i]:
                line_colors[i] = 'g'  # https://blog.csdn.net/u011808596/article/details/121335672
            elif colors_bool[i] == True:
                line_colors[i] = 'r'
        return edge_colors, line_colors

    def set_vol_colors(self, close, amount, avg_amount, pct):
        # https://www.cnblogs.com/Gelthin2017/p/14177100.html 颜色设置参考
        colors_vol = ['#1f77b4'] * len(close)
        for i in range(len(close)):
            if pct[i] > 8:
                colors_vol[i] = '#e377c2'
            elif amount[i] > avg_amount[i] * 1.2 and i >4 and amount[i] >= amount[i-1]:
                colors_vol[i] = '#8c564b'

        return colors_vol


    def plot_long(self):
        fig = plt.figure(figsize=(25, 20), dpi=80)
        ax1 = fig.add_axes([0.05, 0.30, 0.9, 0.65])  # left, bottom, width, height
        ax2 = fig.add_axes([0.05, 0.10, 0.9, 0.20], sharex=ax1)  # 共享ax1轴
        title = "{} {}/{}%".format(self.name_list[-1], self.close_list[-1], self.pct_list[-1])
        ax1.set_title(title, fontsize=20)
        # ax1.set_ylabel('Price', fontweight='bold', fontsize=14, rotation=0)
        ax1.tick_params(labelsize=14)
        ax2.tick_params(labelsize=11)
        ax1.grid(linestyle=":")  # 增加虚线
        ax2.grid(linestyle=":", b="True", axis="x")

        colors_bool = self.close_price >= self.open_price
        colors = self.set_colors(colors_bool=colors_bool, close=self.close_list, high=self.high_list,
                                 low=self.low_list, open=self.open_list, last_close=self.last_close, pct=self.pct_list,
                                 thr=0.75)
        edge_colors, line_colors = self.set_ege_colors(colors_bool=colors_bool, close=self.close_list,
                                                       ma5=self.ma5_list)

        ax1.vlines(self.dates, self.min_price, self.max_price, color=line_colors)
        ax1.bar(self.dates, (self.close_price - self.open_price), bottom=self.open_price, color=colors,
                edgecolor=edge_colors, zorder=3)
        ax1.plot(self.dates, self.ma5_list, label='MA5', c='b')
        ax1.plot(self.dates, self.ma10_list, label='MA10', c='y')
        ax1.plot(self.dates, self.ma20_list, label='MA20', c='c')
        ax1.axhline(self.close_list[-1], color='b', linestyle=':')
        if self.xt_top > 0:
            ax1.axhline(self.xt_top, color='olive', linestyle='--')
        if self.xt_bottom > 0:
            ax1.axhline(self.xt_bottom, color='y', linestyle='--')


        for x, y in zip(self.date_list, self.amount_list):
            ax2.text(x, y, y, ha='center', va='bottom', fontsize=9)

        yr = min(self.low_list)-0.4* (min(self.low_list)//10)
        y1 = yr
        idx = 0
        for x, y in zip(self.date_list, self.pct_list):
            idx += 1
            fontsize = 8
            if idx % 2 == 1:
                fontsize = 7
            if y > 0:
                ax1.text(x, y1, str(y), ha='center', va='bottom', fontsize=fontsize, c='r')
            else:
                ax1.text(x, y1, str(y), ha='center', va='bottom', fontsize=fontsize, c='g')

        max_indx = self.high_list.index(max(self.high_list))
        ax1.annotate(self.high_list[max_indx], xytext=(self.dates[max_indx], self.high_list[max_indx]),
                     xy=(self.dates[max_indx], self.high_list[max_indx]), fontsize=14)
        min_indx = self.low_list.index(min(self.low_list))
        ax1.annotate(self.low_list[min_indx], xytext=(self.dates[min_indx], self.low_list[min_indx]),
                     xy=(self.dates[min_indx], self.low_list[min_indx]), fontsize=14)


        colors_vol = self.set_vol_colors(close=self.close_list, amount=self.amount_list, avg_amount=self.amo_avg_list, pct=self.pct_list)
        ax2.bar(self.dates, self.amount_list, color=colors_vol)
        ax2.plot(self.dates, self.amo_avg_list, c='g')
        ax2.axhline(sum(self.amount_list[-10:]) / 10, color='coral', linestyle=':')

        ax2.set_xticklabels(self.dates, rotation=45)
        curt = time.strftime("%Y-%m%d", time.localtime())
        # price_axe = plt.figure().add_axes()  # 添加价格图表 K线图
        plt.xticks(fontsize=10, rotation=45)

        plt.show()

    def plot_view(self):
        # https://matplotlib.org/stable/api/axes_api.html#axis-limits
        fig = plt.figure(figsize=(25, 20), dpi=80)
        left1, width1 = 0.03, 0.47
        left2, width2 = 0.53, 0.44
        ax1 = fig.add_axes([left1, 0.30, width1, 0.65])  # left, bottom, width, height
        ax2 = fig.add_axes([left1, 0.10, width1, 0.20], sharex=ax1)  # 共享ax1轴
        ax3 = fig.add_axes([left2, 0.30, width2, 0.65])  # 共享ax1轴
        # ax4 = fig.add_axes([left2, 0.25, width2, 0.10],sharex=ax3)  # 共享ax1轴
        ax5 = fig.add_axes([left2, 0.20, width2, 0.10])  # 共享ax1轴
        ax4 = fig.add_axes([left2, 0.10, width2, 0.10], sharex=ax3)  # 共享ax1轴
        # plt.setp(ax4.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
        plt.setp(ax5.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
        title = "{} {}/{}%".format(self.name_list[-1],self.close_list[-1], self.pct_list[-1])
        ax1.set_title(title, fontsize=20)
        #ax1.set_ylabel('Price', fontweight='bold', fontsize=14, rotation=0)
        ax1.tick_params(labelsize=14)
        ax2.tick_params(labelsize=11)
        ax1.grid(linestyle=":")  # 增加虚线
        ax2.grid(linestyle=":", b="True", axis="x")

        ax3.set_title('30分线', fontsize=20)
        ax3.tick_params(labelsize=11)
        ax4.tick_params(labelsize=11)
        ax5.tick_params(labelsize=11)
        ax3.grid(linestyle=":")  # 增加虚线
        ax4.grid(linestyle=":", b="True", axis="x")
        ax5.grid(linestyle=":", b="True", axis="x")

        # 4.判断收盘价与开盘价 确定蜡烛颜色
        colors_bool = self.close_price >= self. open_price
        colors = self.set_colors(colors_bool=colors_bool, close=self.close_list, high=self.high_list,
                                 low=self.low_list, open=self.open_list,last_close=self.last_close, pct=self.pct_list,thr=0.75)
        edge_colors, line_colors = self.set_ege_colors(colors_bool=colors_bool, close=self.close_list, ma5=self.ma5_list)


        ax1.vlines(self.dates, self.min_price, self.max_price, color=line_colors)
        ax1.bar(self.dates, (self.close_price - self.open_price), bottom=self.open_price, color=colors,
                edgecolor=edge_colors, zorder=3)
        ax1.plot(self.dates, self.ma5_list, label='MA5', c='b')
        ax1.plot(self.dates, self.ma10_list, label='MA10', c='y')
        ax1.plot(self.dates, self.ma20_list, label='MA20', c='c')
        ax1.axhline(self.close_list[-1], color='b', linestyle=':')
        ax3.axhline(self.close_list[-1], color='b', linestyle=':')

        colors_bool2 = self.close_price2 >= self.open_price2
        colors2 = self.set_colors(colors_bool=colors_bool2, close=self.close_list2, high=self.high_list2,
                                  low=self.low_list2, open=self.open_list2,last_close=self.last_close2, pct=self.pct_list2,thr=0.1)
        edge_colors2, line_colors2 = self.set_ege_colors(colors_bool=colors_bool2, close=self.close_list2,
                                                       ma5=self.ma5_list2)

        ax3.vlines(self.dates2, self.min_price2, self.max_price2, color=line_colors2)
        ax3.bar(self.dates2, (self.close_price2 - self.open_price2), bottom=self.open_price2, color=colors2,
                edgecolor=edge_colors2, zorder=3)
        ax3.plot(self.dates2, self.ma5_list2, label='MA5', c='b')
        ax3.plot(self.dates2, self.ma10_list2, label='MA10', c='y')
        ax3.plot(self.dates2, self.ma20_list2, label='MA20', c='c')

        ax2.axhline(sum(self.amount_list[-10:])/10, color='coral', linestyle=':')
        ax4.axhline(sum(self.amount_list2[-10:]) / 10, color='coral', linestyle=':')
        ax3.axhline(self.last_close[-1], color='gray', linestyle=':')
        ax5.axhline(self.last_close[-1], color='gray', linestyle=':')
        ax5.plot(self.ma20_list3, label='MA20', c='c', linestyle='--')
        ax5.plot(self.close_price3, label='Close', c='b')
        # ax5.vlines(dates3, min_price3, max_price3)
        # ax5.bar(dates3, (close_price3 - open_price3), bottom=open_price3)

        # https://www.cnblogs.com/Gelthin2017/p/14177100.html 颜色设置参考

        for x, y in zip(self.date_list, self.amount_list):
            ax2.text(x, y, y, ha='center', va='bottom', fontsize=11)

        y1 = min(self.low_list)-0.1* (min(self.low_list)//10)
        for x, y in zip(self.date_list, self.pct_list):
            if y > 0:
                ax1.text(x, y1, str(y), ha='center', va='bottom', fontsize=9, c='r')
            else:
                ax1.text(x, y1, str(y), ha='center', va='bottom', fontsize=9, c='g')

        max_indx = self.high_list.index(max(self.high_list))
        ax1.annotate(self.high_list[max_indx], xytext=(self.dates[max_indx], self.high_list[max_indx]),
                     xy=(self.dates[max_indx], self.high_list[max_indx]), fontsize=14)
        min_indx = self.low_list.index(min(self.low_list))
        ax1.annotate(self.low_list[min_indx], xytext=(self.dates[min_indx], self.low_list[min_indx]),
                     xy=(self.dates[min_indx], self.low_list[min_indx]), fontsize=14)

        if self.xt_top > 0:
            ax1.axhline(self.xt_top, color='olive', linestyle='--')
        if self.xt_bottom > 0:
            ax1.axhline(self.xt_bottom, color='y', linestyle='--')

        max_indx = self.high_list2.index(max(self.high_list2))
        ax3.annotate(self.high_list2[max_indx], xytext=(self.dates2[max_indx], self.high_list2[max_indx]),
                     xy=(self.dates2[max_indx], self.high_list2[max_indx]), fontsize=14)
        min_indx = self.low_list2.index(min(self.low_list2))
        ax3.annotate(self.low_list2[min_indx], xytext=(self.dates2[min_indx], self.low_list2[min_indx]),
                     xy=(self.dates2[min_indx], self.low_list2[min_indx]), fontsize=14)

        colors_vol = self.set_vol_colors(close=self.close_list, amount=self.amount_list, avg_amount=self.amo_avg_list, pct=self.pct_list)
        ax2.bar(self.dates, self.amount_list, color=colors_vol)
        ax2.plot(self.dates, self.amo_avg_list, c='g')

        colors_vol2 = self.set_vol_colors(close=self.close_list2, amount=self.amount_list2, avg_amount=self.amo_avg_list2,
                                         pct=self.pct_list2)

        ax4.bar(self.dates2, self.amount_list2, color=colors_vol2)
        ax4.plot(self.dates2, self.amo_avg_list2, c='g')
        for x, y in zip(self.date_list2, self.amount_list2):
            ax4.text(x, y, y, ha='center', va='bottom', fontsize=11)

        ax2.set_xticklabels(self.dates, rotation=45)
        curt = time.strftime("%Y-%m%d", time.localtime())
        # price_axe = plt.figure().add_axes()  # 添加价格图表 K线图
        plt.xticks(fontsize=10, rotation=45)

        plt.show()

def get_xt_val(df, key, val=0, dt="", num = 10, is_bottom=True):
    if val != 0:
        return val
    if dt == "-1":
        return 0
    ds = df['datetime'].values.tolist()[-num:]
    high = df['high'].values.tolist()[-num:]
    low = df['low'].values.tolist()[-num:]
    close = df['close'].values.tolist()
    if is_bottom == True:
        dt = ds[low.index(min(low))]
    else:
        dt = ds[high.index(max(high))]
    df = df[(df['datetime'] == dt)]

    val = df[key].values.tolist()[-1]
    return val

def run_amount_plot(is_follow=False,params_config={}, save_file="", page=1, max_num=6000):
    #ut = Utils()
    params = {"sort_ways": "成交额",
               "maxn": 100, "vol_max": 150, "vol_min": 5,
               "pct_limit": -2,
               'blue_line': 30, 'yellow_line': 10,
               "need_show": False,
               "need_send": False,
               "need_ma5": True,
               "need_minute": False,
               'filter_high': True,
              'filter_green':True
               }
    for k, v in params_config.items():
        if k in params:
            params[k] = params_config[k]
    url1 = "https://66.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402589714281201181_1679376147293&" \
           "pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=%7C0%7C0%7C0%7Cweb&" \
           "fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048".format(page, max_num)
    url2 = "https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery1123017213004353442263_1687356361420&fid=f62&" \
           "po=1&pz={}&pn=1&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2" \
           "Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2".format(max_num)

    if is_follow == False:
        url = url1
        html = requests.get(url)
        info = html.text[42:-2]
    else:
        url = url2
        html = requests.get(url)
        info = html.text[43:-2]
    info = json.loads(info)
    info_list = info['data']['diff']
    data_list = []
    for row in info_list:
        ans = []
        for i in range(1, 30):
            if i in [11, 27, 28, 29]:
                continue
            key = "f{}".format(i)
            if key in row:
                ans.append(row[key])
        data_list.append(ans)
    cols = ['序号', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '换手率',
            '市盈率-动态', '量比', '代码', '涨速', '名称',
            '最高', '最低', '今开', '昨收', '未知', '总市值',
            '流通市值', '5分钟涨跌', '市净率', '60日涨跌幅', '年初至今涨跌幅', '上市日期'
            ]
    df = pd.DataFrame(data_list, columns=cols)
    stock_df = df

    df = df.drop(labels=['未知'], axis=1)
    df = df[(df['涨跌幅'] != "-") & (df['成交额'] != "-")]

    df['涨跌幅'] = df['涨跌幅'].astype('float')
    df['成交额'] = df['成交额'].astype('float')
    if params['sort_ways'] == "成交额":
        df = df.sort_values(by=['成交额', '涨跌幅'], ascending=[False, False])
    else:
        df = df.sort_values(by=[params['sort_ways'], '涨跌幅'], ascending=[False, False])
    df['成交额'] = df.apply(lambda x: round(x['成交额'] / 10000 / 10000, 1), axis=1)
    df = df[(df['成交额'] <= params['vol_max'])]
    up_num = 0
    for s in df['涨跌幅'].values.tolist()[:params['maxn']]:
        if s > 0: up_num += 1
    print("在今日TOP{}中上涨个数为{},占比{}%".format(params['maxn'], up_num, round(100*up_num/params['maxn'],2)))

    title = params['sort_ways']
    if params['sort_ways'] == "60日涨跌幅":
        df = df[(df['成交额'] >= 5)]
    else:
        df = df[(df['成交额'] >= 2)]
        if params['filter_green'] == True:
            df = df[(df['今开'] < df['最新价'])]

    df = df.iloc[:params['maxn'], :]
    up_num = 0
    pct_list = df['涨跌幅'].values.tolist()
    for s in pct_list:
        if s > 0: up_num += 1
    print("开盘为正的股票，在TOP{}中上涨个数为{},占比{}%".format(params['maxn'], up_num, round(100*up_num/params['maxn'], 2)))
    # 过滤
    df = df[(df['总市值'] < 10000*10000*8000)] # 市值小于8000亿
    df = df[(df['涨跌幅'] > params['pct_limit'])]
    df = df[(df['涨跌幅'] <= 20)]
    if params['filter_high'] == True:
        df = df[(df['涨跌幅'] <= 18)]
    df = df.iloc[:50, :]
    if is_follow == True:
        return stock_df
    if params['filter_green'] == True:
        print("剔除低开&市值超过8000亿的TOP{}".format(len(df['代码'].values.tolist())))
    else:
        print("剔除市值超过8000亿的TOP{}".format(len(df['代码'].values.tolist())))
    return df

def main(name, code, params={}, need_plot=False):
    dh = DealHistory()
    period = 'd'
    date_len = 5
    if params['long_way'] == 1:
        period = params['period']
    if period != 'd':
        date_len = 8
    ddf = dh.get_eastmoney_trade_data(code=code, period=period)
    mdf = dh.get_eastmoney_trade_data(code=code, period='30')
    odf = dh.get_eastmoney_trade_data(code=code, period='1')
    ddf['amount'] = ddf.apply(lambda x: round(x['amount'] / 10000 / 10000, 1), axis=1)
    ddf['last_close'] = ddf['close'].shift(1)
    ddf['MA5'] = ddf.close.rolling(window=5).mean()
    ddf['MA10'] = ddf.close.rolling(window=10).mean()
    ddf['MA20'] = ddf.close.rolling(window=20).mean()
    ddf['amo_avg'] = ddf.amount.rolling(window=5).mean()
    mdf['amount'] = mdf.apply(lambda x: round(x['amount'] / 10000 / 10000, 1), axis=1)
    mdf['last_close'] = mdf['close'].shift(1)
    mdf['MA20'] = mdf.close.rolling(window=20).mean()
    mdf['MA10'] = mdf.close.rolling(window=10).mean()
    mdf['MA5'] = mdf.close.rolling(window=5).mean()
    mdf['amo_avg'] = mdf.amount.rolling(window=5).mean()
    odf['MA20'] = odf.close.rolling(window=20).mean()
    # save_file若是不设置则默认不保存 need_show=True才画图  need_minute=True才会画30分钟K线
    start_date = ""
    maxn = 25
    if params['long_way'] == 1:
        maxn = 60
    ddf = ddf.iloc[-maxn:, :]
    mdf = mdf.iloc[-maxn:, :]

    xt_bottom = get_xt_val(ddf, 'close',  dt="", num=10, is_bottom=True) # 箱体底部
    xt_top = get_xt_val(ddf, 'close',  dt="", num=10, is_bottom=False)  # 箱体顶部
    amount_list = ddf['amount'].values.tolist()
    close_list = ddf['close'].values.tolist()
    lastest_60 = close_list[-60]
    bias_lastest_60 = round(100 * (close_list[-1] - lastest_60) / lastest_60, 2)
    lastest_20 = close_list[-20]
    bias_lastest_20 = round(100 * (close_list[-1] - lastest_20) / lastest_20, 2)
    high_list = ddf['high'].values.tolist()
    highest = max(high_list[-5:])
    pct_list = ddf['pctChg'].values.tolist()
    # 30分中轨线
    min_ma20 = round(mdf['MA20'].values.tolist()[-1],2)
    min_bias_20 = round(100 * (close_list[-1] - min_ma20) / min_ma20, 2)
    bias_highest = round(100 * (close_list[-1] - highest) / highest, 2)
    # 日线
    avg10 = round(sum(amount_list[-10:]) / 10, 1)
    avg5 = round(sum(amount_list[-5:]) / 5,1)
    dif1 = round(100 * (close_list[-1] - xt_top) / xt_top, 2)
    dif2 = round(100 * (close_list[-1] - xt_bottom) / xt_bottom, 2)
    ma5 = round(sum(close_list[-5:])/5, 2)
    ma10 = round(sum(close_list[-10:])/10, 2)
    bias_5 = round(100*(close_list[-1]-ma5)/ma5, 2)
    bias_10 = round(100 * (close_list[-1] - ma10) / ma10, 2)
    if dif1 > 0:
        dif1 = "+{}".format(dif1)
    if dif2 > 0:
        dif2 = "+{}".format(dif2)
    r2 = ""
    r3, r4 = "", ""
    if min_bias_20 < 0 and bias_10 < 0:
        r4 = "跌破30分中轨，破10日线，应该清仓"
    elif min_bias_20 < 0 and bias_5 < 0:
        r4 = "跌破30分中轨，破5日线，该止盈"
    elif min_bias_20 < 0:
        r4 = "跌破30分中轨，该减仓"
    elif pct_list[-1] > 0 and min_bias_20 > 0:
        r4 = "突破30分中轨"
    elif bias_highest < -5 and min_bias_20 < 0:
        r4 = "跌中轨&最高点下来超过5%，该减仓"
    elif bias_highest < -5 and pct_list[-1] < 0:
        r4 = "下跌行情，最高点下来超过5%，该减仓"
    elif bias_highest < -5:
        r4 = "上涨，但最高点下来超过5%，当心"
    elif pct_list[-1] > 0 and min_bias_20 > 0 and bias_5 >0:
        r4 = "突破30分中轨,5日线上"
    elif pct_list[-1] > 0 and min_bias_20 > 0 and bias_10 >0:
        r4 = "突破中轨,10日线上"
    elif bias_10 < 0:
        r4 = "跌破10日生命线，应清仓"
    elif bias_5 < 0:
        r4 = "跌破5日强势线"


    if bias_10 < 0:
        r2 = "跌破10日生命线"
    elif bias_5 < 0:
        r2 = "跌破5日强势线"

    if ddf['close'].values.tolist()[-1] < xt_bottom:
        r3 = "|跌破箱体，清仓离去"
    elif ddf['close'].values.tolist()[-1] > xt_top:
        r3= "|突破箱体，考虑加仓"

    content = ""
    content += "{}股价{}[{}%],30分中轨{}[{}%]。MA5为{}[{}%],MA10为{}[{}%]\n 近五日最高{}[{}%],近10日箱顶{}[{}%],箱底{}[{}%],{}{}".\
        format(name, close_list[-1], pct_list[-1],
               min_ma20, min_bias_20,
               ma5, bias_5,
               ma10, bias_10,
               highest,bias_highest,
               xt_top, dif1,
               xt_bottom, dif2,
               r4, r3)
    cur_amount = amount_list[-1]

    time_dif = get_time_dif()
    pred_amount = round(cur_amount/time_dif, 1)
    last_amount = amount_list[-2]
    pred_dif = round(100*(pred_amount-last_amount)/last_amount,2)
    dif10 = round(100*(pred_amount-avg10)/avg10, 2)
    dif5 = round(100*(pred_amount-avg5)/avg5, 2)

    r1 = ""
    if pred_dif < -20:
        r1 = ",缩量考虑减仓"
    content += "\n "
    content += "今日成交{}亿,预估成交{}亿[{}%],昨日成交{}亿;ma5为{}亿[{}%],ma10为{}亿[{}%]{}"\
        .format(cur_amount, pred_amount,
                pred_dif, last_amount,
                avg5, dif5,
                avg10, dif10,
                r1)

    data_list = [name, close_list[-1], "{}%".format(pct_list[-1]),
                 min_ma20, "{}%".format(min_bias_20),
                 cur_amount, avg5, "{}%".format(dif5) ,
                 ma5, "{}%".format(bias_5),
                 ma10, "{}%".format(bias_10),
                 highest,"{}%".format(bias_highest),
                 r4,
                 pred_amount, "{}%".format(pred_dif),
                 avg10, "{}%".format(dif10),
                 "{}%".format(bias_lastest_60),
                 "{}%".format(bias_lastest_20),
                 xt_top, dif1,
                 xt_bottom, dif2, r1
                 ]

    #print("今日成交额{}亿,近5日平均成交额{}亿,对比{}%".format(cur_amount, avg5, dif5))
    #print("今日成交额{}亿,近10日平均成交额{}亿,对比{}%".format(cur_amount, avg10, dif10))


    if need_plot == True:
        #xt_top = 34.1, 39.1
        plo = plot_show(ddf, mdf, odf, xt_bottom=xt_bottom, xt_top=xt_top, date_len=date_len)
        if params['long_way'] == 1:
            plo.plot_long()
        else:
            plo.plot_view()

    return content, data_list

# https://www.cnblogs.com/Gelthin2017/p/14177100.html 颜色设置参考
# https://blog.csdn.net/u010705932/article/details/123929884

def run(name_list, code_list):
    data_set = []
    all_infos = ""
    for i in range(len(name_list)):
        stock = name_list[i]
        code = code_list[i]
        content, data_list = main(name=stock, code=code, params={'long_way': 1, 'period': 'd'}, need_plot=False) # 选择成交量还是近60天的涨幅
        all_infos += "{}.{}\n\n".format(i+1, content)
        data_set.append(data_list)

    info_head = ['名称','股价','涨幅',
                 '30分中轨','偏离中轨',
                 '成交额', '五日均额', '偏离五均额',
                 'MA5','偏离MA5',
                 'MA10', '偏离MA10',
                 '5日峰价', '偏离最高',
                 '说明',
                 '预估成交', '对比昨日',
                 '十日均额', '偏离十均额',
                 '近60日涨幅','近20日涨幅',
                 '箱顶','btop','箱底', 'bbo','备注']

    dateset = pd.DataFrame(data_set, columns=info_head)
    return all_infos, dateset
    #print("同花顺手机版热榜https://eq.10jqka.com.cn/frontend/thsTopRank/index.html?client_userid=ygEVW&back_source=wxhy&share_hxapp=isc#/")
    #print("东财概念涨幅榜http://quote.eastmoney.com/center/boardlist.html#concept_board")

def main_fun(follow_list, is_follow=True):

    follow_list = list(set(follow_list))
    # 获取大盘top成交
    sdf = run_amount_plot(is_follow=is_follow)
    name_list = sdf['名称'].values.tolist()
    code_list = sdf['代码'].values.tolist()
    if is_follow == True and len(follow_list) > 0:
        # 分析指定股票成交额情况
        code_list_ = []
        for name in follow_list:
            if name in name_list:
                code_list_.append(code_list[name_list.index(name)])
            else:
                code_list_.append('000001')
        all_infos, dateset = run(name_list=follow_list, code_list=code_list_)
    else:
        # 分析大盘top80成交额股票情况
        all_infos, dateset = run(name_list=name_list, code_list=code_list)
    print("不止损的后果历历在目，既要经受亏损，还占用仓位！")
    print("成本即为最高价！！")
    print("跌破30分中轨立刻减仓，下跌不言底！！！")
    print(all_infos)
    #dateset['mv_signal'] = dateset.apply(lambda x: '{}%'.format(x), axis=1)
    dateset = dateset.sort_values(by="成交额", ascending=False)
    dateset.to_csv("top_amount_analysis.csv", index=False)

"""
关注股票的实时行情数据

"""
if __name__ == "__main__":

    follow_list = ['剑桥科技', '浪潮信息','华工科技','机器人', '中科曙光',
                   '工业富联', '深科技', '拓维信息','昆仑万维', '蓝色光标',
                   '科大讯飞', '景嘉微', '三七互娱', '金桥信息', '中国科传',
                   '拓尔思','万兴科技','中文在线', '沪电股份', '易华录',
                   '紫光股份'
                   ]

    #main_fun(follow_list, is_follow=True) # is_follow = True运行的follow_list中股票，否则是top成交50
    main_fun(follow_list, is_follow=False)  # is_follow = True运行的follow_list中股票，否则是top成交50
