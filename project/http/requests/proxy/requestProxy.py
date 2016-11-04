import sys
import os
sys.path.insert(0, os.path.abspath('../../../../'))
from project.http.requests.parsers.freeproxyParser import freeproxyParser
from project.http.requests.parsers.proxyforeuParser import proxyforeuParser
from project.http.requests.parsers.rebroweeblyParser import rebroweeblyParser
from project.http.requests.parsers.samairproxyParser import semairproxyParser
from project.http.requests.useragent.userAgent import UserAgentManager
import requests
from requests.exceptions import ConnectionError
import random
import time
import codecs
from requests.exceptions import ReadTimeout
import traceback

__author__ = 'pgaref'

class RequestProxy:

    currentWorkingProxy = None
    useProxy = True

    def __init__(self, web_proxy_list=[]):
        self.userAgent = UserAgentManager()

        #####
        # Each of the classes below implements a specific URL Parser
        #####
        parsers = []
        parsers.append(freeproxyParser('http://free-proxy-list.net'))
        parsers.append(proxyforeuParser('http://proxyfor.eu/geo.php', 100.0))
        parsers.append(rebroweeblyParser('http://rebro.weebly.com/proxy-list.html'))
        #parsers.append(semairproxyParser('http://www.samair.ru/proxy/time-01.htm'))

        print "=== Initialized Proxy Parsers ==="
        for i in range(len(parsers)):
            print "\t {0}".format(parsers[i].__str__())
        print "================================="

        self.parsers = parsers
        self.proxy_list = web_proxy_list
        for i in range(len(parsers)):
            self.proxy_list += parsers[i].parse_proxyList()


    def get_proxy_list(self):
        return self.proxy_list

    def generate_random_request_headers(self):
        headers = {
            "Connection": "close",  # another way to cover tracks
            "User-Agent": self.userAgent.get_random_user_agent()
        }  # select a random user agent
        return headers

    #####
    # Proxy format:
    # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
    #####
    def generate_proxied_request(self, url, params={}, req_timeout=30):
        random.shuffle(self.proxy_list)
        req_headers = dict(params.items() + self.generate_random_request_headers().items())

        request = None
        try:
            rand_proxy = None

            if self.useProxy:
                if not self.currentWorkingProxy == None:
                    rand_proxy = self.currentWorkingProxy
                else:
                    rand_proxy = random.choice(self.proxy_list)
                    self.currentWorkingProxy = rand_proxy

                print "Using proxy: {0}".format(str(rand_proxy))
                request = requests.get(url, proxies={"http": rand_proxy},
                                   headers=req_headers, timeout=req_timeout)
            else:
                print "Not Using proxy"
                request = requests.get(url,headers=req_headers, timeout=req_timeout)

            if not request.status_code == 200:
                print "Proxy request status code:" + str(request.status_code)
                self.currentWorkingProxy = None

        except ConnectionError:
            self.proxy_list.remove(rand_proxy)
            print "Proxy unreachable - Removed Straggling proxy: {0} PL Size = {1}".format(rand_proxy, len(self.proxy_list))
            self.currentWorkingProxy = None
            pass
        except ReadTimeout:
            self.proxy_list.remove(rand_proxy)
            print "Read timed out - Removed Straggling proxy: {0} PL Size = {1}".format(rand_proxy, len(self.proxy_list))
            self.currentWorkingProxy = None
            pass
        except KeyboardInterrupt:
            raise
        except:
            print "Unexpected error:", sys.exc_info()[0]
            outPutFileName = "ErrorLogs/netWorkLog.log"
            if not os.path.exists(os.path.dirname(outPutFileName)):
                try:
                    os.makedirs(os.path.dirname(outPutFileName))
                except OSError as exc:
                    if exc.errno != exc.EEXIST:
                        raise

            with codecs.open(outPutFileName,"a","utf-8") as errorLogFile:
                format = '%Y-%m-%d %H:%M:%S'
                errorLogFile.write("Unexpected error:("+time.strftime(format)+")" + str(traceback.format_exc())+"\n\n")

            self.currentWorkingProxy = None
            raise

        return request

if __name__ == '__main__':

    start = time.time()
    req_proxy = RequestProxy()
    print "Initialization took: {0} sec".format((time.time()-start))
    print "Size : ", len(req_proxy.get_proxy_list())
    print " ALL = ", req_proxy.get_proxy_list()

    test_url = 'http://localhost:8888'

    while True:
        start = time.time()
        request = req_proxy.generate_proxied_request(test_url)
        print "Proxied Request Took: {0} sec => Status: {1}".format((time.time()-start), request.__str__())
        print "Proxy List Size: ", len(req_proxy.get_proxy_list())

        print"-> Going to sleep.."
        time.sleep(10)
