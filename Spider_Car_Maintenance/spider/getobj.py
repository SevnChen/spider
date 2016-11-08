# -*- coding: utf-8
import cookielib
import urllib2
import urllib
import re
import chardet
from StringIO import StringIO
import gzip

class GetObj(object):

    def __init__(self,url):
        cookie_jar = cookielib.LWPCookieJar()
        cookie = urllib2.HTTPCookieProcessor(cookie_jar)
        self.opener = urllib2.build_opener(cookie)
        user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        self.url=url
        self.send_headers={'User-Agent':user_agent}

    def getcodeing(self,obj):
        if obj:
            coding=chardet.detect(obj)["encoding"]
            return coding

    def gethtml(self):
        try:
            request = urllib2.Request(self.url,headers=self.send_headers)
            request.add_header('Accept-encoding', 'gzip')
            response = urllib2.urlopen(request)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read())
                f = gzip.GzipFile(fileobj=buf)
                soures_home = f.read()
            else:
                soures_home = response.read()
        except urllib2.URLError,e:
            return None
        except urllib2.HTTPError,e:
            return None
        return soures_home