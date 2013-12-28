import os
import socket
import urllib2
import bs4


def tr(string):
    return string


class Parser:
    baseUrl = ""
    chaptersPage = ""
    chapterItemSelector="" #css selector for chapter item link
    chapterItemAttr = ""
    chapterNameSelector=""
    chapterNameAttr=""
    pageItemSelector = ""
    pageItemSelectorAttr = ""
    imageItemSelector = "";
    imageItemSelectorAttr = "";
    userAgent = tr("Opera/9.80 (X11; Linux x86_64) Presto/2.12.388 Version/12.15")
    debugLevel = 0
    encoding = 'utf-8'
    timeout = 30

    def __init__(self):
        pass

    def getPath(self, path):
        return self.baseUrl + path;

    # return list of hrefs
    def getChapters(self, name):
        s = self.getPage(self.chaptersPage + name)
        soup = bs4.BeautifulSoup(s)
        li = soup.select(self.chapterItemSelector)

        hrefs = list(item[self.chapterItemAttr].replace(self.baseUrl, "") for item in li) # make hrefs list

        return hrefs

    def getPagesList(self, chapterPage):
        s = self.getPage(chapterPage)

        soup = bs4.BeautifulSoup(s)
        li = soup.select(self.pageItemSelector)

        hrefs = list(item[self.pageItemSelectorAttr].replace(self.baseUrl, "") for item in li) # make hrefs list

        return hrefs

    def getImagesList(self, imagesPage):
        s = self.getPage(imagesPage)
        soup = bs4.BeautifulSoup(s)
        li = soup.select(self.imageItemSelector)

        hrefs = list(item[self.imageItemSelectorAttr].replace(self.baseUrl, "") for item in li) # make hrefs list

        return hrefs

    def getImageName(self, path):
        return os.path.basename(path)


    def getPageBytes(self, path, addDomen = 1):
        if addDomen:
            url = self.getPath(path);
        else:
            url = path;

        h = urllib2.HTTPHandler(debuglevel=self.debugLevel)
        opener = urllib2.build_opener(h)

        request = urllib2.Request(url);
        request.add_header('User-Agent', self.userAgent)
        if self.debugLevel == 1:
            print tr('trying to connect to "%s"' % path)

        try:
            response = opener.open(request, timeout = self.timeout)
        except urllib2.URLError, e:
            raise Exception (tr("There was an error: %r") % e)
        except socket.timeout, e:
            raise Exception (tr("Socket timeout: %r") % e)

        return response.read()

    # return page in the specific encoding of self.encoding
    def getPage(self, path):
        response = self.getPageBytes(path);
        return response.decode(encoding=self.encoding)

