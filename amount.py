# -*- encoding=utf-8 -*-
import time
import warnings
warnings.filterwarnings('ignore')
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

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

def add_url(code):
    if code[0] == '6':
        return "https://xueqiu.com/S/SH" + code
    return "https://xueqiu.com/S/SZ" + code

def cal_rate(x, y):
    return round(100 * (x - y) / y, 2)

def get_eastmoney_trade_data(code='515030', period=30, fqt=0, day_num=500):
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

def get_ma5_data(df):
    code_list = df['代码'].values.tolist()
    ma5_list = []
    for code in code_list:
        mdf = get_eastmoney_trade_data(code=code, period='d', day_num=50)
        mdf['MA5'] = mdf['close'].rolling(5).mean()
        if mdf['MA5'].values.tolist()[-1] < mdf['close'].values.tolist()[-1]:
            ma5_list.append(True)
        else:
            ma5_list.append(False)

    return ma5_list

def plot_30_min(df, need_show=False,save_file=""):
    sdf = pd.DataFrame()
    name_list = df['名称'].values.tolist()
    code_list = df['代码'].values.tolist()
    for code in code_list:
        pdf = get_eastmoney_trade_data(code=code)
        pdf['last_close'] = pdf['close'].shift(1)
        pdf['max_rate'] = pdf.apply(lambda x: cal_rate(x['high'], x['last_close']), axis=1)
        pdf['min_rate'] = pdf.apply(lambda x: cal_rate(x['low'], x['last_close']), axis=1)
        pdf['open_rate'] = pdf.apply(lambda x: cal_rate(x['open'], x['last_close']), axis=1)
        pdf['MA5'] = pdf.close.rolling(window=5).mean()
        pdf = pdf.iloc[-1:, :]
        sdf = pd.concat([sdf, pdf])
    name_list = sdf['name'].values.tolist()
    close_rate = sdf['pctChg'].values.tolist()
    max_rate = sdf['max_rate'].values.tolist()
    min_rate = sdf['min_rate'].values.tolist()
    open_rate = sdf['open_rate'].values.tolist()
    df['成交额'] = df.apply(lambda x: round(x['成交额'] / 10000 / 10000, 1), axis=1)
    vol_list = df['成交额'].values.tolist()
    plot_top(name_list, open_rate,close_rate, max_rate, min_rate,vol_list,
             ma5_list=[], save_file=save_file,need_show=False)
    print(" 30 minute plot success ")

def plot_top(names, open_price,close_price,max_price,min_price,vol_list,
             ma5_list=[], title='TOP成交',blue_line=30, yellow_line=10,
             save_file="", need_show=False):
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
    fig = plt.figure(figsize=(25, 10), dpi=80)

    left, width = 0.05, 0.9
    ax1 = fig.add_axes([left, 0.25, width, 0.70])  # left, bottom, width, height
    ax2 = fig.add_axes([left, 0.10, width, 0.15], sharex=ax1)  # 共享ax1轴
    #plt.setp(ax1.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    #plt.setp(ax2.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    ax1.set_title(title)
    ax1.title.set_size(20)

    ax1.tick_params(labelsize=12)
    ax1.grid(linestyle=":")

    # 4.判断收盘价与开盘价 确定蜡烛颜色
    colors_bool = close_price >= open_price
    colors = np.zeros(colors_bool.size, dtype="U5")
    colors[:] = "white"
    colors[colors_bool] = "white"
    for i in range(len(close_price)):
        if abs(list(close_price)[i]-10) <= 0.3:
            colors[i] = 'r'
        if abs(list(close_price)[i]-20) <= 1:
            colors[i] = 'r'

    # 5.确定蜡烛边框颜色
    edge_colors = np.zeros(colors_bool.size, dtype="U1")
    edge_colors[:] = "g"
    edge_colors[colors_bool] = "r"
    # 6.绘制蜡烛
    ax1.vlines(dates, min_price, max_price, color=edge_colors)
    ax1.bar(dates, (close_price - open_price), 0.8, bottom=open_price, color=colors,
            edgecolor=edge_colors, zorder=3)

    # 7.绘制蜡烛直线(最高价与最低价)
    # plt.legend()
    # plt.gcf().autofmt_xdate() ../data/east_money/top_amount/
    ax1.axhline(8, color='purple', linestyle='--')  # #FF00FF
    ax1.axhline(5, color='b', linestyle='--')
    ax1.axhline(2, color='y', linestyle='--')

    # https://www.cnblogs.com/Gelthin2017/p/14177100.html 颜色设置参考
    colors_vol = ['#7f7f7f'] * len(close_price)
    for i in range(len(close_price)):
        if abs(list(close_price)[i] - 10) <= 0.3:
            colors_vol[i] = '#e377c2'
        elif abs(list(close_price)[i] - 20) <= 1:
            colors_vol[i] = '#e377c2'
        elif len(ma5_list) > 0 and list(ma5_list)[i] == False:
            colors_vol[i] = '#2ca02c'
        elif abs(list(close_price)[i] - list(max_price)[i]) <= 1.2:
            colors_vol[i] = '#1f77b4'

    ax2.bar(dates, vol_list, color=colors_vol)
    ax2.axhline(blue_line, color='b', linestyle='--')
    ax2.axhline(yellow_line, color='y', linestyle='--')
    curt = time.strftime("%Y-%m%d", time.localtime())
    #price_axe = plt.figure().add_axes()  # 添加价格图表 K线图
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if len(save_file) > 0:
        loc = save_file + "{}.png".format(curt)
        plt.savefig(loc)  # 保存图片
    if need_show == True:
        plt.show()

def run_amount_plot(params={}, save_file="", page=1, max_num=5000):
    if len(params) < 1:
        params = {"sort_ways": "成交额",
                   "maxn": 100, "vol_max": 150, "vol_min": 5,
                   "pct_limit": -2,
                   'blue_line': 30, 'yellow_line': 10,
                   "need_show": False,
                   "need_send": False,
                   "need_ma5": True,
                   "need_minute": False,
                   'filter_high': True
                   }
    url = "https://66.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402589714281201181_1679376147293&pn={}&pz={}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=%7C0%7C0%7C0%7Cweb&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048".format(
        page, max_num)
    html = requests.get(url)
    #print(url)
    info = html.text[42:-2]
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

    df = df.drop(labels=['未知'], axis=1)
    df = df[(df['涨跌幅'] != "-") & (df['成交额'] != "-")]

    df['涨跌幅'] = df['涨跌幅'].astype('float')
    df['成交额'] = df['成交额'].astype('float')
    if params['sort_ways'] == "成交额":
        df = df.sort_values(by=['成交额', '涨跌幅'], ascending=[False, False])
    else:
        df = df.sort_values(by=[params['sort_ways'], '涨跌幅'], ascending=[False, False])

    df['max_rate'] = df.apply(lambda x: cal_rate(x['最高'], x['昨收']), axis=1)
    df['min_rate'] = df.apply(lambda x: cal_rate(x['最低'], x['昨收']), axis=1)
    df['open_rate'] = df.apply(lambda x: cal_rate(x['今开'], x['昨收']), axis=1)
    df['成交额'] = df.apply(lambda x: round(x['成交额'] / 10000 / 10000, 1), axis=1)
    df = df[(df['成交额'] <= params['vol_max'])]
    title = params['sort_ways']
    df = df.iloc[:params['maxn'], :]
    up_num = 0
    pct_list = df['涨跌幅'].values.tolist()
    for s in pct_list:
        if s > 0: up_num += 1
    print("统计TOP{},上涨个数为{},占比{}%".format(params['maxn'], up_num, round(100*up_num/params['maxn'],2)))
    # 过滤
    df = df[(df['总市值'] < 10000*10000*8000)]
    df = df[(df['涨跌幅'] > params['pct_limit'])]  # 市值小于9000亿
    df = df[(df['涨跌幅'] <= 20)]
    if params['filter_high'] == True:
        df = df[(df['涨跌幅'] <= 17)] # 市值小于9000亿


    if params['sort_ways'] == "60日涨跌幅":
        df = df[(df['成交额'] >= 5)]
    else:
        df = df[(df['今开'] < df['最新价'])]

    name_list = df['名称'].values.tolist()
    close_rate = df['涨跌幅'].values.tolist()
    max_rate = df['max_rate'].values.tolist()
    min_rate = df['min_rate'].values.tolist()
    open_rate = df['open_rate'].values.tolist()
    vol_list = df['成交额'].values.tolist()
    if params['sort_ways'] == "60日涨跌幅":
        vol_list = df['60日涨跌幅'].values.tolist()
    ma5_list = []
    if params['need_ma5']  == True:
        ma5_list = get_ma5_data(df)
    plot_top(name_list, open_rate, close_rate, max_rate, min_rate, vol_list,
             ma5_list=ma5_list, save_file=save_file, need_show=params['need_show'], title=title,
             blue_line=params['blue_line'], yellow_line=params['yellow_line'])
    print(" top amount plot success ")
    if params['need_minute'] == True:
        plot_30_min(df, save_file="./top_amount/30_minute", need_show=False)
    return df

def run_test(params={}):
    # save_file若是不设置则默认不保存 need_show=True才画图  need_minute=True才会画30分钟K线
    df = run_amount_plot(save_file="", params=params)
    name_list = df['名称'].values.tolist()
    amount_list = df['成交额'].values.tolist()
    pct_list = df['涨跌幅'].values.tolist()
    close_list = df['最新价'].values.tolist()
    code_list = df['代码'].values.tolist()
    print(len(name_list))
    res, j = "", 1
    for i in range(len(name_list)):
        res += name_list[i] + "\t"
        if j % 5 == 0:
            res += "\n"
        j += 1
    print(res)
    content = "#### **成交Top stock** \n\n>"
    content += "总共{}只\n\n>".format(len(name_list))
    Ding = DingAlarm()
    for i in range(len(name_list)):
        url = add_url(str(code_list[i]))
        name = "[{}]({})".format(name_list[i], url)
        pct = "{}%".format(pct_list[i])
        if pct > '0':
            pct = Ding.coloring(text=pct, color="red")
        else:
            pct = Ding.coloring(text=pct, color="green")
        content += "{}{}/{}/{}亿\n\n>".format(name, close_list[i], pct, amount_list[i])
    if params['need_send'] == True:
        Ding.send_dingd(content=content)
        file = "C:/Users/Administrator/PycharmProjects/stock/trade/back_info/result_data/newest_amount/amount_top_info.csv"
        df.to_csv(file, index=False)
        print("https://github.com/fushida/back_info/blob/main/result_data/newest_amount/amount_top_info.csv")

# print("""成交额柱状图颜色解释:
#   红色表示涨停
#   绿色表示低于五日均线
#   蓝色表示上影线不足1.2%
#   灰色表示高于五日均线
#   """)
test = 1
if test == 1:
    params1 = {"sort_ways": "60日涨跌幅",
              "maxn": 100, "vol_max": 150, "vol_min": 5,
              "pct_limit": -2.5,
              'blue_line': 150, 'yellow_line': 60,
              "need_show": True,
              "need_send": False,
              "need_ma5": True,
              "need_minute": False,
              'filter_high': True
              }
    params2 = {"sort_ways": "成交额",
              "maxn": 100, "vol_max": 150, "vol_min": 5,
              "pct_limit": -2, # 最小涨幅-2
              'blue_line': 30, 'yellow_line': 10,
              "need_show": True, # 是否需要画图
              "need_send": False, # 钉钉发送结果
              "need_ma5": True, # 是否需要
              "need_minute": False, # 是否需要30分线
              'filter_high': True
              }
    run_test(params=params2) # 选择成交量还是近60天的涨幅
