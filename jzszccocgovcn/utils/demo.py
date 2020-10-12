import requests

url = "http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowImageServlet?action=displaypic&id=EFA191D7971CE9450C0443F593D4642B&pictype=1"
with open("1.jpg", "wb")as file:
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': "JSESSIONID=DA7CCA01EE6C36B8F8F7C8822CA8953B;",
        'Host': 'jzszc.coc.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'

    }
    content = requests.get(url, headers=headers).content
    file.write(content)