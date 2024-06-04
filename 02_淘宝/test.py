from DrissionPage.common import Actions
import DrissionPage
import json
import re


keywords = ''
page = 5
username = ''
password = ''

page = DrissionPage.ChromiumPage()
page.get('https://login.taobao.com/member/login.jhtml')

# 登陆
if page.ele("xpath: //input[@name='fm-login-id']"):
    page.ele("xpath: //input[@name='fm-login-id']").input(username, clear=True)
    page.ele("xpath: //input[@name='fm-login-password']").input(password)
    page.ele("xpath: //div[@class='fm-btn']/button").click()

 
# 验证码滑块  自动化过不了大概率 最好手动操作
if page.ele("xpath: //span[@aria-label='滑块']"):
    page.wait(2)
    ele1 = page.ele("xpath: //div[@id='nc_1_n1t']/span[@aria-label='滑块']")
    size = page.ele("xpath: //div[@id='nocaptcha']").rect.size
    ele1.hover()
    ele1.drag(size[0], 0 , 1)
    page.wait(2)
    page.ele("xpath: //div[@class='fm-btn']/button").click()

page.wait(2,5)
page.ele("xpath: //div[@class='site-nav-new-home']").click()


page.ele("xpath: //input[@id='q']").input(keywords)
page.ele("xpath: //button[@class='btn-search tb-bg']").click()


# 开始监听请求
page.listen.start('/mtop.relationrecommend.wirelessrecommend.recommend/2.0/')

# 点击下一页
for _ in range(page):
    page.ele("xpath: //span[@class='next-btn-helper' and contains(text(), '下一页')]").click()
    page.wait(3)

# 获取数据 
count = 1
for packet in page.listen.steps():
    data = json.loads(re.findall("mtopjson.*?\((.*)\)", packet.response.body)[0])['data']['itemsArray']
    for item in data:
        title = item['title'].replace('<span class=H>', '').replace("</span>", '').replace(" ", '')
        shopName = item['shopInfo']['title']
        price = item['priceShow']['unit'] + item['priceShow']['price']
        detailUrl = item['auctionURL']
        print('{}  {}  {}  {}'.format(count, title, price, shopName))
        count += 1 
