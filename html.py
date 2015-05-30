import re
import os

from bs4 import BeautifulSoup

def rehtml():
    f = os.getcwd() + '/' + 'test.html'
    fp = open(f, 'r')
    text = fp.read()
    fp.close()
    text = text.replace("\\",'')
    #<strong node-type="follow">2</strong>
    #follow _ fans number
    p = re.compile('<strong node-type="follow">(\d+)</strong>')
    p1 = re.compile('<strong node-type="fans">(\d+)</strong>')
    num = p1.search(text).group(1)
    print 'p_num', num
    #p = re.compile('<li class="S_line1"><a bpfilter="page_frame" href=\"(.*?)follow')
    #yonghu!!!
    # p = re.compile('uid=(\d+)&profile')
    # url = p.findall(text)
    # print url
if __name__ == "__main__":
    rehtml()