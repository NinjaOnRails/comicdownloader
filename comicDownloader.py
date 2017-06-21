#! python3
# comicDownloader.py -Checks web comics sites and automatically
# downloads new images.

import os, threading, requests, bs4
    
def checkSite1():
    count = 0
    lastImage1 = open('lastImg1.txt')
    lastContent1 = lastImage1.read()
    url1 = 'http://www.lefthandedtoons.com'
    print('Downloading page %s...' % url1)
    res = requests.get(url1)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    comicElem = soup.select('.comicimage')
    if comicElem[0].get('alt') == lastContent1:
        print('No new images found on %s' % url1)
        lastImage1.close()
    else:
        alt = comicElem[0].get('alt')
        lastImage1 = open('lastImg1.txt', 'w')
        lastImage1.write(alt)
        lastImage1.close()
        while alt != lastContent1:            
            comicUrl = comicElem[0].get('src')
            try:
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()
            except requests.exceptions.MissingSchema:
                prevLink = soup.select('.prev a')[0]
                url1 = 'http://www.lefthandedtoons.com' + prevLink.get('href')
                continue
            imageFile = open(os.path.join('/Users/hoangvu/Desktop', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            count += 1
            prevLink = soup.select('.prev a')[0]
            url1 = 'http://www.lefthandedtoons.com' + prevLink.get('href')
            print('Downloading page %s...' % url1)
            res = requests.get(url1)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "lxml")
            comicElem = soup.select('.comicimage')
            alt = comicElem[0].get('alt')
        print('New images downloaded from lefthandedtoons.com: %s.' % count)
    return count


def checkSite2():
    count = 0
    lastImage2 = open('lastImg2.txt')
    lastContent2 = lastImage2.read()
    url2 = 'http://buttersafe.com'
    print('Downloading page %s...' % url2)
    res = requests.get(url2)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    comicElem = soup.select('#comic img')
    if comicElem[0].get('alt') == lastContent2:
        print('No new images found on %s.' % url2)
        lastImage2.close()
    else:
        alt = comicElem[0].get('alt')
        lastImage2 = open('lastImg2.txt', 'w')
        lastImage2.write(alt)
        lastImage2.close()
        while alt != lastContent2:
            comicUrl = comicElem[0].get('src')
            try:
                print('Downloading image %s...' % (comicUrl))
                res = requests.get(comicUrl)
                res.raise_for_status()
            except requests.exceptions.MissingSchema:
                prevLink = soup.select('a[rel="prev"]')[0]
                url2 = prevLink.get('href')
                continue
            imageFile = open(os.path.join('/Users/hoangvu/Desktop', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
            count += 1
            prevLink = soup.select('a[rel="prev"]')[0]
            url2 = prevLink.get('href')
            print('Downloading page %s...' % url2)
            res = requests.get(url2)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "lxml")
            comicElem = soup.select('#comic img')
            alt = comicElem[0].get('alt')
        print('New images downloaded from buttersafe.com: %s.' % count)
    return count

threadObj1 = threading.Thread(target=checkSite1)
threadObj2 = threading.Thread(target=checkSite2)
threadObj1.start()
threadObj2.start()
threadObj1.join()
threadObj2.join()
print('Finished.')
