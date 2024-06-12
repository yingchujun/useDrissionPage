import DrissionPage
import base64
import json
import re
from io import BytesIO
from PIL import Image
import cv2
import random

# 判断缺口位置 返回缺口的X坐标
def identify_gap(bg,tp,out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg) # 背景图片
    tp_img = cv2.imread(tp) # 缺口图片
    
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
    
    # 绘制方框
    th, tw = tp_pic.shape[:2] 
    tl = max_loc # 左上角点的坐标
    br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
    cv2.imwrite(out, bg_img) # 保存在本地
    
    # 返回缺口的X坐标
    return tl[0] 

# 调整图片大小并保存
def resize_and_save_image(path,content, size):
    '''
    path: 图片路径
    content: 图片数据
    size: 图片大小(元组)
    '''
    image = Image.open(BytesIO(content))
    image = image.resize(size)
    image.save(path)



keywords = 'python'
page = 5
username = '15888888888'
password = '123465'

page = DrissionPage.ChromiumPage()
page.get('https://passport.jd.com/new/login.aspx')

page.run_cdp('Storage.clearCookies')
page.get('https://passport.jd.com/new/login.aspx')


# 开始监听请求
page.listen.start(['https://iv.jd.com/slide/g.html?appId=1604ebb2287&scene=login&product=click-bind-suspend', 'https://iv.jd.com/slide/s.html'])

# 登陆
if page.ele("xpath: //input[@id='loginname']"):
    page.ele("xpath: //input[@id='loginname']").input(username, clear=True)
    page.ele("xpath: //input[@id='nloginpwd']").input(password)
    page.ele("xpath: //div[contains(@class, 'login-btn')]").click()


def base64_to_img(bstr, file_path):
    imgdata = base64.b64decode(bstr)
    file = open(file_path, 'wb')
    file.write(imgdata)
    file.close()


# 获取数据 
count = 1
for packet in page.listen.steps():

    if '/slide/s.html' in packet.response.url:
        if json.loads(re.findall("jsonp_\d+\((.*)\)", packet.response.body)[0])['message'] == 'success':
            print('登录成功, 在此执行登陆后的操作')


        continue
    else:
        print(f'第 { count } 次尝试')

    data = json.loads(re.findall("jsonp_\d+\((.*)\)", packet.response.body)[0])
    patch = data['patch']
    bg = data['bg']

    resize_and_save_image('patch.png', base64.b64decode(patch), (33,33))
    resize_and_save_image( 'bg.png', base64.b64decode(bg), (242, 94))

    x = identify_gap('bg.png','patch.png',  'result.png')
    page.actions.move_to("xpath: //div[@class='JDJRV-slide-inner JDJRV-slide-btn']").click().hold().move(x-1, random.randint(1,20), random.randint(1,2)).release()
    page.wait(random.randint(1,2))
    count += 1
