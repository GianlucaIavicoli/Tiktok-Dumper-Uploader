import asyncio
import json
from TikTokApi import TikTokApi
import asyncio
import sys
import os
import random
from pyrogram import Client
from const import *
from upload import upload_video


async def create_session(channel: str):
    """Create a new session, save the cookies and return it"""
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens="ms_token", num_sessions=1, sleep_after=5)
        session = api._get_session()
        cookie = await api.get_session_cookies(session[1])
        with open(file=f"cookies/{channel}.json", mode="w", encoding="utf-8") as file:
            json.dump(obj=cookie, fp=file, indent=4)

        return session


def get_cookie(channel: str):
    """Read the session file and returns the cookies"""
    with open(file=f"cookies/{channel}.json", mode="r", encoding="utf-8") as file:
        cookie = json.loads(file.read())
    return cookie


async def dump_channel_videos(channel: str, channelDump: str):
    # Create default files

    cookie = get_cookie(channel)
    ms_token = cookie["msToken"]
    videoUrls = []

    # TODO Add the proxy usage while scraping videos from tiktok
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=10, cookies=[cookie])
        async for video in api.user(username=channelDump).videos(count=LIMIT_VIDEOS_TO_DUMP):
            username = video.author.username
            videoId = video.id
            description = video.as_dict['desc']
            song = video.sound.as_dict['music']['title']
            if song == "original sound":
                song = None

            url = f"https://www.tiktok.com/@{username}/video/{videoId}"

            videoDict = {
                "username": username,
                "videoId": videoId,
                "description": description,
                "song": song,
                "url": url,
                "channel": channel
            }

            videoUrls.append(videoDict)

        with open(file="data/dumped.json", mode="r", encoding="utf-8") as file:
            try:
                videosAvailable = json.load(file)
            except:
                videosAvailable = {"dumped": []}

        [videosAvailable['dumped'].append(
            newVideo) for newVideo in videoUrls if newVideo not in videosAvailable['dumped']]

        with open(file="data/dumped.json", mode="w", encoding="utf-8") as file:
            json.dump(videosAvailable, file, indent=4)

        await api.close_sessions()
        return await telegram_download(videoUrls)


# Telegram

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")


async def telegram_download(videoUrls: list):
    """Connect, get the videos without the watermark and then delete them from the chat"""
    async with Client("telegram_session/bot") as client:
        for videoDict in videoUrls:
            # Only if the video is not present here
            if not os.path.exists(f"videos/{videoDict['videoId']}.mp4"):
                initialMessage = await client.send_message("tikwatermark_remover_bot", videoDict['url'])
                initialMessageId = initialMessage.id + 2
                await asyncio.sleep(SLEEP_BETWEEN_SCRAPE_TELEGRAM_VIDEO)

                reponseMessage = await client.get_messages("tikwatermark_remover_bot", initialMessageId)
                await client.download_media(reponseMessage, progress=progress, file_name=f"videos/{videoDict['videoId']}.mp4")
            else:
                print(f"Video {videoDict['videoId']} already downloaded")


def upload(channel: str, channelDump: str):
    with open(file="data/dumped.json", mode="r", encoding="utf-8") as file:
        videosDumpedDict = json.load(file)

    with open(file="data/uploaded.json", mode="r", encoding="utf-8") as file:
        videosUploadedDict = json.load(file)

    videosAvailable = []
    for video in videosDumpedDict['dumped']:
        if video['username'] == channelDump:
            videosAvailable.append(video)

    videoToDump = random.choice(videosAvailable)

    upload_video(f"videos/{videoToDump['videoId']}.mp4", description=videoToDump['description'],
                 song=videoToDump['song'], channel=channel, cookies=f"cookies/{channel}.txt", headless=False, browser='chrome')

    os.remove(f"videos/{videoToDump['videoId']}.mp4")
    videosAvailable.remove(videoToDump)

    # Add the uploaded video in the right json after being removed from the "dumped.json"
    videosUploadedDict['uploaded'].append(videoToDump)

    with open(file="data/uploaded.json", mode="w", encoding="utf-8") as file:
        json.dump(videosUploadedDict, file, indent=4)

    with open(file="data/dumped.json", mode="w", encoding="utf-8") as file:
        json.dump({"dumped": videosAvailable}, file, indent=4)


def setup():

    # Create files
    if not os.path.exists("data/dumped.json"):
        with open("data/dumped.json", "w") as file:
            json.dump({"dumped": []}, file, indent=4)

    if not os.path.exists("data/uploaded.json"):
        with open("data/uploaded.json", "w") as file:
            json.dump({"uploaded": []}, file, indent=4)

    # Create dirs
    if not os.path.isdir("cookies"):
        os.mkdir("cookies")

    if not os.path.isdir("videos"):
        os.mkdir("videos")

    if not os.path.isdir("data"):
        os.mkdir("data")

    if not os.path.isdir("telegram_session"):
        os.mkdir("telegram_session")


if __name__ == "__main__":
    channel = "__copyandpaste"
    channelDump = "__copyandpaste"
    setup()
    if channel not in CHANNELS:
        raise Exception("Wrong channel name")
    # asyncio.run(dump_channel_videos(channel, channelDump))
    upload(channel, channelDump)
