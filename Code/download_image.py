import re
import os
import urllib3
import requests
from lxml import etree
import time
from big_file_download import download


release_url = "http://bamboo.calix.local/artifact/IBAXOS192-CI/shared"

release_home_url = "http://bamboo.calix.local"

reg_release = r'<A HREF="(/artifact/IBAXOS192-CI/shared/build-.*)">build-.*</a>'

reg_image = r'<a href="/artifact/IBAXOS192-CI/shared/build-00533/FullRelease.run/FullRelease_system-E7-2_IB-AXOS-19.2_20190415175703_builder.run">FullRelease_system-E7-2_IB-AXOS-19.2_20190415175703_builder.run</a>'

path = "C:/wuyuan/FW/E7/19.2/"



class release_download():
    def get_url(self,url):
        html = requests.get(url)

        # print(html.status_code)

        text = html.text
        return text

    def find_latest_release_url(self, text):
        data = text

        release_list = re.findall(reg_release, data)
        print('the latest release (may not pass somke test) is', release_list[-1])

        latest_release_url = release_home_url + release_list[-1] + '/FullRelease.run'
        return latest_release_url


    def download_release(self,url):
        release_data = release.get_url(url)

        html = etree.HTML(release_data)

        image = html.xpath('//a/@href')

        image_name = html.xpath('//a')

        ###find image name
        for i in image_name:
            if 'FullRelease_system-E7-2' in i.text:
                print(i.text)
                image_name = i.text

        ###find image url
        for i in image:
            if 'FullRelease_system-E7-2' in i:
                print(i)

                image_url = release_home_url + i

                print(image_url, image_name)

                print('build found. please use command:', 'upgrade activate filename ftp://e7@10.245.37.200/19.2/%s password 1234' %image_name)

        print('downloading  image')
        # r = requests.get(image_url)
        # with open(path+image_name, "wb") as f:
        #     f.write(r.content)
        #
        # print('image download finished')
        download(image_url, path + image_name)








release = release_download()

if __name__ == '__main__':
    release = release_download()
    text = release.get_url(release_url)

    latest_image_url = release.find_latest_release_url(text)

    release.download_release(latest_image_url)


#
# def Schedule(a, b, c):
#     per = 100.0 * a * b / c
#     if per > 100:
#         per = 100
#     print('%.2f%%' % per)
#
# url = 'http://bamboo.calix.local/artifact/IBAXOS192-CI/shared/build-00534/FullRelease.run/FullRelease_system-E7-2_IB-AXOS-19.2_20190415190932_builder.run FullRelease_system-E7-2_IB-AXOS-19.2_20190415190932_builder.run'
# local = os.path.join('C:\python', 'FullRelease_system-E7-2_IB-AXOS-19.2_20190415190932_builder.run')
# urllib3.urlretrieve(url, local, Schedule)

