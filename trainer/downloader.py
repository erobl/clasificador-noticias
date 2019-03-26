from goose3 import Goose
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
from collections import namedtuple
import socket

# timeout in seconds
timeout = 1
socket.setdefaulttimeout(timeout)

DownloadResult = namedtuple("DownloadResult", "netloc text")

class Downloader():
    def __init__(self):
        self.g = Goose({'use_meta_language': False, 'target_language':'es', 'browser_user_agent': 'Mozilla', 'parser_class':'soup'})

        self.ignore = ["www.facebook.com", "www.monumental.co.cr", "www.diarioextra.com", "www.laprensalibre.cr", "www.elfinancierocr.com"]

    def process(self, doc):
        url = doc["link"]
        print(url)
        try:
            if urlparse(url).netloc not in self.ignore:
                with urllib.request.urlopen(url) as response:
                    netloc = urlparse(response.url).netloc
                    html = response.read()
            else:
                netloc = urlparse(url).netloc
        except:
            print("Error descargando url:", doc["link"])
            return DownloadResult(None, None)

        if netloc == "www.nacion.com":
            return DownloadResult(netloc, self.scrapeln(html))
        elif netloc == "www.crhoy.com":
            return DownloadResult(netloc, self.scrapegoose(url))
        elif netloc == "www.teletica.com":
            return DownloadResult(netloc, self.scrapegoose(url))
        elif netloc == "semanariouniversidad.com":
            return DownloadResult(netloc, self.scrapegoose(url))
        elif netloc == "www.facebook.com":
            print("Error: Link a facebook en el objeto", doc["_id"])
            # loguear a un archivo
            with open("facebook.txt", "a") as file:
                file.write(str(doc))
            return DownloadResult(netloc, None)
        else:
            print("Error: URL no conocido", netloc)
            return DownloadResult(netloc, None)


    def scrapeln(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return " ".join([s.text for s in soup.findAll("p", {"class": "element element-paragraph"})])

    def scrapegoose(self, url):
        return self.g.extract(url=url).cleaned_text
