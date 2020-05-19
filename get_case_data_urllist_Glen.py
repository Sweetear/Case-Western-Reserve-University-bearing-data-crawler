'''
Crawler for CWRU data

Author: hp
From:
    http://hp.stuhome.net/index.php/2017/11/03/case-western-reserve-university-bearing-data-center-crawler/
    https://github.com/callofdutyops/Case-Western-Reserve-University-bearing-data-crawler

Modified by Glen on 15 May 2020
New added: download the mat file from url and save as name of situation

'''

import requests as rq
from lxml import etree
import os
import urllib

DATA_URL = "http://csegroups.case.edu/bearingdatacenter/pages/download-data-file"
SAVE_DIR = "C:\\Users\\Glen\\Desktop\\Z_Cardiff\\Research\\dataset\\Case-Western-Reserve-University-bearing-data-crawler-master"


def get_content(url, pattern):
    html = rq.get(url).text
    selector = etree.HTML(html)
    content = selector.xpath(pattern)
    return content


def mkdir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def write_file(file_name, text):
    with open(file_name, "wt") as f:
        for t in text:
            print(t, file=f)


def get_text_url_pair(content):
    pairs = []
    for c in content:
        # Use '_' instead of ' '(space) because this is more friendly to shell scipt
        text = "_".join(c.text.split())
        url = c.attrib["href"]
        pairs.append((text, url))
    return pairs


def main():
    content = get_content(DATA_URL, "//span/a")
    dir_pairs = get_text_url_pair(content)
    for p in dir_pairs:
        text = []
        folder_path = os.path.join(SAVE_DIR, p[0])
        mkdir(folder_path)
        content = get_content(p[1], "//span/a")
        data_pairs = get_text_url_pair(content)
        # Aria2 download list
        for file_name, url in data_pairs:
            text.append(url)
            text.append("  dir=" + folder_path)
            text.append("  out=" + file_name)
            write_file(os.path.join(folder_path, "url.txt"), text)
            
            # new added: download mat file and save as name of situation
            print('downloading {}'.format(file_name))
            new_file_name = folder_path + '\\'+ file_name + '.mat'
            urllib.request.urlretrieve(url, new_file_name)

if __name__ == "__main__":
    main()
