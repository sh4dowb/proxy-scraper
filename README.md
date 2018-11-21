

# Proxy Scraper & Checker & Free List

Easy proxy scraper & checker, and publicly available list

```
usage: proxy-scraper.py [-h] [-c] -o OUTPUT [-t THREADS] [--timeout TIMEOUT]
                        [--http] [--check-with-website CHECK_WITH_WEBSITE]
                        [--country] [--connection-time] [-f] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -c, --check           Check the scraped proxies
  -o OUTPUT, --output OUTPUT
                        Output file
  -t THREADS, --threads THREADS
                        Checker threads count (default: 30)
  --timeout TIMEOUT     Checker timeout in seconds (default: 5)
  --http                Check proxies for HTTP instead of HTTPS
  --check-with-website CHECK_WITH_WEBSITE (default: httpbin.org/ip)
                        Website to connect with proxy. If it doesn't return
                        HTTP 200, it's dead
  --country             Locate and print country (requires maxminddb-geolite2)
  --connection-time     Print connection time information
  -f, --write-immediately
                        Force flush the output file every time
  -i, --extra-information
                        Print last updated time, and configuration description
```


This runs on my server:
```
python3 /root/proxy-scraper.py --check -t 300 --timeout 5 --check-with-website httpbin.org/ip --country --connection-time --extra-information --output /home/admin/web/cagriari.com/public_html/fresh_proxy.txt 
```

<br><br>
Hourly updated & checked proxy list: https://cagriari.com/fresh_proxy.txt

HTTPS, 5 seconds timeout

_*actually it takes about +10 mins for checking_
