# coding='utf-8'

# import gevent
import requests, time, re  # 发送请求，接收JSON数据，正则解析
from fake_useragent import UserAgent  # 随机请求头
from lxml import etree  # 进行xpath解析
from urllib import parse  # 将中文转换为url编码
import urllib3
# import xlwt
import xlrd
import pandas as pd

urllib3.disable_warnings()


def get_user_info(uid, base_url_1, headers):  # 传入用户id
    # 获取用户个人基本信息
    user_data = []  # 保存用户信息
    params = {
        'uid': uid,  # 用户id，即uid
    }  # 参数，用于组配链接
    while True:  # 防止timeout
        try:
            resp = requests.get(url=base_url_1, params=params, headers=headers, timeout=(30, 50), verify=False)
            print(resp)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    data = resp.json()  # 转换为josn格式
    info = data["data"]["user"]  # 用户信息
    id = info["id"]  # uid
    name = info["screen_name"]  # 用户名
    verified = info["verified"]  # 是否认证用户
    if verified == 'TRUE':  # 只有当是认证用户的时候
        verified_reason = info["verified_reason"]  # 认证原因/机构
    else:
        verified_reason = '未认证'
    location = info["location"]  # 地理位置
    gender = info["gender"]  # 性别，f为女，m为男
    followers_count = info["followers_count"]  # 粉丝数
    statuses_count = info["statuses_count"]  # 全部微博数
    user_data.append([id, name, verified, verified_reason, location, gender, followers_count, statuses_count])
    return user_data  # 返回用户基本信息


def get_user_detail_info(uid, base_url_2, headers):  # 传入用户id
    # 获取用户个人详细信息
    user_data = []  # 保存用户信息
    params = {
        'uid': uid,  # 用户id，即uid
    }  # 参数，用于组配链接
    while True:  # 防止timeout
        try:
            resp = requests.get(url=base_url_2, params=params, headers=headers, timeout=(30, 50), verify=False)
            # print(resp)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    data = resp.json()  # 转换为josn格式
    info = data["data"]  # 用户信息
    birthday = info["birthday"]  # birthday
    created_at = info["created_at"]  # 账号创建时间
    description = info["description"]  # 简介
    # verified_reason=info["verified_reason"]#认证原因/机构
    try:
        ip_location = info["ip_location"]  # ip属地
    except:
        ip_location = info["location"]  # 使用地点替代ip地址
    # print(ip_location)
    user_data.append([birthday, created_at, description, ip_location])  #

    return user_data  # 返回用户详细信息


def extract(inpath):
    """取出uid数据"""
    data = xlrd.open_workbook(inpath, encoding_override='utf-8')
    table = data.sheets()[0]  # 选定表
    nrows = table.nrows  # 获取行号
    ncols = table.ncols  # 获取列号
    numbers = []
    for i in range(1, nrows):  # 第0行为表头
        alldata = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        result_1 = alldata[2]  # 取出表中数据，bid
        numbers.append(str(int(result_1)))
    return numbers


def get_header(cookie):
    headers = {
        'authority': 's.weibo.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'cookie': cookie,
        'pragma': 'no-cache',
        'Host': 'weibo.com',
        'referer': 'https://weibo.com/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': UserAgent().random,
    }  # com版本

    return headers

def run(headers, uids,id_list, name_list,save_file):
    succ_num, fail_num = 0, 0
    infos = []
    for uid in uids:
        info = []
        if uid in id_list and len(name_list[id_list.index(uid)]) > 0:
            continue
        try:
            base_url_1 = "https://weibo.com/ajax/profile/info"  # 基本信息域名
            base_url_2 = "https://weibo.com/ajax/profile/detail"  # 详细信息域名
            base_info = get_user_info(uid, base_url_1, headers)
            detail_info = get_user_detail_info(uid, base_url_2, headers)
            for i, j in zip(base_info, detail_info):
                info.append(i + j)  # 组合成一个列表
            print(info[0])
            info_ = [str(i) for i in info[0]]
            save_file.write(",".join(info_))  # 备份
            infos.append(info[0])
            succ_num += 1
            time.sleep(1)  # 跑一个sleep下
        except:
            fail_num += 1
            print(uid, "crawl fail")
    print("成功抓取{}条，失败抓取{}条".format(succ_num, fail_num))
    return infos

if __name__ == '__main__':
    # 1、填入cookie
    cookie = "SINAGLOBAL=7411150802454.904.1686642285119; UOR=,,www.baidu.com; XSRF-TOKEN=kcjckF4eSzijIttYY8v9mekm; SSOLoginState=1687000855; _s_tentry=weibo.com; Apache=8176000020546.344.1687000869890; ULV=1687000869900:3:3:3:8176000020546.344.1687000869890:1686729590319; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFlXNTIxyzl.23nL25_2_sX5JpX5KMhUgL.FoMXeKeEeK-ESoM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSh20eo2feoqN; ALF=1690474268; SCF=AkS2kR2LzZmdGLiaVBYXotBf8Atp6jn28xA919QWC3bikEvE8rRHgcSg7aJ3LTgamxKpsUYX8QXtPgl7jqxfJnM.; SUB=_2A25Jn3pMDeRhGeFK6lET8SvOzTuIHXVq7eyErDV8PUNbmtANLU_XkW9NQ4bTizhhaQAEn7jNuFehXOgKRvG27Q32; WBPSESS=5Z6s8UWJ0z4nYQUZnNpJf7PjDSJy6sHEhVMbwwosZSdx82f1X9eGwKZUBmwGElIMQ29Tkom-dzBHMDjmGckaOYc0UxNFQZGYdPpKgJp0m7O4KaY2cQ6LuaYW-bhSJsnwrMQ9BAiFFMUVMzgS_wMq3g=="
    headers = get_header(cookie)  # 获取headers
    uids = []
    # 2、批量放入uid在filename中
    try:
        filename = 'xx.txt'
        for line in open(filename, 'r'):
            uids.append(line.strip())
    except:
        uids = ['1859372664']  # 根据uid获取，单个用户
    print("用户总数{}".format(len(uids)))

    # 3、创建存储路径
    save_file = open('user_infos.txt', 'a+', encoding='utf-8')
    try:
        rdf = pd.read_csv('user_info_.csv')
        id_list = rdf['id'].vlaues.tolist()
        name_list = rdf['name'].vlaues.tolist()
    except:
        id_list = [] # 若是没有user_info_则置为空
        name_list = []
    infos = run(headers=headers, uids=uids, id_list=id_list, name_list=id_list, save_file=save_file)
    info_head = ['id', 'name', 'verified', 'verified_reason', "location", "gender",
                 "followers_count", "statuses_count",
                 "birthday", "created_at", "description", "ip_location"]
    df = pd.DataFrame(infos, columns=info_head)
    # 4、创建存储csv文件
    df.to_csv("user_info_.csv", index=False)  # 存储为csv