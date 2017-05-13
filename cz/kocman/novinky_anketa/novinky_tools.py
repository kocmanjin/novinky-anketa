import urllib
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from bs4 import Tag
import re


def find_anktea(tag):
    return tag.has_attr('id') \
           and tag.has_attr('data-dot') \
           and tag['id'] == 'inquiries' \
           and tag['data-dot'] == 'hp_anketa'

url_link = urllib.urlopen("http://www.novinky.cz")
myfile = url_link.read()
soup = BeautifulSoup(myfile, 'html.parser')
prim_div = soup.find(find_anktea)
div = prim_div.find('div')
m = re.match(r'inquiry(\d+)',div['id'])
if (not m):
    raise Exception("div pro Anketu zmenil svuj format! (ocekava se inquiry\d+, ziskano " + div['id'] + ")")
print(m.group(1))
