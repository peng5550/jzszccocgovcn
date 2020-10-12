from functools import partial
import aiohttp
import asyncio
import os
import psutil
import requests
from jzszccocgovcn.utils.login import loginProcessing
from lxml import etree
from jzszccocgovcn.utils.SqlConn import SQLConnection


IMAGEDATA = f"{os.path.dirname(__file__)}/IMAGE"
if not os.path.exists(IMAGEDATA):
    os.makedirs(IMAGEDATA)


class ReportProcessing:

    def __init__(self):
        self.login = loginProcessing()
        self.addCookieToHeaders()
        self.sql = SQLConnection()

    def addCookieToHeaders(self):
        cookies = self.login.llogin()
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'Host': 'jzszc.coc.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }

    async def downloadContent(self, semaphore, link):
        async with semaphore:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with await session.get(link) as resp:
                    content = await resp.text()
                    return content

    def itemProcessing(self, registerFlowId, future):

        html = etree.HTML(future.result())

        item = {
            "name": "".join(html.xpath(
                "//*[@id='name']/@value")),
            "gender": "".join(html.xpath(
                "//*[@id='sex']/option[@selected]/text()")),
            "nation": "".join(html.xpath(
                "//*[@id='nation']/option[@selected]/text()")),
            "email": "".join(html.xpath(
                "//*[@id='email']/@value")),
            "idType": "".join(html.xpath(
                "//*[@id='idtype']/option[@selected]/text()")),
            "idNo": "".join(html.xpath(
                "//*[@id='idnumber']/@value")),
            "phone": "".join(html.xpath(
                "//*[@id='phone']/@value")),
            "school": "".join(html.xpath(
                "//*[@id='school']/@value")),
            "major": "".join(html.xpath(
                "//*[@id='profession']/@value")),
            "education": "".join(html.xpath(
                "//*[@id='education']/option[@selected]/text()")),
            "degree": "".join(html.xpath(
                "//*[@id='degree']/option[@selected]/text()")),
            "graduation": "".join(html.xpath(
                "//*[@id='edu_gdate']/@value")),
            "companyNameNow": "".join([i for i in html.xpath(
                "//*[@id='enterpriseName']/@value") if i]),
            "companyNatureNow": "".join(html.xpath(
                "//*[@id='code_entnature']/option[@selected]/text()")),
            "companyRegistrationPlaceNow": "".join(html.xpath(
                "//*[@id='reg_place']/@value")),
            "companyLegalPersonNow": "".join(html.xpath(
                "//*[@id='legalperson']/@value")),
            "companyTypeNow": "".join(html.xpath(
                "//*[@id='code_enttype']/option[@selected]/text()")),
            "postNoNow": "".join(html.xpath(
                "//*[@id='zip']/@value")),
            "addressNow": "".join(html.xpath(
                "//*[@id='address']/@value")),
            "companyNameBefore": "".join(html.xpath(
                "//*[@id='oldenterpriseName']/@value")),
            "companyNatureBefore": "".join(html.xpath(
                "//*[@id='oldcode_entnature']/option[@selected]/text()")),
            "companyRegistrationPlaceBefore": "".join(html.xpath(
                "//*[@id='oldreg_place']/@value")),
            "companyLegalPersonBefore": "".join(html.xpath(
                "//*[@id='oldlegalperson']/@value")),
            "companyTypeBefore": "".join(html.xpath(
                "//*[@id='oldcode_enttype']/option[@selected]/text()")),
            "postNoBefore": "".join(html.xpath(
                "//*[@id='oldzip']/@value")),
            "addressBefore": "".join(html.xpath(
                "//*[@id='oldaddress']/@value")),
            "startDate": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[5]/tr[1]/td[2]/input/@value")),
            "endDate": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[5]/tr[1]/td[4]/input/@value")),
            "headImage": "".join(["http://jzszc.coc.gov.cn" + i for i in html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[1]/td[5]/img/@src")]),
            "signImage": "".join(
                ["http://jzszc.coc.gov.cn" + i for i in html.xpath("//img[@class='uploadedpic']/@src")]),
            "idCardImage": ", ".join(
                ["http://jzszc.coc.gov.cn" + i for i in html.xpath("//div[@class='toolsli_a']/img/@src")]),
            "registerFlowId": registerFlowId,
        }
        self.sql.conn.ping(reconnect=True)
        item_info = {"registerFlowId": item["registerFlowId"]}
        imageList = [(link, f"{IMAGEDATA}/{item['name'] + item['idNo'][-8:]}-{index}.jpg") for index, link in
                     enumerate([item["headImage"], item["signImage"]] + item["idCardImage"].split(", "))]

        if not self.sql.select_data(item_info=item_info):
            self.sql.insert_data(item_info=item)
            print("存储成功")
        else:
            print("已存在")

        self.downloadImage(imageList)

    def downloadImage(self, imageList):
        for link, path in imageList:
            if not os.path.exists(path):
                with open(path, "wb")as file:
                    content = requests.get(link, headers=self.headers).content
                    file.write(content)


    async def taskManager(self, linkList, func):
        tasks = []
        cpu_num = psutil.cpu_count()
        semaphore = asyncio.Semaphore(cpu_num)

        for link in linkList:
            task = asyncio.ensure_future(func(semaphore, link))
            task.add_done_callback(partial(self.itemProcessing, link))
            tasks.append(task)

        await asyncio.wait(tasks)

    def start(self):
        baseLink = "http://jzszc.coc.gov.cn/jsbZcgl/client/registrationReview/censor/goreport.htm?registerFlowId={}&processtypecode=02&sbzt=1&registerId=&examsCode%20="
        reportUrlList = [baseLink.format(i) for i in range(1, 3)]
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.taskManager(reportUrlList, self.downloadContent))



if __name__ == '__main__':
    app = ReportProcessing()
    app.start()
