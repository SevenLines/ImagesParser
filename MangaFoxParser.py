#!/usr/bin/python
# http://mangafox.me

import argparse
import os
from time import sleep

import urllib2
import re
import bs4
import socket
from Parser import Parser
from Parser import tr

class MangaFox(Parser):
    baseUrl = "http://mangafox.me/"
    chaptersPage = "manga/"
    chapterItemSelector = ".chlist a.tips"
    chapterItemAttr = "href"
    pageItemSelector = "#top_bar option"
    pageItemSelectorAttr = "value"
    imageItemSelector = "#image"
    imageItemSelectorAttr = "src"

    def getChapters(self, name):
        hrefs = Parser.getChapters(self, name);
        hrefs.reverse();
        return hrefs;

    def getImageName(self, path):
        path = Parser.getImageName(self, path);
        return path.split('?')[0];

    def getPagesList(self, chapterPage):
        prefix = '/'.join(chapterPage.split('/')[:-1]) + '/'
        pages = Parser.getPagesList(self, chapterPage)
        pages = list(prefix + p + '.html' for p in pages)
        return  pages

 
def main():

    # parse command line args
    parser = argparse.ArgumentParser()

    parser.add_argument('mangaName', help="name of manga as it is in url line", type=str)
    parser.add_argument('--outputDir', '-o', metavar="", help='output dir, by default: .', default='.', type=str)
    parser.add_argument('--firstChapter', '-f', metavar="",
                        help='the first chapter for download in the order as it appears on site', default=1, type=int)
    parser.add_argument('--lastChapter', '-l', metavar="", help='the last chapter for download', default=-1, type=int)

    args = parser.parse_args()

    # assign args
    firstChapter = args.firstChapter
    lastChapter = args.lastChapter
    savePath = args.outputDir

    # create site parser
    mangaFox = MangaFox()

    #get chapters list
    chapters = mangaFox.getChapters(args.mangaName)

    # recalculate chapter list
    if lastChapter != -1:
        lastChapter = min(lastChapter, len(chapters))
    else:
        lastChapter = len(chapters)

    # assign chapter counter
    counter = 1

    # itterate over chapters
    for chapter in chapters:

        if  counter > lastChapter:
            break

        # skipping some chapters if nessacery
        if counter >= firstChapter:

            pages = mangaFox.getPagesList(chapter)
            chapterName = '/'.join(chapter.split('/')[1:-1])
            saveDir = str.format('{0}/{1}', savePath, chapterName)

            # create dirs
            if not os.path.exists(saveDir):
                os.makedirs( saveDir )

            pCounter = 1;
            for page in pages:
                # inform user
                print(str.format("[{0}/{1}] - [{2}/{3}]",
                                 counter - firstChapter + 1,
                                 lastChapter - firstChapter + 1,
                                 pCounter,
                                 len(pages)))

                # get image url
                imageUrl = mangaFox.getImagesList(page)[0]
                saveName = mangaFox.getImageName(imageUrl)

                # build file name
                saveName = str.format('{0:03d}{1}', pCounter, os.path.splitext(saveName)[-1])
                saveName = saveDir + '/' + saveName

                # get image data
                imageData = mangaFox.getPageBytes(imageUrl, 0);

                # write file to disk
                file = open(saveName, 'wb')
                file.write(imageData)
                file.close()

                # inform user
                print(str.format(tr('save file to: "{0}"'), saveName))

                # sleep a bit
                print(tr('sleep 1 sec'))
                sleep(1)

                pCounter+=1
        counter += 1

    print tr("parsing ended! ^_^")


if __name__ == '__main__':
    main()
