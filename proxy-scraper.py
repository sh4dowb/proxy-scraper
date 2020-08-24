#!/usr/bin/python3

import sys

if sys.version_info[0] < 3:
	print("This script needs Python 3")
	exit()

import requests, re, queue, threading, traceback, requests, datetime, time, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--check', help="Check the scraped proxies", action='store_true')
parser.add_argument('-o', '--output', help="Output file", required=True)
parser.add_argument('-t', '--threads', type=int, default=20, help="Checker threads count")
parser.add_argument('--timeout', type=int, default=5, help="Checker timeout in seconds")
parser.add_argument('--http', help="Check proxies for HTTP instead of HTTPS", action='store_true')
parser.add_argument('--check-with-website', help="Website to connect with proxy. If it doesn't return HTTP 200, it's dead", default="httpbin.org/ip")
parser.add_argument('--country', help="Locate and print country (requires maxminddb-geolite2)", action='store_true')
parser.add_argument('--connection-time', help="Print connection time information", action='store_true')
parser.add_argument('-f', '--write-immediately', help="Force flush the output file every time", action='store_true')
parser.add_argument('-i', '--extra-information', help="Print last updated time, and configuration description", action='store_true')
parserx = parser.parse_args()
threads = parserx.threads
https = not parserx.http
timeout = parserx.timeout
reader = None
if parserx.country:
	try:
		from geolite2 import geolite2
		reader = geolite2.reader()
	except ImportError:
		print("Error: maxminddb-geolite2 is not installed. Please try without --country option or install this package.")
		exit()

proxies = []


def fetchAndParseProxies(url, custom_regex):
	global proxies
	n = 0
	proxylist = requests.get(url, timeout=5).text
	proxylist = proxylist.replace('null', '"N/A"')
	custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
	custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
	for proxy in re.findall(re.compile(custom_regex), proxylist):
		proxies.append(proxy[0] + ":" + proxy[1])
		n += 1
	sys.stdout.write("{0: >5} proxies fetched from {1}\n".format(n, url))


proxysources = [
	["http://spys.me/proxy.txt","%ip%:%port% "],
	["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
	["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
	["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
	["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
	["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
	["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
	["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
	["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
	["https://www.proxy-list.download/api/v0/get?l=en&t=https", '"IP": "%ip%", "PORT": "%port%",'],
	["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
	["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
	["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
	["https://proxylist.icu/", "<td>%ip%:%port%</td><td>http<"],
	["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
	["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
	["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
	["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
	["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
	["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
	["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",']
]

sourcethreads = []
for source in proxysources:
	t = threading.Thread(target=fetchAndParseProxies, args=(source[0], source[1]))
	sourcethreads.append(t)
	t.start()

for t in sourcethreads:
	t.join()

proxies_unique = list(set(proxies))
print("{0: >5} proxies fetched total, {1} unique.".format(len(proxies), len(proxies_unique)))
proxies = proxies_unique
proxies_ok = []

f = open(parserx.output, "w")
if parserx.extra_information:
	f.write("# Last updated: {}\n".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
	if parserx.check:
		f.write("# {}, {}-second timeout\n".format("HTTPS" if https else "HTTP", timeout))
	f.write("# https://github.com/sh4dowb/proxy-scraper\n\n")

if parserx.check:
	print("Checking with {} threads ({}, {} seconds timeout)".format(threads, "HTTPS" if https else "HTTP", timeout))
	q = queue.Queue()
	for x in proxies:
		q.put([x, "N/A"])
	dead = 0
	alive = 0
	def checkProxies():
		global q
		global dead
		global alive
		global f
		global proxies
		global timeout
		while not q.empty():
			proxy = q.get()
			try:
				resp = requests.get(("https" if https else "http") + ("://" + parserx.check_with_website), proxies={'http':'http://'+proxy[0],'https':'http://'+proxy[0]}, timeout=timeout)
				if resp.status_code != 200:
					raise BadProxy
				if parserx.country:
					try:
						proxy[1] = reader.get(proxy[0].split(':')[0])['country']['iso_code']
					except KeyError:	
						pass
					except IndexError:
						pass
					except TypeError:
						pass
				f.write("{}|{}|{:.2f}s\n".format(proxy[0], proxy[1], resp.elapsed.total_seconds()))
				if alive % 30 == 0:
					f.flush()
				alive += 1
			except:
				dead += 1

			sys.stdout.write("\rChecked %{:.2f} - (Alive: {} - Dead: {})".format((alive + dead) / len(proxies) * 100, alive, dead))
			sys.stdout.flush()

	threadsl = []
	for i in range(0, threads):
		t = threading.Thread(target=checkProxies)
		t.start()
		threadsl.append(t)
	for t in threadsl:
		t.join()

	sys.stdout.write("\rCompleted - Alive: {} - Dead: {}         \n".format(alive, dead))
	print("")
else:
	for proxy in proxies:
		f.write("{}\n".format(proxy))

f.close()
