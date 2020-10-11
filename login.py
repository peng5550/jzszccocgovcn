from chaojiying import Chaojiying_Client
import requests


"请不要使用非法的URL地址访问"


USERNAME = "ziyougang"
PASSWORD = "Aa123456."
COOKIE_FILE = "./cookies.txt"
CAPTCHA_PATH = "./captcha.jpg"
HEADERS = {
    'Host': 'jzszc.coc.gov.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://jzszc.coc.gov.cn/jsbZcgl/link/index.do',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

class loginProcessing:

    def __init__(self):
        self.chaojiying = Chaojiying_Client("peng5550", "pengchao123", "1902")

    def visitHomepage(self):
        self.sess = requests.Session()
        self.sess.headers = HEADERS
        homepage = "http://jzszc.coc.gov.cn/jsbZcgl/client/enterpriseLogin/index.htm"
        self.sess.get(homepage)

    def downloadCaptchaImage(self):
        url = "http://jzszc.coc.gov.cn/jsbZcgl/servlet/ShowAuthMngImgServlet"
        with open(CAPTCHA_PATH, "wb")as file:

            content = self.sess.get(url).content
            file.write(content)

    def verifyCaptcha(self):
        with open(CAPTCHA_PATH, "rb")as f:
            img = f.read()

        result = self.chaojiying.PostPic(img, 1902)
        print(result)
        code = result.get("pic_str")
        pic_id = result.get("pic_id")

        return code, pic_id


    def llogin(self):
        self.visitHomepage()
        self.downloadCaptchaImage()
        code, pic_id = self.verifyCaptcha()
        loginUrl = "http://jzszc.coc.gov.cn/jsbZcgl/client/enterpriseLogin/login.htm"
        formData = {
            "uname": "7528F778604D3927767A257F1772C05A",
            "pword": "DECE9F39AA7C728E0C68DB9247ED6E68",
            "uname1": USERNAME,
            "pword1": PASSWORD,
            "yzm": code,
        }
        # print(formData)
        resp = self.sess.post(loginUrl, data=formData)
        # print(resp.text)
        # print('-'*100)
        response = self.sess.get("http://jzszc.coc.gov.cn/jsbZcgl/client/registrationReview/censor/goreport.htm?registerFlowId=1112344&processtypecode=02&sbzt=1&registerId=&examsCode%20=").text
        # print(response)
        if "刘东升" in response:
            cookies = self.sess.cookies.get_dict()
            # with open(COOKIE_FILE, "w+")as file:
            #     file.write(f"JSESSIONID={cookies['cookies']};")

            print("获取cookie成功")
            return f"JSESSIONID={cookies['JSESSIONID']};"
        print("登录失败")
        return




if __name__ == '__main__':
    app = loginProcessing()
    app.llogin()