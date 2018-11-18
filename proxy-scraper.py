import requests, sys, re, queue, threading, traceback, requests

if sys.version_info[0] != 3:
	print("This script needs Python 3")
	exit()

if len(sys.argv) != 3:
	print("python3 proxy-scraper.py check output\n")
	print("Example: python3 proxy-scraper.py yes checked-proxies.txt")
	exit()

proxies = []

try:
	fate0_proxylist = requests.get("https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list").text
	fate0_proxylist = fate0_proxylist.replace('null', '"N/A"')
	for proxy in re.findall(r'"host": "([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})".*?"country": "(.*?){2}",.*?"port": ([0-9]{1,5})', fate0_proxylist):
		proxies.append([proxy[0] + ":" + proxy[2], proxy[1]])
except:
	print("fate0 failed")

try:
	a2u_proxylist = requests.get("https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', a2u_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("a2u failed")

try:
	clarketm_proxylist = requests.get("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt")
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5}) (.*?){2}-.-S \+', clarketm_proxylist.text):
		proxies.append([proxy[0] + ":" + proxy[1], proxy[2]])
except:
	print("clarketm failed")

try:
	opsxcq_proxylist = requests.get("https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', opsxcq_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("opsxcq failed")

try:
	usproxyorg_proxylist = requests.get("https://www.us-proxy.org/").text
	for proxy in re.findall(r"<tr><td>([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})<\/td><td>([0-9]{1,5})<\/td><td>(.*?){2}<\/td><td class='hm'>.*?<\/td><td>.*?<\/td><td class='hm'>.*?<\/td><td class='hx'>(.*?)<\/td><td class='hm'>.*?<\/td><\/tr>", usproxyorg_proxylist):
		if proxy[3] != "yes":
			continue
			proxies.append([proxy[0] + ":" + proxy[1], proxy[2]])
except:
	print("usproxyorg failed")

try:
	freeproxylistnet_proxylist = requests.get("https://free-proxy-list.net/").text
	for proxy in re.findall(r"<tr><td>([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})<\/td><td>([0-9]{1,5})<\/td><td>(.*?){2}<\/td><td class='hm'>.*?<\/td><td>.*?<\/td><td class='hm'>.*?<\/td><td class='hx'>(.*?)<\/td><td class='hm'>.*?<\/td><\/tr>", freeproxylistnet_proxylist):
	        if proxy[3] != "yes":
	                continue
	        proxies.append([proxy[0] + ":" + proxy[1], proxy[2]])
except:
	print("freeproxylistnet failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/HTTP_Working_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/Socks4_Working_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/Socks5_Working_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/HTTP_Transparent_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/HTTP_Anonymous_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/HTTP_Elite_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/HTTP_5000ms_Timeout_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/Socks5_5000ms_Timeout_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/Socks4_5000ms_Timeout_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")

try:
	proxyscrapecom_proxylist = requests.get("https://proxyscrape.com/proxies/HTTP_SSL_Proxies_5000ms_Timeout_Proxies.txt").text
	for proxy in re.findall(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}):([0-9]{1,5})', proxyscrapecom_proxylist):
		proxies.append([proxy[0] + ":" + proxy[1], "N/A"])
except:
	print("proxyscrapecom failed")


print("{} proxies fetched".format(len(proxies)))
proxies_ok = []

f = open(sys.argv[2], "w")
if sys.argv[1] == "yes":
	print("Checking with 10 threads (HTTPS, 5 seconds timeout)")
	q = queue.Queue()
	for x in proxies:
		q.put(x)
	dead = 0
	alive = 0
	def checkProxies():
		global q
		global dead
		global alive
		global f
		global proxies
		while not q.empty():
			proxy = q.get()
			try:
				requests.get("https://httpbin.org/ip", proxies={'https':'http://'+proxy[0]}, timeout=5)
				alive += 1
				f.write("{} - {}\n".format(proxy[0], proxy[1]))
				f.flush()
			except:
				dead += 1

			sys.stdout.write("\rChecked %{:.2f} - (Alive: {} - Dead: {})".format((alive + dead) / len(proxies) * 100, alive, dead))
			sys.stdout.flush()
	threads = []
	for i in range(0, 10):
		t = threading.Thread(target=checkProxies)
		t.start()
		threads.append(t)
	for t in threads:
		t.join()
	print("")
else:
	for proxy in proxies:
		f.write("{} - {}\n".format(proxy[0], format[1]))

f.close()
