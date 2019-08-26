# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.join(sys.path[0], '../../'))

import requests
import schedule
from instabot import Bot, utils
import re

import config

def test_proxy(proxy, save=False):
    bot = Bot(proxy=proxy)
    if bot and bot.login(username="rafikizjuice_ug", password="Ultimate32", proxy=proxy, ignore_429_sleep=True) and bot.api.last_response and bot.api.last_response.status_code == 200:
       	if save:
            print("Saving the good proxy to %s" % config.PROXY_FILE)
            file = open(config.PROXY_FILE,"w")
            file.write(proxy)
            file.close()
        return True
    try:
        bot.logout()
    except:
        pass

    return False
    	

if os.path.isfile(config.PROXY_FILE):
    proxy_file = open(config.PROXY_FILE, "r")
    if (proxy_file):
    	proxy_str = proxy_file.readline()
    	if re.match("https://*:*", proxy_str) and test_proxy(proxy_str):
    		print("Already have a good proxy %s" % proxy_str)
    		exit(0)

print("Found no good proxy. Going to look for one...")
response = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=yes&anonymity=anonymous")
if response.status_code == 200:
  proxies = response.content.split()
  for proxy in proxies:
    proxy_str = "https://" + proxy.decode("utf-8")
    if test_proxy(proxy_str, True):
    	exit(0)

# fails if it doesn't find a good proxy
print("Failed to find a good proxy")
exit(1)
