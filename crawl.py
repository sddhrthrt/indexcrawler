import sys
import os
import subprocess
from urllib import request
from urllib.error import HTTPError
import urllib.parse
import threading
import queue
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

queue = queue.Queue()
num_threads = 8 
sentinel = None

tmp_folder = "/home/thota/Downloads/HD"

def axelFile(queue):
    while True:
        item = queue.get()
        if item is sentinel:
            break
        (url, folder) = item
        
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                pass
        filename = urllib.parse.unquote(os.path.basename(url))
        if not os.path.exists(os.path.join(folder, filename)):
            subprocess.call(["axel", "-a",  "-n 120",
                         'http://%s'%(url, ),
                         "-o", '%s'%(tmp_folder, )])
            subprocess.call(["mv", os.path.join(tmp_folder, filename), folder])

        queue.task_done()


threads = [threading.Thread(target=axelFile, args = (queue, ))
            for i in range(num_threads)]

for t in threads:
    t.start()


class Crawler:
    def __init__(self, url, folder):
        self.url = url
        self.folder = folder

    
    def websiteStrip(self, url):
        url = url.lstrip(os.sep)
        rootdir = url[url.index(os.sep):] if os.sep in url else url
        return rootdir


    def getFolder(self, url):
        # gets a folder
        # without http://
        logger.info("getting folder: " + url)
        try:
            f=request.urlopen("http://" + url)
        except HTTPError as e:
            logger.error("Failed to fetch directory " + e)
            return 
        for i in f:
            words=str(i).split(' ')
            for word in words:
                if word.rfind('href')!=-1:
                    targeturl = word.lstrip('href="')
                    targeturl = targeturl.split('"')[0]
                    targeturl = os.path.join(url, targeturl)
                    self.process(targeturl)


    def process(self, url=None):
        if url is None:
            url = self.url
        logger.info("processing: " + url)
        if url.endswith('./') or url.endswith('../'):
            # it's folder up
            return
        if url.endswith('/'):
            # it's a folder
            self.getFolder(url)
        else:
            # it's a file
            folder = os.path.join(self.folder,
                                  os.path.dirname(
                                    self.websiteStrip(url).lstrip('/')) + '/')
            queue.put((url, folder))

    
if __name__ == "__main__":
    args = sys.argv 
    if len(args) < 3:
        print("\n"
              "Usage:\n"
              "%s url /target/folder [numthreads=4]\n"
              "\n"
              "(url is always assumed http://, dont add it)\n" % args[0])
        exit(0)

    url = args[1]
    folder = args[2]
    crawler = Crawler(url, folder)
    crawler.process()

    queue.join()
    for i in range(num_threads):
        queue.put(sentinel)

    for t in threads:
        t.join()

    logger.info("Done")
