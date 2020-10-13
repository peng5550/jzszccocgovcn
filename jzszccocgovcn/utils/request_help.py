# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl

def print_headers_raw_to_dict(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" +
        "': '".join(s.strip().split(': ')) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_headers_raw_to_dict_space(headers_raw_l):
    print("{\n    '" + ",\n    ".join(map(lambda s: "'" + "': '".join(s.strip().split('\t')) + "'", headers_raw_l))[1:-1] + "'\n}")

def print_dict_from_copy_headers(headers_raw):
    headers_raw = headers_raw.strip()
    headers_raw_l = headers_raw.splitlines()

    if ':' in headers_raw_l[0]:
        print_headers_raw_to_dict(headers_raw_l)
    else:
        print_headers_raw_to_dict_space(headers_raw_l)

def print_url_params(url_params):
    s = str(parse_qsl(url_params.strip(), 1))
    print("OrderedDict(\n    " + "),\n    ".join(map(lambda s: s.strip(), s.split("),")))[1:-1] + ",\n)")

if __name__ == '__main__':
    header_text = '''
Host: cjrk.hbcic.net.cn
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: FSSBBIl1UgzbN7NS=5QUWPrQ.TJsbsW1I2WGE79QbKBJVsxx2WLSu5uGjEdoag7FWtrqqXOwVYnpv2JR3_VqZHPbpMBKWMLzok962lga; FSSBBIl1UgzbN7NT=5UgH6F25keCLqqqmTDgWtaA91wTkFsugelFI8rI4mm_NJRMc47dGRu7LSTD.gggO3A0IeWwtHBp3jO_oAH6aBOqHtKTF0nBIiFIQd4a9jU_psn7rJVX31rPTWX1tI6WMylHnPtxiAmAgIvzjJY9bo7_L0CktVzj8lGUnxgaLqEvWdksJbDCKc.HgFPcYb9_gex2Dp6d_uce5IOE6ncJAK61QPrYXQntWSjbAPuQRBgFDW4Jk.sTLY.hVrSqVCC1IxtNoeNbuMWKAD65Qhp5..Rv




'''

    print_dict_from_copy_headers(header_text)



