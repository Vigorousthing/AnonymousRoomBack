from bs4 import BeautifulSoup
from urllib.request import urlopen
#
# url = 'http://daum.net'
# # url = 'http://naver.com'
# # url = 'http://twitter.com'
# html = urlopen(url)
# bs = BeautifulSoup(html, 'html.parser')
#
# # for meta in bs.head.find_all('meta'):
# #     # print(meta.get('name'))
# #     print(meta)
# # image = bs.head.find('meta', {'name': 'twitter:image'}).get('content')
# # description = bs.head.find('meta', {'name': 'description'}).get('content')
# # print(image)
# # print(description)
# # title = bs.find('meta', property='og:title')['content']
# # image = bs.find('meta', property='og:image')['content']
# title = bs.find('title')
# image = bs.find('image')
#
# print(title, image)


class A:
    def __init__(self, name):
        self.name = name
        self.a = 1


c = A("abc")





