import requests
from typing import Tuple
import random
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

API_KEY = os.environ.get('PROXY6_API_KEY')
URL = f"https://proxy6.net/api/{API_KEY}"


def get_proxy() -> str:
    """Fetch all the proxies from the provider and return a random URL of a proxy"""
    urls = []
    expired = ""

    req = requests.get(f"{URL}/getproxy?nokey")
    proxies = req.json()['list']

    totalProxies = 0
    for proxy in proxies:
        if proxy['version'] == "4" or proxy['version'] == "3":
            totalProxies += 1

    if totalProxies <= 1:
        proxyUrl = buy_proxy()
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


def get_available_proxies() -> Tuple[str, int]:
    """Returns the number of proxies available for one of those country"""
    countries = ["fr", "au", "jp", "sg"]
    count = 0
    for country in countries:
        req = requests.get(f"{URL}/getcount?country={country}")
        count = int(req.json()['count'])
        if count > 0:
            break

    if count == 0:
        raise Exception("No proxies available")

    return country, count


def buy_proxy() -> str:
    """Buy a proxy and return the URL"""

    print("BUYING PROXY, WAITING 100SECONDS")
    sleep(100)

    country, count = get_available_proxies()
    if count >= 1:
        req = requests.get(
            f"{URL}/buy?count=1&period=3&country={country}&version=4type=socks&nokey")
        proxy = req.json()['list'][0]

        proxyUrl = f"socks5h://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"

    print("PROXY BOUGHT")
    return proxyUrl


def delete_expired_proxy(ids: str) -> None:
    """Delete the expired proxies"""
    requests.get(f"{URL}/delete?ids={ids}")
