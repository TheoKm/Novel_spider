import requests
import re
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
list_url = 'http://www.haotxt.com/xiaoshuo/'

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
}
def get_page(url):

    response = requests.get(url,headers=headers)
    try:
        if response.status_code == 200 :
            response.encoding=response.apparent_encoding
            return response.text
    except requests.ConnectionError as e:
        print('Error',e.args)

def parse_one_page(html,name):
    if html != None:
        soup = BeautifulSoup(html, 'lxml')
        if soup:
            fout = open(name + '.txt', 'a+', encoding='utf-8')
            for h1 in soup.select('h1'):
                fout.write("\n" + h1.text + "\n")
            for content in soup.select('#content'):
                fout.write(content.text)
            fout.close()

def get_noval_chapter_url(html,url_):
    soup = BeautifulSoup(html, 'html.parser')
    fail_num = 0
    if soup:
        urls = []
        for a in soup.select('.ccss a'):
            name = soup.select('h1')[0].text
            urls.append(url_ + a.attrs['href'])
        content = re.search('.*/(.*).html', urls[0], re.S)
        i = 0
        for url in urls:
            urls[i] = (url_ + str(int(content.group(1)) + i) + '.html')
            i = i + 1
        return urls, name
    else:
        fail_num = fail_num+1
        print('One chapter parse the error and parse the errors:'+fail_num+'.')

def get_noval_list_url(url):
    urls = []
    i = 0
    list_len = 25576
    while i<=list_len:
        urls.append(list_url+str(int(i/1000))+'/'+str(i)+'/')
        i = i+1
    return urls

def main(url):
    html = get_page(url)
    Urls, name = get_noval_chapter_url(html,url)
    for Url in Urls:
        i = 1
        html = get_page(Url)
        parse_one_page(html, name)
        print('Successfully parse '+str(i)+'chapter.')
        i = 1 + i
    print('Successfully parse a novel.')

if __name__ == '__main__':
    urls = get_noval_list_url(list_url)
    pool = Pool(20)
    pool.map(main,urls)
    pool.close()
    pool.join()
