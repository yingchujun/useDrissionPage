import DrissionPage



page = DrissionPage.ChromiumPage()
page.get('http://www.fangdi.com.cn/index.html')
page.ele("xpath: //div[contains(@class, 'menu_wrapper')]/a[contains(text(), '一手房')]").click()
page.wait(2)
page.ele("xpath: /html//div[1]/div[3]/div/div[3]/div[1]/div[2]/h6/a").click()
page.wait(2)

uls =  page.eles("xpath: //table[@class='layui-table']/tbody/tr")
for ul in uls:
    status = ul.ele("xpath: ./td[1]//text()")
    projectName = ul.ele("xpath: ./td[2]//text()")
    projectAddress = ul.ele("xpath: ./td[3]//text()")
    totul = ul.ele("xpath: ./td[4]//text()")
    area = ul.ele("xpath: ./td[5]//text()")
    position = ul.ele("xpath: ./td[6]//text()")
    print(status, projectName, projectAddress, totul, area, position)