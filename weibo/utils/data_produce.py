# -*- encoding=utf-8 -*-
import time
import warnings
warnings.filterwarnings('ignore')
import akshare as ak
import pandas as pd

header = ['id', 'bid', 'user_id', 'text', 'retweet_id', 'article_url', 'topics', 'location', 'created_at',
          'attitudes_count', 'comments_count', 'reposts_count', 'at_users']
count = 0
data_list = []

for line in open('./spiders/data1901_wujia.txt', encoding='utf-8'):
    count += 1
    tmp = line.strip().split("|||")
    if len(tmp) == 13:
        data_list.append(tmp)
#
# for line in open('data1801_gongzuo.txt', encoding='utf-8'):
#     tmp = line.strip().split("|||")
#     count += 1
#     if len(tmp) == 13:
#         data_list.append(tmp)

df = pd.DataFrame(data_list, columns=header)
print(count)
print(df.shape)
df = df.drop_duplicates(['text'], keep='first')
print("drop dup")
print(df.shape)
def text_filter(text):
    flag = 0
    filter_words = ['@', 'O网页链接', 'via','表了头条文章','正式公布','快讯','公布','日评论','日电','发布','报告','公告',
                    '独家','披露','工作会议','出炉','我在看','播报','』','O','新浪看点','秒看','】','关注以下','排行榜',
                    '微博视频','表示','统计结果','同比增长']
    for word in filter_words:
        if word in text:
            return 1
    if len(text) > 120:
        return 1
    return flag

def filter_time(created_at):
    flag = 0
    if '2019' in str(created_at):
        flag = 1

    return flag

df['flag2'] = df.apply(lambda x:filter_time(x['created_at']), axis=1)
df = df[(df['flag2'] == 1)]

# df['flag'] = df.apply(lambda x:text_filter(x['text']), axis=1)
# df = df[(df['flag'] != 1)]
# print(df.shape)
# col = ['id', 'user_id', 'text', 'retweet_id', 'topics', 'location', 'created_at',
#           'attitudes_count', 'comments_count', 'reposts_count', 'at_users']
# df[col].to_csv("./data/data1901_wujia.csv", index=False)