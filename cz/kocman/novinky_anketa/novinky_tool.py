import urllib
from bs4 import BeautifulSoup
import re
import json
import os
import time

baseDir = 'inquiries'

def find_anktea(tag):
    return tag.has_attr('id') \
           and tag.has_attr('data-dot') \
           and tag['id'] == 'inquiries' \
           and tag['data-dot'] == 'hp_anketa'

def get_last_inquire():
    url_link = urllib.urlopen("http://www.novinky.cz")
    myfile = url_link.read()
    soup = BeautifulSoup(myfile, 'html.parser')
    prim_div = soup.find(find_anktea)
    div = prim_div.find('div')
    m = re.match(r'inquiry(\d+)',div['id'])
    if (not m):
        raise Exception("div pro Anketu zmenil svuj format! (ocekava se inquiry\d+, ziskano " + div['id'] + ")")
    return m.group(1)

def get_inquire(inquireId):
    url_link = urllib.urlopen("https://www.novinky.cz/inquiry/screen?inquiryIds=" + inquireId)
    myfile = url_link.read()
    myfile = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", myfile)
    data = json.loads(myfile)
    return data['inquiry'][0]

def add_or_create_inquire(inquire):
    inquireId = str(inquire['inquiryId'])
    if not os.path.exists(os.path.join(baseDir, inquireId)):
        f = open(os.path.join(baseDir, inquireId), 'w')
        f.write("# Otazka: " + inquire['title'].encode('utf-8') + '\n')
        f.write("# Mozne odpovedi: \n")
        for answer in inquire['answers']:
            f.write("#" + str(answer['answerId']) + ": " + answer['text'].encode('utf-8') + "\n")
        f.write("#" + "time" + '\t')
        for answer in inquire['answers']:
            f.write(str(answer['answerId']) + "[-]" + "\t")
        for answer in inquire['answers']:
            f.write(str(answer['answerId']) + "[%]" + "\t")
        f.write("\n")
    else:
        f = open(os.path.join(baseDir, inquireId), 'a')

    f.write(time.strftime('%Y-%m-%d %H:%M:%S') + "\t")
    for answer in inquire['answers']:
        f.write(str(answer['voteCount']) + "\t")
    for answer in inquire['answers']:
        f.write(str(answer['pc']) + "\t")
    f.write("\n")
    f.close()
