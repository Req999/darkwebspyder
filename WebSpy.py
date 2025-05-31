'''
Req999
'''

__version__ = 1

import sys
sys.dont_write_bytecode = True

import requests
from bs4 import BeautifulSoup
import os
import time
import argparse
import random
import re
import json
import socket
from banner import Banner

# Ensure required modules are installed
try:
    import nltk
    from textblob import TextBlob
    from termcolor import cprint, colored
except ModuleNotFoundError as e:
    print(f"[Error] Missing module: {e.name}. Install it using: pip install {e.name}")
    sys.exit(1)

# Download necessary NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Tor Proxy Configuration
TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

#User-Agent list for Kali Linux
USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Kali Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

class Configuration:
    __webspy_engines__ = [
        "https://ahmia.fi/search/?q=",
        "https://onionsearchengine.com/search?q=",
        "https://onionlandsearchengine.com/search?q=",
        "https://haystack.search/search?q=",
        "https://deeplink.search/?q=",
        "https://phobos.search/search?q=",
        "http://tor66sear.ch/search?q=",
        "https://torgle.search/?q=",
        "http://darksearch.io/search?q=",
        "https://multivacsearchengine.com/search?q="
    ]

class Platform(object):
    def check_tor_connection(self):
        test_url = 'http://check.torproject.org'
        try:
            response = requests.get(test_url, proxies=TOR_PROXY, timeout=10)
            if 'Congratulations' in response.text:
                print(colored("[+] Tor is active. You are browsing anonymously.", "green"))
                return True
            else:
                print(colored("[-] Tor is not properly configured.", "red"))
        except requests.RequestException:
            print(colored("[Error] Unable to connect to Tor. Ensure the Tor service is running.", "red"))
        return False

class WebSpy(object):
    def crawl(self, query, amount, use_proxy=False):
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        proxy_config = TOR_PROXY if use_proxy else {}

        if use_proxy and not Platform().check_tor_connection():
            return

        for search_engine in Configuration.__webspy_engines__:
            search_url = search_engine + query
            try:
                print(colored(f"Querying: {search_engine}", "yellow"))
                response = requests.get(search_url, headers=headers, proxies=proxy_config, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                results = soup.find_all('a', href=True)
                for result in results:
                    print(colored(f"Found: {result['href']}", "green"))
            except requests.RequestException as e:
                print(colored(f"[Error] {search_engine} -> {e}", "red"))

# Main Function
def webspy_main():
    bn = Banner()
    try:
        bn.LoadWebSpyBanner()
    except AttributeError:
        print("[Error] Banner method not found.")

    parser = argparse.ArgumentParser(description="WebSpy - Deep Web Scraper")
    parser.add_argument("-q", "--query", help="Keyword to search on the deep web", type=str)
    parser.add_argument("-a", "--amount", help="Number of results to retrieve", type=int, default=10)
    parser.add_argument("-p", "--proxy", help="Use Tor proxy for scraping", action="store_true")
    args = parser.parse_args()

    if args.query:
        print(f"Searching For: {args.query} and showing results...")
        WebSpy().crawl(args.query, args.amount, use_proxy=args.proxy)
    else:
        print("[~] No query provided. Use -q <query> to search.")

if __name__ == "__main__":
    webspy_main()
