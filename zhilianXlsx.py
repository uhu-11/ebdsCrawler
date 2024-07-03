import datetime
import re
import webbrowser
from time import sleep
import requests
import redis
import hashlib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
import pymysql
import xlwt


# 连接到redis和数据库
# r = redis.Redis(host="192.168.3.106", port=6379, db=0)

# 配置selenium
# flag1 = '智联招聘</title>'
flag1 = '智联招聘'
flag2 = '页面信息丢失'
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
options.add_experimental_option("prefs", prefs)
options.page_load_strategy = 'eager'
# 设置代理
# options.add_argument('--proxy-server=%s' % 'http://121.11.115.186:16819')
driver = webdriver.Chrome(options=options)
js = open('stealth.min.js').read()
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})


def main(city):
    cookies = {
        'x-zp-client-id': '0493f927-b24c-403b-96aa-7cddf4be3c85',
        'sts_deviceid': '1905ddc5787581-0c35e7cda8542c-4c657b58-1296000-1905ddc5788f31',
        'ZP_OLD_FLAG': 'false',
        'locationInfo_search': '{%22code%22:%22647%22%2C%22name%22:%22%E6%B3%B0%E5%B7%9E%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}',
        'selectCity_search': '538',
        'LastCity': '%E4%BF%9D%E5%AE%9A',
        'LastCity%5Fid': '570',
        'at': '8e84e73b1a0f4408bb107b82a8fcc202',
        'rt': 'd7452d8920024c5cb73c714ebc36f0a9',
        'ssxmod_itna': 'Qq+xcDyDgifrDODzxAhYoDkDBQQn6=YfxdEo4D/tmDnqD=GFDK40oE7iD7tchQn6xr3Gq0Giyi4SRAegiKObEk3KoDU4i8DCk0eYlDeW=D5xGoDPxDeDADYE6DAqiOD7qDdfhTXtkDbxi3SxGCOx0CVoYD7=v8m=YDhxDCXmPDwOA8DiWFqtvp2=GIeiG8D7vhDlpxEfw8bf3LSmvI+b3GEiKDXEdDvaHw0OoDUn9z9xBoWmRYb0wKb703Pjh4WAuDOixKCBpxzA=KW7ZD7kDeO7cutqDWHljDD=',
        'ssxmod_itna2': 'Qq+xcDyDgifrDODzxAhYoDkDBQQn6=YfxdoYG9iuiDBwRYq7PeNOFWG2DGEP7=D+6TD=',
        'sensorsdata2015jssdkchannel': '%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221161309461%22%2C%22first_id%22%3A%2218fe7f4e0e8f2d-0fbee4d1db5699-4c657b58-1296000-18fe7f4e0e91c9e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmZTdmNGUwZThmMmQtMGZiZWU0ZDFkYjU2OTktNGM2NTdiNTgtMTI5NjAwMC0xOGZlN2Y0ZTBlOTFjOWUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTYxMzA5NDYxIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221161309461%22%7D%2C%22%24device_id%22%3A%2218fe7f4e0e8f2d-0fbee4d1db5699-4c657b58-1296000-18fe7f4e0e91c9e%22%7D',
        'sts_sg': '1',
        'sts_sid': '1905ddc5c12d71-0fdd52e5bce88e-4c657b58-1296000-1905ddc5c131199',
        'sts_chnlsid': 'Unknown',
        'zp_src_url': 'https%3A%2F%2Fpassport.zhaopin.com%2F',
        'sts_evtseq': '4',
        'ZL_REPORT_GLOBAL': '{%22/resume/new%22:{%22actionid%22:%225d379033-9c97-4b0c-b866-58cfe646b45e%22%2C%22funczone%22:%22addrsm_ok_rcm%22}%2C%22//www%22:{%22seid%22:%228e84e73b1a0f4408bb107b82a8fcc202%22%2C%22actionid%22:%2283ac1fe0-6b06-4f1e-9d44-b62672dd1c6e-cityPage%22}}',
        'acw_tc': '276077d917195616172802403e28e0ea826906835ebce39358b9a894824123',
        'Hm_lpvt_7fa4effa4233f03d11c7e2c710749600': '1719561665',
        'Hm_lvt_7fa4effa4233f03d11c7e2c710749600': '1718100353,1719561589',

        # 未找到
        # 'FSSBBIl1UgzbN7NP': '5RmN7yKpFMi3qqqDEqs29mGeD5NgtMy5J_unnocj.HkIzhLDqUN34Q4cHbZ4ird42K5kM6.hNZH29pT4tHOXWMG_QKeQq3B5Sj8AXj5Za8TpxDNbmDhqy0yfaUy3a4fX29NoXirsVG6mKhCIZR9J3PV7Xj7nMPY7OKYZrGU56Hg3E1Y3pCkNNFFExdvR3OUGPhCj0yc5JCyM5zkRzoXWxz8vlEbjaXdrAHIFJZC04weGq8i_DACj0ekYExgm4EaeKBotStWNnAQ56xojehw754But0cluY_orps_E._oywSqa',
        # 'zp_passport_deepknow_sessionId': 'b28f565as77e2e48f8a58850398421fae434',
        # 'campusOperateJobUserInfo': '3e03838f-d610-4ff0-b947-07e184f0d25e',
        # 'FSSBBIl1UgzbN7NO': '5kwkRLYuos2clTdlVW6rFPLqBJPZnbfWwsUgBUpj1Hn6EyOWYTTi4KpRWfpJG64KJwwr7gF78a1C3aCEDu4TbYA',
        # '_uab_collina': '168257626983812849729792',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
                      'Safari/537.36 Edg/126.0.0.0 '
    }

    # for page in range(1, 5):
    for page in range(1, 2):

        params = {
            'jl': city,
            'p': page,
            # 'cityCode': city
        }

        print("开始第" + str(page) + "页  ")

        response = requests.get('https://sou.zhaopin.com/', params=params, headers=headers, cookies=cookies)
        # response = requests.get('https://sou.zhaopin.com/?jl=538&p=1', headers=headers, cookies=cookies)
        # response = requests.get('https://m.zhaopin.com/sou', headers=headers, cookies=cookies)
        if response.status_code != 200:
            return
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        print("soup为:")
        print(str(soup))

        # positionList-hook > div > div.positionlist__list > div:nth-child(1) > div.joblist-box__iteminfo > div.jobinfo > div.jobinfo__top > a
        job_name = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.jobinfo > div.jobinfo__top > a")
        salary = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.jobinfo > div.jobinfo__top > p")
        comp_name = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.companyinfo > div.companyinfo__top > a")
        position = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.jobinfo > div.jobinfo__other-info > div:nth-child(1) > span")
        experience = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.jobinfo > div.jobinfo__other-info > div:nth-child(2)")
        degree = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.jobinfo > div.jobinfo__other-info > div:nth-child(3)")
        comp_type = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.companyinfo > div.companyinfo__tag > div:nth-child(1)")
        comp_size = soup.select(
            "#positionList-hook > div > div.positionlist__list > div > div > div.companyinfo > div.companyinfo__tag > div:nth-child(2)")

        # sleep(10)
        print(job_name[0].text)
        print(job_name[1].text)
        print(job_name[2].text)
        print("jobNameEnd!!!")

        # #positionList-hook > div > div.positionlist__list > div:nth-child(1)

        tmp = soup.select("#positionList-hook > div > div.positionlist__list > div > div > div.jobinfo > div > a")
        # #positionList-hook > div > div.positionlist__list > div > div.joblist-box__iteminfo > div.jobinfo > div > a
        urls = ["" for i in range(0, len(tmp))]
        for i in range(0, len(tmp)):
            # print(tmp[i])
            urls[i] = tmp[i]['href'].split("?")[0]
            print("单个url为：" + urls[i])

        # 创建workbook
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建工作表
        mysheet = workbook.add_sheet('智联招聘就业数据', cell_overwrite_ok=True)
        # 表头
        header = ['岗位名称', '薪资', '公司名称', '公司类型', '公司规模', '地理位置', '工作经验要求', '学历要求', '岗位类型', '招聘人数', '行业', '岗位描述', '日期']

        # 写入xlx文件表头
        for k in range(0, 13):
            mysheet.write(0, k, header[k])

        # 设置数据初始写入行的行序
        j = 1
        # 遍历列表中的每一个url
        for i in range(0, len(urls)):
            if 1:
            # if add_url(urls[i]):
                param = get_detail(urls[i],
                                     job_name[i].text,
                                     salary[i].text,
                                     comp_name[i].text,
                                     comp_type[i].text,
                                     comp_size[i].text,
                                     position[i].text,
                                     experience[i].text,
                                     degree[i].text)
                # print(param)
                # 写入一行数据
                mysheet.write(j, 0, param[0])
                mysheet.write(j, 1, param[1])
                mysheet.write(j, 2, param[2])
                mysheet.write(j, 3, param[3])
                mysheet.write(j, 4, param[4])
                mysheet.write(j, 5, param[5])
                mysheet.write(j, 6, param[6])
                mysheet.write(j, 7, param[7])
                mysheet.write(j, 8, param[8])
                mysheet.write(j, 9, param[9])
                mysheet.write(j, 10, param[10])
                mysheet.write(j, 11, param[11])
                mysheet.write(j, 12, param[12])

                print("第" + str(j) + "行完成")
                # 行序递增
                j += 1

                sleep(2)
        print(str(city) + "第" + str(page) + "页完成")

        # 保存工作表
        workbook.save(str(city) + '第' + str(page) + '页结果.xlsx')
        # 打印消息
        print('第' + str(page) + '页数据写入到excel表中成功')


# def get_md5(val):
#     # 把目标数据进行哈希，用哈希值去重更快
#     md5 = hashlib.md5()
#     md5.update(val.encode('utf-8'))
#     return md5.hexdigest()


# def add_url(url):
#     res = r.sadd("employment_urls", get_md5(url))
#     if res == 0:  # 若返回0,说明插入不成功，表示有重复
#         return False
#     else:
#         return True


def get_detail(url, job_name, salary, comp_name, comp_type, comp_size, position, experience, degree):
    driver.get(url.strip())
    # print(url)
    source = driver.page_source
    title = re.findall('<title>(.*?)</title>', source)
    # print(title)
    # print(source)
    while flag1 not in source and flag2 not in source:
        # print(source)
        print('出现滑块！！！')
        # 滑块验证自动化
        # btn = driver.find_element('id', "nc_1_n1z")
        # ActionChains(driver).click_and_hold(btn).perform()
        # ActionChains(driver).move_by_offset(260, 0).perform()
        # ActionChains(driver).release().perform()
        sleep(20)
        source = driver.page_source

    soup = BeautifulSoup(source, 'html.parser')
    print(soup)
    job_type = soup.select("root > div.job-summary > div > div > div.summary-plane__bottom.clearfix > "
                           "div.summary-plane__left > ul > li:nth-child(4)")

    headcount = soup.select("root > div.job-summary > div > div > div.summary-plane__bottom.clearfix > "
                            "div.summary-plane__left > ul > li:nth-child(5)")
    # root > div.job-summary > div.summary-fixed > div > div.summary-fixed__left > div.summary-fixed__left > ul > li:nth-child(6)
    industry = soup.select("#root > div:nth-child(5) > div.app-main__right > div > div.company > div.company__detail "
                           "> button.company__industry")
    description = soup.select("#root > div:nth-child(5) > div.app-main__left > div.job-detail > div.describtion > "
                              "div.describtion__detail-content")

    # job_type = soup.select("#root > div.job-summary > div > div > div.summary-plane__bottom.clearfix > "
    #                        "div.summary-plane__left > ul > li:nth-last-child(2)")
    # headcount = soup.select("#root > div.job-summary > div > div > div.summary-plane__bottom.clearfix > "
    #                         "div.summary-plane__left > ul > li:nth-last-child(1)")
    # industry = soup.select("#root > div:nth-child(5) > div.app-main__right > div > div.company > div > "
    #                        "button.company__industry")
    # description = soup.select("#root > div:nth-child(5) > div.app-main__left > div.job-detail > div.describtion > "
    #                           "div.describtion__detail-content")

    # 去除空格和转行符
    salary = salary.strip()
    comp_name = comp_name.strip().replace('\n', '').replace('\r', '')
    comp_size = comp_size.strip()
    experience = experience.strip()
    degree = degree.strip()

    print(comp_name)
    print(comp_size)

    # 如果公司的第一个字段不是公司类型而是公司规模
    comp_type = comp_type.strip()
    if comp_type[0:1].isdigit():
        comp_size = comp_type
        comp_type = ""

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

    return job_name, salary, comp_name, comp_type, comp_size, position, experience, degree, job_type, headcount, industry, description, datetime.datetime.today().strftime('%Y-%m')


if __name__ == '__main__':
    # main(530)
    # main(531)
    main(538)
    # main(551)
    # 565
    # 907
    # for i in range(538, 539):
    #     if i != 640 and i != 649 and i != 650 and i != 651 and i != 652 and i != 676 and i != 686 and i != 713 \
    #             and i != 784 and i != 797 and i != 798 and i != 839:
    #         main(i)
