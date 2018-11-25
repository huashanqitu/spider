import pymysql
import requests
from lxml import etree
import time,random
import os

# 数据库连接
conn = pymysql.connect(host = "localhost",port = 3306,user = "root",
password = "sunck",charset="utf8",database = "yiliao")
cur = conn.cursor()
cur.execute("""drop table if exists data_me""")
conn.commit()
sqlc = """
CREATE TABLE data_me (
id int not null auto_increment,
med_name varchar(200) null,
url_01 varchar (200) null,
url_02 varchar (200) null,
url_03 varchar (200) null,
url_04 varchar (200) null,
url_05 varchar (200) null,
url_06 varchar (200) null,
url_07 varchar (200) null,
url_08 varchar (200) null,
url_09 varchar (200) null,
url_10 varchar (200) null,
primary key (`id`))
default character set = utf8;
"""
cur.execute(sqlc)
conn.commit()


# 获取事先爬好、检测了的代理ip
# with open("new_http.txt",encoding="utf-8") as file :
#     t0 = file.read()
#     s0 = t0.split(",")

def get_responses_data(branch_url):
    # 获取代理ip
    # i = random.randint(0,len(s0)-2)
    # proxies = {
    #     'http': s0[i]
    # }
    # requests 发送请求
    # get_response = requests.get(branch_url,proxies=proxies)
    get_response = requests.get(branch_url)
    # # 将返回的响应码转换成文本（整个网页）
    get_data = get_response.text
    #解析页面
    a = etree.HTML(get_data)
    return a

# 主页面
main_url = "http://www.med361.com"
# 发送请求
response_01 = get_responses_data(main_url)
# 不同医疗商品类别url
branch_url_1 = response_01.xpath('//*[@id="h3_list"]/div/div[1]/ul/li/a/@href')
branch_url_2 = response_01.xpath('//*[@id="h3_list"]/div/div[2]/ul/li/a/@href')
# 合并所有类别
branch_url = branch_url_1 + branch_url_2
# 将url处理成我们能直接访问的类型
for i in range(len(branch_url)):
    branch_url[i] = main_url + branch_url[i].replace('/..','')
# print(branch_url)

# 商品名称集
commodity_name = []
# 商品介绍图集
commodity_intr = []

for i in range(len(branch_url)):    #不同类别
    time.sleep(random.randint(1,3))
    response_02 = get_responses_data(branch_url[i])
    url_list_all = []
    # xpath获取所有单个商品url
    url_list = response_02.xpath('//*[@id="ddbd"]/form/dl/dd[2]/a/@href')
    # xpath获取所有翻页url
    url_paging = response_02.xpath('//*[@id="pager"]/a/@href')
    # 将翻页url处理成我们能直接访问的类型
    for j in range(len(url_paging)):
        url_paging[j] = main_url + url_paging[j].replace('/..','')
    # 将商品url处理成我们能直接访问的类型
    for j in range(len(url_list)):
        url_list[j] = main_url + url_list[j]
    url_list_all = url_list
    # 单个类别翻页
    for n in range(len(url_paging)):
        time.sleep(1)
        #发送请求
        response_03 = get_responses_data(url_paging[n])
        # Xpath 获取所有单个商品url
        url_list = response_03.xpath('//*[@id="ddbd"]/form/dl/dd[2]/a/@href')
        # 将商品url处理成我们能直接访问的类型
        for j in range(len(url_list)):
            url_list[j] = main_url + url_list[j]
        url_list_all = url_list_all + url_list  # 获取了单个类别所有的商品

    for m in range(len(url_list_all)):
        time.sleep(1)
        response_04 = get_responses_data(url_list_all[m])
        # 1.医疗器材名称（Medical equipment name）
        m_e_name = response_04.xpath('//*[@id="product-intro"]/ul/li[1]/h1/text()')[0].strip()
        commodity_name.append(m_e_name)  # 获得商品名称
        # 2.图片介绍(Picture introduction)
        picture_i = response_04.xpath('//*[@id="gallery"]/div/div/a/img/@src')
        for i in range(len(picture_i)):
            picture_i[i] = main_url + picture_i[i]
        while len(picture_i)<10:
            picture_i = picture_i + ['0']
        commodity_intr.append(picture_i)
        insert_sql = """
        insert into data_me(med_name,url_01,url_02,url_03,url_04,url_05,url_06,url_07,url_08,url_09,url_10) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        data_med = [commodity_name[m]]+[i for i in commodity_intr[m]]
        cur.execute(insert_sql,data_med)
        conn.commit()
cur.close()
conn.close()




# 文件下载存储到本地
# 下载图片函数
'''
folder_name : 文件夹名称，按图片简介
picture_address ： 一组图片的链接
'''
# def download_pictures(folder_name,picture_address):
#     file_path = r'F:\spider_project\testdata\{0}'.format(folder_name)
#     if not os.path.exists(file_path):
#         # 新建一个文件夹
#         os.mkdir(os.path.join(r'F:\spider_project\testdata',folder_name))
#     # 下载图片保存到新建文件夹
#     for i in range(len(picture_address)):
#         # 下载文件（wb,以二进制格式写入）
#         with open(r'F:\spider_project\testdata\{0}\0{1}.jpg'.format(folder_name,i+1),'wb') as f:
#             time.sleep(1)
#             # 根据下载链接，发送请求，下载图片
#             response = requests.get(picture_address[i])
#             f.write(response.content)


# 字段内容存储到`csv`文件
# 存储进CSV文件
'''
list_info : 存储内容列表
'''
# def file_do(list_info):
#     # 获取文件大小(先新建一个csv文件)
#     file_size = os.path.getsize(r'F:\medical.csv')
#     if file_size == 0:     # 只打印一次表头
#         # 表头
#         name = ['名称简介','url_01','url_02','url_03','url_04','url_05','url_06','url_07','url_08','url_09','url_10']
#         # 建立DataFrame对象
#         file_test = pd.DataFrame(columns=name, data=list_info)
#         # 数据写入
#         file_test.to_csv(r'F:\medical.csv', encoding='utf-8',index=False)
#     else:
#         with open(r'F:\medical.csv','a+',newline='') as file_test :
#             # 追加到文件后面
#             writer = csv.writer(file_test)
#             # 写入文件
#             writer.writerows(list_info)

