import requests
from typing import Tuple
import random
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

API_KEY = os.environ.get('PROXY6_API_KEY')
URL = f"https://proxy6.net/api/{API_KEY}"


def get_proxy(username: str) -> str:
    """Fetch all the proxies from the provider and return a random URL of a proxy"""
    urls = []
    expired = ""

    req = requests.get(f"{URL}/getproxy?descr={username}&nokey")
    proxies = req.json()['list']

    # TODO When starting with the real accounts, remove the check on the version "3", only use ipv4 EU private, not shared.

    totalProxies = 0
    for proxy in proxies:
        if proxy['version'] == "4" or proxy['version'] == "3":
            totalProxies += 1

    if totalProxies < 1:
        proxyUrl = buy_proxy(username)
        return proxyUrl

    for proxy in proxies:
        if proxy['type'] == "socks" and proxy['active'] == "1" and proxy['version'] == "4" or proxy['version'] == "3":
            urls.append(
                f"socks5h://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}")

        elif proxy['active'] == "0":
            expired += f"{proxy['id']},"

    proxyUrl = random.choice(urls)

    if expired:
        delete_expired_proxy(expired[:-1])

    return proxyUrl


def get_available_proxies() -> str:
    """Returns the number of proxies available for one of those country"""
    countries = ['it', 'fr', 'es', 'at', 'nl', 'cy', 'dk',
                 'fi', 'ee', 'de', 'ie', 'lt', 'ch', 'se']

    count = 0
    for country in countries:
        req = requests.get(f"{URL}/getcount?country={country}&version=4")
        count = int(req.json()['count'])
        if count > 0:
            break

    if count == 0:
        raise Exception("No proxies available")

    return country


def buy_proxy(username: str) -> str:
    """Buy a proxy and return the URL"""

    print("BUYING PROXY, WAITING 100SECONDS")
    sleep(100)

    country = get_available_proxies()

    req = requests.get(
        f"{URL}/buy?count=1&period=3&country={country}&version=4type=socks&descr={username}&nokey")
    print(req.json())
    proxy = req.json()['list'][0]

    proxyUrl = f"socks5h://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"

    print("PROXY BOUGHT")
    return proxyUrl


def delete_expired_proxy(ids: str) -> None:
    """Delete the expired proxies"""
    requests.get(f"{URL}/delete?ids={ids}")
