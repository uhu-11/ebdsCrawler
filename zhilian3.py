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
# 设置代理
options.add_argument('--proxy-server=%s' % 'http://121.11.115.186:16819')
driver = webdriver.Chrome(options=options)
js = open('stealth.min.js').read()
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                      'Safari/537.36 '
    }

    for page in range(1, 35):

        params = {
            'jl': city,
            'p': page
        }

        response = requests.get('https://sou.zhaopin.com/', params=params, headers=headers, cookies=cookies)
        if response.status_code != 200:
            return
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
                                     degree[i].text))
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


def get_detail(url, job_name, salary, comp_name, comp_type, comp_size, position, experience, degree):
    driver.get(url.strip())
    print(url)
    source = driver.page_source
    while flag1 not in source and flag2 not in source:
        print('出现滑块')
        # 滑块验证自动化
        # btn = driver.find_element('id', "nc_1_n1z")
        # ActionChains(driver).click_and_hold(btn).perform()
        # ActionChains(driver).move_by_offset(260, 0).perform()
        # ActionChains(driver).release().perform()
        sleep(10)
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
    return (job_name, salary, comp_name, comp_type, comp_size, position, experience, degree, job_type, headcount, industry, description, datetime.datetime.today().strftime('%Y-%m'))


def insert_db(param):
    # 获取一个游标对象
    cursor = conn.cursor()
    # sql语句中，用%s做占位符，参数用一个元组
    sql = "insert into info values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # 执行数据库插入
    cursor.execute(sql, param)
    # 提交
    conn.commit()


if __name__ == '__main__':
    # main(530)
    # main(531)
    # main(538)
    # main(551)
    # 565
    # 907
    for i in range(833, 840):
        if i != 640 and i != 649 and i != 650 and i != 651 and i != 652 and i != 676 and i != 686 and i != 713 \
                and i != 784 and i != 797 and i != 798 and i != 839:
            main(i)