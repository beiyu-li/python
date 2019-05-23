import re
import sys
import os
import urllib3
import requests
from lxml import etree
import time
import heapq
from download_image import release_download
import datetime
import time
from datetime import datetime, timedelta
from time import sleep
from big_file_download import download

release_home_url = "http://bamboo.calix.local"
release_url_19_2_smx = "http://bamboo.calix.local/browse/IBSMX192-CI/"
release_url_19_2_smx_candidate = 'http://bamboo.calix.local/browse/MBSMX192-CI'
release_tag = "/artifact/"
xpath_smx = """//*[@class="Successful"]/a"""
xpath_img = """//a[text()='install-activate.bin']"""
path = "C:/wuyuan/FW/E7/smx/"
reg_img_name = r'/browse/(IBSMX.*)'
reg_img_name1 = r'/(.*?.bin)'

SECONDS_PER_DAY = 24 * 60 * 60

def get_valid_image_list_and_download(text):
    valid_image_node1 = etree.HTML(text).xpath(xpath_smx)

    # print('smx img', valid_image_node1)

    valid_image_node1_list = []


    for item in valid_image_node1:
        # print(item.attrib)
        # print(item.xpath('@href'))
        valid_image_node1_list.append(item.xpath('@href')[0])
    print(valid_image_node1_list)


    common_list = valid_image_node1_list

    print('smx imag list is :%s' %common_list)

    if common_list !=[]:
        latest_valid_image_url= heapq.nlargest(1, common_list)[0]

        print(latest_valid_image_url)

        # img_name = re.findall(reg_img_name,latest_valid_image_url)
        #
        # img_name_full = 'install-activate-' + img_name[0] + '.bin'

        # print('img name is %s'% img_name_full)

        # print('valid image url:', latest_valid_image_url)

        full_latest_valid_image_url = release_home_url + latest_valid_image_url + release_tag

        print('valid image url:', full_latest_valid_image_url)

        html = requests.get(full_latest_valid_image_url)

        text = html.text

        img_url = etree.HTML(text).xpath(xpath_img)

        print('found image is %s'%img_url[0].xpath('@href'))

        download_img_url = release_home_url + img_url[0].xpath('@href')[0]
        print('download image is %s' % download_img_url)

        img_name1 = re.findall(reg_img_name1,download_img_url)

        print('img name1 is %s' % img_name1)

        img_name_full = img_name1[1]

        print(img_name_full)

        print('build found. please use ftp:', 'server ip 10.245.37.200 user smx  password 1234 file name %s' %img_name_full)

        print('downloading  image')
        download(download_img_url,path+img_name_full)



    else:
        print('no valid release found')









def download_seconds():
    curTime = datetime.now()
    print(curTime)
    desTime = curTime.replace(hour=6, minute=0, second=0, microsecond=0)
    print(desTime)
    delta = curTime - desTime
    print(delta)
    skipSeconds = SECONDS_PER_DAY - delta.total_seconds()
    # skipSeconds = SECONDS_PER_DAY - delta.total_seconds() + SECONDS_PER_DAY*4
    print("Next day must sleep %d seconds" % skipSeconds)
    sleep(skipSeconds)
    start_download()



def start_download():
    release = release_download()
    text = release.get_url(release_url_19_2_smx_candidate)
    #find valid image url list
    valid_image_url = get_valid_image_list_and_download(text)


if __name__ == '__main__':
    ###schedule doanload
    # download_seconds()

    ###download now
    start_download()

