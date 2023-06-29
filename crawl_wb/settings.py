# -*- coding: utf-8 -*-

BOT_NAME = 'weibo'
SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
LOG_LEVEL = 'ERROR'
# 访问完一个页面再访问下一个时需要等待的时间，默认为10秒
DOWNLOAD_DELAY = 1
DEFAULT_REQUEST_HEADERS = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cookie': 'SINAGLOBAL=7411150802454.904.1686642285119; UOR=,,www.baidu.com; XSRF-TOKEN=kcjckF4eSzijIttYY8v9mekm; SSOLoginState=1687000855; _s_tentry=weibo.com; Apache=8176000020546.344.1687000869890; ULV=1687000869900:3:3:3:8176000020546.344.1687000869890:1686729590319; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFlXNTIxyzl.23nL25_2_sX5JpX5KMhUgL.FoMXeKeEeK-ESoM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSh20eo2feoqN; ALF=1690632358; SCF=AkS2kR2LzZmdGLiaVBYXotBf8Atp6jn28xA919QWC3binl_jfWPGOxEwoY06OTaEXG0MpeDoxQwpxMhuuQaa7Nc.; SUB=_2A25JmQP4DeRhGeFK6lET8SvOzTuIHXVq73IwrDV8PUNbmtAGLWXakW9NQ4bTi4GYWw4a8WIcQf4e2pVwAWQgYS4V; WBPSESS=5Z6s8UWJ0z4nYQUZnNpJf7PjDSJy6sHEhVMbwwosZSdx82f1X9eGwKZUBmwGElIMQ29Tkom-dzBHMDjmGckaOabDHGZY9eR2D2vFyYEGHvdEZ_RwALHxKmIkihKl7grIKnL-gVvd5NqD6n6UaFSGiA=='
}
ITEM_PIPELINES = {
    'weibo.pipelines.DuplicatesPipeline': 300,
    'weibo.pipelines.CsvPipeline': 301,
    # 'weibo.pipelines.MysqlPipeline': 302,
    # 'weibo.pipelines.MongoPipeline': 303,
    # 'weibo.pipelines.MyImagesPipeline': 304,
    # 'weibo.pipelines.MyVideoPipeline': 305
}
# 要搜索的关键词列表，可写多个, 值可以是由关键词或话题组成的列表，也可以是包含关键词的txt文件路径，
# 如'keyword_list.txt'，txt文件中每个关键词占一行
#  经济、就业、收入、物价、购房、投资、生活状况
#
#KEYWORD_LIST =['经济压力', '没有经济', '经济来源', '经济形势', '实体经济', '经济问题', '经济水平', '没经济', '当地经济', '明年经济', '今年经济', '未来经济'] # 或者 KEYWORD_LIST = 'keyword_list.txt'
#'整体经济', '经济活力', '经济拮据', '经济寒冬', '经济差', '经济萧条', '经济低迷', '经济平稳', '经济紧张', '经济保障', '经济企稳', '经济不行', '经济预期', '经济崩溃', '经济风险', '经济疲软', '经济走势', '经济飞速发展', '经济停滞', '经济乐观', '经济减速', '经济宽裕', '经济蓬勃发展', '经济跟不上', '经济恢复', '经济倒退']

#KEYWORD_LIST =['经济压力', '没有经济', '经济来源', '经济形势', '实体经济', '经济问题', '经济水平', '没经济', '当地经济', '明年经济', '今年经济', '未来经济','整体经济', '经济活力', '经济拮据', '经济寒冬', '经济差', '经济萧条', '经济低迷', '经济平稳', '经济紧张', '经济保障', '经济企稳', '经济不行', '经济预期', '经济崩溃', '经济风险', '经济疲软', '经济走势', '经济飞速发展', '经济停滞', '经济乐观', '经济减速', '经济宽裕', '经济蓬勃发展', '经济跟不上', '经济恢复', '经济倒退']


#KEYWORD_LIST = ['经济状况', '经济条件', 'GDP', '经济']
#KEYWORD_LIST =['收入', '工资', '挣钱', '没钱', '报酬', '奖金', '升职', '利润', '资产', '收益', '补贴', '薪水', '薪酬', '加薪', '薪资', '财产', '福利', '待遇', '财富']
KEYWORD_LIST = ['涨薪', '降薪', '挣钱少', '挣钱多', '没钱', '奖金', '工资下降', '福利减少', '资产缩水', '收入减少', '收入增加', '升职']

# 要搜索的微博类型，0代表搜索全部微博，1代表搜索全部原创微博，2代表热门微博，3代表关注人微博，4代表认证用户微博，5代表媒体微博，6代表观点微博
WEIBO_TYPE = 1
# 筛选结果微博中必需包含的内容，0代表不筛选，获取全部微博，1代表搜索包含图片的微博，2代表包含视频的微博，3代表包含音乐的微博，4代表包含短链接的微博
CONTAIN_TYPE = 0
# 筛选微博的发布地区，精确到省或直辖市，值不应包含“省”或“市”等字，如想筛选北京市的微博请用“北京”而不是“北京市”，想要筛选安徽省的微博请用“安徽”而不是“安徽省”，可以写多个地区，
# 具体支持的地名见region.py文件，注意只支持省或直辖市的名字，省下面的市名及直辖市下面的区县名不支持，不筛选请用“全部”
#REGION = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆']
REGION = ['全部']
# 搜索的起始日期，为yyyy-mm-dd形式，搜索结果包含该日期
START_DATE = '2018-01-01'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期
END_DATE = '2018-06-30'
# 进一步细分搜索的阈值，若结果页数大于等于该值，则认为结果没有完全展示，细分搜索条件重新搜索以获取更多微博。数值越大速度越快，也越有可能漏掉微博；数值越小速度越慢，获取的微博就越多。
# 建议数值大小设置在40到50之间。
FURTHER_THRESHOLD = 46
# 图片文件存储路径
IMAGES_STORE = './'
# 视频文件存储路径
FILES_STORE = './'
# 配置MongoDB数据库
# MONGO_URI = 'localhost'
# 配置MySQL数据库，以下为默认配置，可以根据实际情况更改，程序会自动生成一个名为weibo的数据库，如果想换其它名字请更改MYSQL_DATABASE值
# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = '123456'
# MYSQL_DATABASE = 'weibo'
