import requests
from bs4 import BeautifulSoup

'https://f1022.wonderfulday27.live/forumdisplay.php?fid=21'

def get(bbs_url):
    headers = {
        'Host': 'f1022.wonderfulday27.live',
        'User-Agent': '''Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:76.0)Gecko/20100101Firefox/76.0''',
        'Accept': '''text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        'Accept-Language':'''zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2''',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive',
        'Referer': 'https://f1022.wonderfulday27.live/index.php',
        'Cookie': '''__cfduid=db670b44508e77e4cc40f29cd0dd1db821601952834;CzG_sid=3h334R;__dtsu=51A016019528329BA9833197FE7E5479''',
        'Upgrade-Insecure-Requests':'1',
        'TE': 'Trailers'
    }
    base_url = 'https://f1022.wonderfulday27.live/'
    resp = requests.get(bbs_url, headers=headers)
    doc = resp.content.decode()
    soup = BeautifulSoup(doc, 'html.parser')
    page_url_set = set()
    page_url_list = list()
    for link in soup.find_all('a'):
        page_url = link.get('href')
        if 'viewthread' in page_url and is_real_page(page_url) and base_url+page_url not in page_url_set:
            page_url_list.append(base_url + page_url)
            page_url_set.add(base_url + page_url)
    return page_url_list
def is_real_page(url):
    if not url:
        return False
    li = url.split('&')
    if not li:
        return False
    if not li[-1]:
        return False
    if li[-1][:4] == 'page':
        return False
    if 'extra' in url:
        return True
    return False


def real(page_url):
    '''
    函数功能: 拿到具体页面的图片url, 返回具体的img_url_list
    :return:
    '''
    if not page_url:
        return []
    headers = {
        'Host': 'f1022.wonderfulday27.live',
        'User-Agent': '''Mozilla/5.0(WindowsNT10.0;Win64;x64;rv: 76.0) Gecko / 20100101Firefox / 76.0''',
        'Accept': '''text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        'Accept-Language': '''zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2''',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive',
        'Referer': 'https://f1022.wonderfulday27.live/forumdisplay.php?fid=21',
        'Cookie': '''__cfduid=db670b44508e77e4cc40f29cd0dd1db821601952834;CzG_sid=HPz4UU;__dtsu=51A016019528329BA9833197FE7E5479;CzG_visitedfid=21;__utma=93056010.1042757453.1601952922.1601952922.1601952922.1;__utmb=93056010.1.10.1601952922;__utmc=93056010;__utmz=93056010.1601952922.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);__utmt=1''',
        'Upgrade-Insecure-Requests': '1'
    }
    cont = requests.get(page_url, headers=headers)
    doc = cont.content.decode()
    soup = BeautifulSoup(doc, 'html.parser')
    # 缓存img_url的set
    img_url_set = set()
    # 真正存储img_url的list
    img_url_list = list()
    for link in soup.find_all('img'):
        img_url = link.get('file')
        if img_url and img_url not in img_url_set:
            img_url_list.append(img_url)
            img_url_set.add(img_url)
    return img_url_list

def download(img_url):
    with open(img_url.split('//')[-1], 'wb') as f:
        f.write(requests.get(img_url).content)

def main():
    url = 'https://f1022.wonderfulday27.live/forumdisplay.php?fid=21'
    bbs_urls = get(url)
    if not bbs_urls:
        exit()
    for bbs in bbs_urls:
        img_urls = real(bbs)
        if not img_urls:
            continue
        for i in img_urls:
            download(i)
main()