# -*- coding: utf-8 -*-
import scrapy
from jzszccocgovcn.items import JzszccocgovcnItem


class JzszcSpider(scrapy.Spider):
    name = 'jzszc'

    def start_requests(self):
        for i in range(1, 20):
            link = f"http://jzszc.coc.gov.cn/jsbZcgl/client/registrationReview/censor/goreport.htm?registerFlowId={i}&processtypecode=02&sbzt=1&registerId=&examsCode%20="
            yield scrapy.Request(link, meta={"registerFlowId": i}, dont_filter=True, callback=self.detail_page)

    def detail_page(self, response):
        item = JzszccocgovcnItem()
        registerFlowId = response.meta["registerFlowId"]
        item["data"] = {
            "name": response.xpath("//*[@id='name']/@value").extract_first(""),
            "gender": response.xpath("//*[@id='sex']/option[@selected]/text()").extract_first(""),
            "nation": response.xpath("//*[@id='nation']/option[@selected]/text()").extract_first(""),
            "email": response.xpath("//*[@id='email']/@value").extract_first(""),
            "idType": response.xpath("//*[@id='idtype']/option[@selected]/text()").extract_first(""),
            "idNo": response.xpath("//*[@id='idnumber']/@value").extract_first(""),
            "phone": response.xpath("//*[@id='phone']/@value").extract_first(""),
            "school": response.xpath("//*[@id='school']/@value").extract_first(""),
            "major": response.xpath("//*[@id='profession']/@value").extract_first(""),
            "education": response.xpath("//*[@id='education']/option[@selected]/text()").extract_first(""),
            "degree": response.xpath("//*[@id='degree']/option[@selected]/text()").extract_first(""),
            "graduation": response.xpath("//*[@id='edu_gdate']/@value").extract_first(""),
            "companyNameNow": response.xpath("//*[@id='enterpriseName']/@value").extract_first(""),
            "companyNatureNow": response.xpath("//*[@id='code_entnature']/option[@selected]/text()").extract_first(""),
            "companyRegistrationPlaceNow": response.xpath("//*[@id='reg_place']/@value").extract_first(""),
            "companyLegalPersonNow": response.xpath("//*[@id='legalperson']/@value").extract_first(""),
            "companyTypeNow": response.xpath("//*[@id='code_enttype']/option[@selected]/text()").extract_first(""),
            "postNoNow": response.xpath("//*[@id='zip']/@value").extract_first(""),
            "addressNow": response.xpath("//*[@id='address']/@value").extract_first(""),
            "companyNameBefore": response.xpath("//*[@id='oldenterpriseName']/@value").extract_first(""),
            "companyNatureBefore": response.xpath("//*[@id='oldcode_entnature']/option[@selected]/text()").extract_first(""),
            "companyRegistrationPlaceBefore": response.xpath("//*[@id='oldreg_place']/@value").extract_first(""),
            "companyLegalPersonBefore": response.xpath("//*[@id='oldlegalperson']/@value").extract_first(""),
            "companyTypeBefore": response.xpath("//*[@id='oldcode_enttype']/option[@selected]/text()").extract_first(""),
            "postNoBefore": response.xpath("//*[@id='oldzip']/@value").extract_first(""),
            "addressBefore": response.xpath("//*[@id='oldaddress']/@value").extract_first(""),
            "startDate": response.xpath("//*[@id='ldhtyxqstart']/@value").extract_first(""),
            "endDate": response.xpath("//*[@id='ldhtyxqend']/@value").extract_first(""),
            "headImage": "".join(["http://jzszc.coc.gov.cn" + i for i in response.xpath("//div[@class='ibox-content']/div[@class='reg_info_left']/table[1]/tr[1]/td[5]/img/@src").extract()]),
            "signImage": "".join(["http://jzszc.coc.gov.cn" + i for i in response.xpath("//img[@class='uploadedpic']/@src").extract()]),
            "idCardImage": ", ".join(["http://jzszc.coc.gov.cn" + i for i in response.xpath("//div[@class='toolsli_a']/img/@src").extract()]),
            "registerFlowId": registerFlowId,
        }
        yield item
