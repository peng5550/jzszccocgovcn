from functools import partial
import aiohttp
import asyncio
import os
import psutil
import requests
from login import loginProcessing
from lxml import etree
from SqlConn import SQLConnection



IMAGEDATA = f"{os.path.dirname(__file__)}/IMAGE"
if not os.path.exists(IMAGEDATA):
    os.makedirs(IMAGEDATA)


class ReportProcessing:

    def __init__(self):
        self.login = loginProcessing()
        self.headers = self.addCookieToHeaders()
        self.sql = SQLConnection()

    def addCookieToHeaders(self):
        cookies = self.login.llogin()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': cookies,
            'Host': 'jzszc.coc.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
        return headers

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
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[1]/td[2]/input/@value")),
            "gender": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[1]/td[4]/select/option[@selected]/text()")),
            "nation": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[2]/td[2]/input/@value")),
            "email": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[2]/td[4]/input/@value")),
            "idType": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[3]/td[2]/input/@value")),
            "idNo": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[3]/td[4]/input/@value")),
            "phone": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[4]/td[2]/input/@value")),
            "school": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[2]/tr[1]/td[2]/div/input/@value")),
            "major": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[2]/tr[1]/td[4]/input/@value")),
            "education": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[2]/tr[2]/td[2]/input/@value")),
            "degree": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[2]/tr[2]/td[4]/input/@value")),
            "graduation": "".join(html.xpath(
                "//div[@class='ibox-content']/div[@class='reg_info_left']/table[2]/tr[3]/td[2]/input/@value")),
            "companyNameNow": "",
            "companyNatureNow": "",
            "companyRegistrationPlaceNow": "",
            "companyLegalPersonNow": "",
            "companyTypeNow": "",
            "postNoNow": "",
            "addressNow": "",
            "companyNameBefore": "",
            "companyNatureBefore": "",
            "companyRegistrationPlaceBefore": "",
            "companyLegalPersonBefore": "",
            "companyTypeBefore": "",
            "postNoBefore": "",
            "addressBefore": "",
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
        print(item)
        print('-' * 100)
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
