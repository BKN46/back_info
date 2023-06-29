
import json
import pandas as pd

df1 =pd.read_csv('data2019.csv')

df2 =pd.read_csv('data2019v2.csv')

df = pd.concat([df1,df2])



sdf = df.drop_duplicates(['text'])

print(sdf)
sdf.to_csv("/Users/think/Downloads/Data2019.csv", index=False, encoding="utf-8")
print(df1)



"""
git链接https://github.com/dataabc/weibo-search
"""

"""
其他https://github.com/Arrackisarookie/weibo-hot-search
https://github.com/gaussic/weibo_wordcloud  生成词云 也可以crawl
https://github.com/mengsiwei/data_process_shanghai_covid_19
https://github.com/Cheereus/WeiboEmotionAnalyzer
"""