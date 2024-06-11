import datetime
from time import sleep
import requests
import redis
import hashlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
import pymysql


# 连接到redis和数据库
conn = pymysql.connect(host="nj-cynosdbmysql-grp-b3f65mfl.sql.tencentcdb.com", port=25704, user="root", passwd="huhu-1234", db="employment")
r = redis.Redis(host="192.168.3.106", port=6379, db=0)


# 配置selenium
flag1 = '智联招聘官网</title>'
flag2 = '页面信息丢失</title>'
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
options.add_experimental_option("prefs", prefs)
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)


def main(city):
    cookies = {
        'x-zp-client-id': '60292532-3bb1-477a-a4bd-9b943b1f3bdd',
        'sts_deviceid': '187c15aea0a185a-0ff01c8be4dd5d-26031851-1821369-187c15aea0b186e',
        'ZP_OLD_FLAG': 'false',
        'campusOperateJobUserInfo': '3e03838f-d610-4ff0-b947-07e184f0d25e',
        'FSSBBIl1UgzbN7NO': '5kwkRLYuos2clTdlVW6rFPLqBJPZnbfWwsUgBUpj1Hn6EyOWYTTi4KpRWfpJG64KJwwr7gF78a1C3aCEDu4TbYA',
        '_uab_collina': '168257626983812849729792',
        'locationInfo_search': '{%22code%22:%22635%22%2C%22name%22:%22%E5%8D%97%E4%BA%AC%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}',
        'selectCity_search': '635',
        'LastCity': '%E5%8D%97%E4%BA%AC',
        'LastCity%5Fid': '635',
        'at': 'ccf0c348bfe149f5a343940b5a88599c',
        'rt': 'a84c1a26b8ce4a44882de5d263ca303f',
        'ssxmod_itna': 'Qq+xcDyDgifrDODzxAhYoDkDBQQn6=YfxdEo4D/tmDnqD=GFDK40oE7iD7tchQn6xr3Gq0Giyi4SRAegiKObEk3KoDU4i8DCk0eYlDeW=D5xGoDPxDeDADYE6DAqiOD7qDdfhTXtkDbxi3SxGCOx0CVoYD7=v8m=YDhxDCXmPDwOA8DiWFqtvp2=GIeiG8D7vhDlpxEfw8bf3LSmvI+b3GEiKDXEdDvaHw0OoDUn9z9xBoWmRYb0wKb703Pjh4WAuDOixKCBpxzA=KW7ZD7kDeO7cutqDWHljDD=',
        'ssxmod_itna2': 'Qq+xcDyDgifrDODzxAhYoDkDBQQn6=YfxdoYG9iuiDBwRYq7PeNOFWG2DGEP7=D+6TD=',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221168507690%22%2C%22first_id%22%3A%22187c157aac6140c-0ee4bfe089185f-26031851-1821369-187c157aac7198a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3YzE1N2FhYzYxNDBjLTBlZTRiZmUwODkxODVmLTI2MDMxODUxLTE4MjEzNjktMTg3YzE1N2FhYzcxOThhIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTE2ODUwNzY5MCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221168507690%22%7D%2C%22%24device_id%22%3A%22187c157aac6140c-0ee4bfe089185f-26031851-1821369-187c157aac7198a%22%7D',
        'sts_sg': '1',
        'sts_sid': '1880125ad611542-04770bc1e95472-26031851-1821369-1880125ad62ffd',
        'sts_chnlsid': 'Unknown',
        'zp_src_url': 'https%3A%2F%2Fwww.zhaopin.com%2F',
        'Hm_lvt_38ba284938d5eddca645bb5e02a02006': '1683480573,1683522715,1683541815,1683646427',
        'sts_evtseq': '2',
        'ZL_REPORT_GLOBAL': '{%22//www%22:{%22seid%22:%22ccf0c348bfe149f5a343940b5a88599c%22%2C%22actionid%22:%2242eb4e04-f773-4f04-8ada-bf22ef22c34e-cityPage%22}}',
        'acw_tc': 'ac11000116836477157451374e00ce0b1e00cc95a8a6851f62e3fd1ccde19c',
        'Hm_lpvt_38ba284938d5eddca645bb5e02a02006': '1683647719',
        'FSSBBIl1UgzbN7NP': '5RmN7yKpFMi3qqqDEqs29mGeD5NgtMy5J_unnocj.HkIzhLDqUN34Q4cHbZ4ird42K5kM6.hNZH29pT4tHOXWMG_QKeQq3B5Sj8AXj5Za8TpxDNbmDhqy0yfaUy3a4fX29NoXirsVG6mKhCIZR9J3PV7Xj7nMPY7OKYZrGU56Hg3E1Y3pCkNNFFExdvR3OUGPhCj0yc5JCyM5zkRzoXWxz8vlEbjaXdrAHIFJZC04weGq8i_DACj0ekYExgm4EaeKBotStWNnAQ56xojehw754But0cluY_orps_E._oywSqa',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                      'Safari/537.36 '
    }

    for page in range(1, 35):

        params = {
            'jl': city,
            'p': page
        }

        response = requests.get('https://sou.zhaopin.com/', params=params, headers=headers, cookies=cookies)
        # 对请求结果的状态码进行判断
        if response.status_code != 200:
            return
        # 设置请求
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        job_name = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line1 > div.iteminfo__line1__jobname > span")
        salary = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line2 > div.iteminfo__line2__jobdesc > p")
        comp_name = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line1 > div.iteminfo__line1__compname > span")
        position = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line2 > div.iteminfo__line2__jobdesc > ul > li:nth-child(1)")
        experience = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line2 > div.iteminfo__line2__jobdesc > ul > li:nth-child(2)")
        degree = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line2 > div.iteminfo__line2__jobdesc > ul > li:nth-child(3)")
        comp_desc = soup.select("#positionList-hook > div > div > a > div.iteminfo__line.iteminfo__line2 > div.iteminfo__line2__compdesc")

        tmp = soup.select("#positionList-hook > div > div > a")
        urls = ["" for i in range(0, len(tmp))]
        for i in range(0, len(tmp)):
            urls[i] = tmp[i]['href'].split("?")[0]

        for i in range(0, len(urls)):
            if add_url(urls[i]):
                insert_db(get_detail(urls[i],
                                     job_name[i].text,
                                     salary[i].text,
                                     comp_name[i].text,
                                     comp_desc[i].text.split(" " + " ")[0],
                                     comp_desc[i].text.split(" " + " ")[1],
                                     position[i].text,
                                     experience[i].text,
                                     degree[i].text, city2province(position[i].text)))
                sleep(1)
        print(str(city) + "第" + str(page) + "页完成")


def get_md5(val):
    # 把目标数据进行哈希，用哈希值去重更快
    md5 = hashlib.md5()
    md5.update(val.encode('utf-8'))
    return md5.hexdigest()


def add_url(url):
    res = r.sadd("employment_urls", get_md5(url))
    if res == 0:  # 若返回0,说明插入不成功，表示有重复
        return False
    else:
        return True


def get_detail(url, job_name, salary, comp_name, comp_type, comp_size, position, experience, degree, province):
    driver.get(url.strip())
    print(url)
    source = driver.page_source
    while flag1 not in source and flag2 not in source:
        print('出现滑块')
        # 滑块验证自动化
        btn = driver.find_element('id', "nc_1_n1z")
        ActionChains(driver).click_and_hold(btn).perform()
        ActionChains(driver).move_by_offset(260, 0).perform()
        ActionChains(driver).release().perform()
        sleep(2)
        driver.refresh()
        source = driver.page_source

    soup = BeautifulSoup(source, 'html.parser')
    job_type = soup.select("#root > div.job-summary > div > div > div.summary-plane__bottom.clearfix > div.summary-plane__left > ul > li:nth-last-child(2)")
    headcount = soup.select("#root > div.job-summary > div > div > div.summary-plane__bottom.clearfix > div.summary-plane__left > ul > li:nth-last-child(1)")
    industry = soup.select("#root > div:nth-child(5) > div.app-main__right > div > div.company > div > button.company__industry")
    description = soup.select("#root > div:nth-child(5) > div.app-main__left > div.job-detail > div.describtion > div.describtion__detail-content")
    if len(job_type) == 0:
        job_type = ""
    else:
        job_type = job_type[0].text
    if len(headcount) == 0:
        headcount = ""
    else:
        headcount = headcount[0].text
    if len(industry) == 0:
        industry = ""
    else:
        industry = industry[0].text
    if len(description) == 0:
        description = ""
    else:
        description = description[0].text
    return (job_name, salary, comp_name, comp_type, comp_size, position, experience, degree, job_type, headcount, industry, description, datetime.datetime.today().strftime('%Y-%m'), province)


def insert_db(param):
    # 获取一个游标对象
    cursor = conn.cursor()
    # sql语句中，用%s做占位符，参数用一个元组
    sql = "insert into info(jobName, salary, compName, compType, compSize, position, experience, degree, jobType, headcount, industry, description, season, province) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        # 执行数据库插入
        cursor.execute(sql, param)
        # 提交
        conn.commit()
    except:
        # 发生错误回滚
        conn.rollback()
        print("数据插入错误")


def city2province(position):
    city = position.split("-")[0]
    allCityList = [["北京"], ["上海"], ["天津"], ["重庆"],
                   ["石家庄", "唐山", "秦皇岛", "邯郸", "邢台", "保定", "张家口", "承德", "沧州", "廊坊", "衡水"],
                   ["太原", "大同", "阳泉", "长治", "晋城", "朔州", "晋中", "运城", "忻州", "临汾", "吕梁"],
                   ["呼和浩特", "包头", "乌海", "赤峰", "通辽", "鄂尔多斯", "呼伦贝尔", "兴安盟", "锡林郭勒盟", "乌兰察布", "巴彦淖尔", "阿拉善盟"],
                   ["沈阳", "大连", "鞍山", "抚顺", "本溪", "丹东", "锦州", "营口", "阜新", "辽阳", "盘锦", "铁岭", "朝阳", "葫芦岛"],
                   ["长春", "吉林", "四平", "辽源", "通化", "白山", "松原", "白城", "延边"],
                   ["哈尔滨", "齐齐哈尔", "鸡西", "鹤岗", "双鸭山", "大庆", "伊春", "佳木斯", "七台河", "牡丹江", "黑河", "绥化", "大兴安岭"],
                   ["南京", "无锡", "徐州", "常州", "苏州", "南通", "连云港", "淮安", "盐城", "扬州", "镇江", "泰州", "宿迁"],
                   ["杭州", "宁波", "温州", "嘉兴", "湖州", "绍兴", "金华", "衢州", "舟山", "台州", "丽水"],
                   ["合肥", "芜湖", "蚌埠", "淮南", "马鞍山", "淮北", "铜陵", "安庆", "黄山", "滁州", "阜阳", "宿州", "六安", "亳州", "池州", "宣城"],
                   ["福州", "厦门", "龙岩", "南平", "宁德", "莆田", "泉州", "三明", "漳州"],
                   ["南昌", "萍乡", "九江", "上饶", "抚州", "吉安", "鹰潭", "宜春", "新余", "景德镇", "赣州"],
                   ["济南", "青岛", "淄博", "枣庄", "东营", "烟台", "潍坊", "济宁", "泰安", "威海", "日照", "临沂", "德州", "聊城", "滨州", "菏泽"],
                   ["郑州", "开封", "洛阳", "平顶山", "焦作", "鹤壁", "新乡", "安阳", "濮阳", "许昌", "漯河", "三门峡", "南阳", "商丘", "信阳", "周口",
                    "驻马店"], ["武汉", "宜昌", "黄冈", "恩施", "荆州", "十堰", "咸宁", "襄阳", "孝感", "随州", "黄石", "荆门", "鄂州"],
                   ["长沙", "邵阳", "常德", "郴州", "株洲", "娄底", "湘潭", "益阳", "永州", "岳阳", "衡阳", "怀化", "韶山", "张家界"],
                   ["广州", "深圳", "潮州", "韶关", "湛江", "惠州", "清远", "东莞", "江门", "茂名", "肇庆", "汕尾", "河源", "揭阳", "梅州", "中山",
                    "阳江", "云浮", "珠海",
                    "汕头", "佛山"], ["南宁", "柳州", "桂林", "梧州", "北海", "防城港", "钦州", "贵港", "玉林", "百色", "贺州", "河池", "来宾", "崇左"],
                   ["海口", "三亚", "洋浦"],
                   ["成都", "自贡", "攀枝花", "泸州", "德阳", "绵阳", "广元", "遂宁", "内江", "乐山", "南充", "眉山", "宜宾", "广安", "达州", "雅安",
                    "巴中", "资阳", "阿坝",
                    "甘孜", "凉山"], ["贵阳", "安顺", "黔西南", "遵义", "铜仁", "六盘水", "毕节", "黔东南", "黔南"],
                   ["昆明", "曲靖", "玉溪", "保山", "昭通", "楚雄", "红河", "文山", "西双版纳", "大理", "德宏", "丽江", "怒江", "迪庆", "临沧"],
                   ["拉萨", "昌都", "山南", "日喀则", "那曲", "阿里", "林芝"],
                   ["西安", "安康", "汉中", "宝鸡", "咸阳", "榆林", "渭南", "商洛", "铜川", "延安"],
                   ["兰州", "嘉峪关", "金昌", "白银", "天水", "武威", "张掖", "平凉", "酒泉", "庆阳", "定西", "陇南", "临夏", "甘南"],
                   ["西宁", "海北", "海西", "黄南", "果洛", "玉树", "海东", "海南州"], ["银川", "固原", "中卫", "石嘴山", "吴忠"],
                   ["乌鲁木齐", "克拉玛依", "吐鲁番", "哈密", "昌吉", "博尔塔拉", "巴音郭楞", "阿克苏", "克孜勒苏柯尔克孜", "喀什", "和田", "伊犁", "塔城",
                    "阿勒泰"]]
    provinceList = ["北京", "上海", "天津", "重庆", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东",
                    "河南", "湖北", "湖南", "广东", "广西", "海南", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆"]
    for i in range(0, len(allCityList)):
        for j in range(0, len(allCityList[i])):
            if allCityList[i][j] == city:
                return provinceList[i]
    return " "


# if __name__ == '__main__':
#     main(530)
#     main(531)
#     main(538)
#     main(551)
#     for i in range(565, 907):
#         if i != 640 and i != 649 and i != 650 and i != 651 and i != 652 and i != 676 and i != 686 and i != 713 \
#                 and i != 784 and i != 797 and i != 798 and i != 839:
#             main(i)